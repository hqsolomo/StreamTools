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
    server_port = config['server_port']
    content_library = config['content_library']
    # Read content library from content.json file
with open('content.json', 'r') as f:
    content = json.load(f)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Read the template file
            with open('streamtools.html', 'r') as file:
                template = file.read()

            # Populate the template with the file list
            file_list = "<ul>"
            for path in content.items():
                file_list += f"<li>{path[0]}: <button onclick='playAudio(\"{urllib.parse.quote(path[0])}\", \"{path[0]}\", \"{path[0]}\")'>Play " + path[0] + " on server</button></li>"
            file_list += "</ul>"
            message = template.format(clips=file_list)
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
            proc = subprocess.Popen(['py', 'play_audio.py', file_path])
            time.sleep(config['clip_duration'])
            proc.terminate()
            self.send_response(200)
            self.end_headers()

        elif self.path == '/update_config':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                new_config = json.loads(post_data)
                with open('config.json', 'w') as f:
                    json.dump(new_config, f)
                self.send_response(200)
            except:
                self.send_response(400)
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

    with socketserver.TCPServer(("", server_port), Handler) as httpd:
        print(f"Serving at port {server_port}")
        t = threading.Thread(target=httpd.serve_forever)
        t.daemon = True
        t.start()
        input("Press Enter to stop the server\n")
        httpd.shutdown()
