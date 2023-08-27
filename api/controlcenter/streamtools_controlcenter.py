import json
import os
import http.server
import socket
import socketserver
import time
import urllib.parse
import threading
import subprocess
from pick_audio import pick_audio

# Read server port and content library from config.json file
with open('config.json', 'r') as f:
    config = json.load(f)
    server_bind_address = config['server_bind_address']
    print(server_bind_address)
    server_port = config['server_port']
    print(server_port)
    content_library = config['content_library']
    # Read content library from content.json file
with open('content.json', 'r') as f:
    content = json.load(f)

# TODO: eventually replace with something a bit more secure
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def get_root(self):
        # Read the template file
        with open('api\controlcenter\streamtools.html', 'r') as file:
            template = file.read()
        # Populate the template with the file list
        file_list = "<ul>"
        for path in content.items():
            file_list += f"<li>{path[0]}: <button onclick='playAudio(\"{urllib.parse.quote(path[0])}\", \"{path[0]}\", \"{path[0]}\")'>Play " + path[0] + " on server</button></li>"
        file_list += "</ul>"
        return template.format(clips=file_list)
    def get_config(self):
        with open('api\controlcenter\settings.html', 'r') as file:
                template = file.read()
    def do_GET(self):
        if self.path == '/':
            message = self.get_root()
            if message == None:
              self.send_response(500)
              print("ERROR")
            else:
                self.send_response(200)
                self.send_header('Server', '')
                self.send_header('X-Frame-Options', 'DENY')
                self.send_header('Content-Security-Policy', "'frame-ancestors 'self'; unsafe-inline 'self' script-src 'self''")
                self.send_header('Content-type', 'text/html')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.end_headers()
                self.wfile.write(bytes(message, "utf8"))
        elif self.path == '/settings':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(message, "utf8"))
        else:
            super().do_GET()
    def do_POST(self):
        global audio_proc
        if self.path == '/play':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            random_audio_file = pick_audio(post_data, content)
            file_path = os.path.join(urllib.parse.unquote(random_audio_file.path))
            proc = subprocess.Popen(['py', 'api\controlcenter\play_audio.py', file_path])
            time.sleep(config['clip_duration'])
            proc.terminate()
            self.send_response(200)
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()

        elif self.path == '/settings':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                new_config = json.loads(post_data)
                with open('config.json', 'w') as f:
                    json.dump(new_config, f)
                self.send_response(200)
                self.send_header('X-Content-Type-Options', 'nosniff')
            except:
                self.send_response(400)
                self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
        else:
            super().do_POST()

    def serve_forever(self):
        self.keep_running = True
        while self.keep_running:
            self.handle_request()

    def shutdown(self):
        self.keep_running = False
        host, port = self.server_address
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.send(b"GET /shutdown HTTP/1.1\r\n")
            sock.send(b"Host: " + self.server_address +"\r\n")
            sock.send(b"Connection: close\r\n")
            sock.send(b"\r\n")

if __name__ == '__main__':
    Handler = MyHandler
    print(str.format("{host}:{port}",host = server_bind_address, port = server_port))
    with socketserver.TCPServer((server_bind_address, server_port), Handler) as httpd:
        print(f"Serving at {httpd.server_address}")
        t = threading.Thread(target=httpd.serve_forever)
        t.daemon = True
        t.start()
        input("Press Enter to stop the server\n")
        httpd.shutdown()
