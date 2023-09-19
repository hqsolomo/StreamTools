import json
import os
import http.server
import socket
import socketserver
import time
import urllib.parse
import threading
import subprocess
from st_process import ST_Process
import streamtools_settings as s
from pick_audio import pick_audio

# TODO: eventually replace with something a bit more secure
class CommandCenter(http.server.SimpleHTTPRequestHandler):
    
    TEMPLATE_ROOT = os.path.join('api', 'controlcenter', 'streamtools.html')
    TEMPLATE_SETTINGS = os.path.join('api', 'controlcenter', 'settings.html')
    TEMPLATE_CLIPS = os.path.join('api','controlcenter','clips.html')

    def read_template(self, template_name):
        try:
            with open(os.path.join('api', 'controlcenter', template_name), 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Template {template_name} not found!")
            return None

    def apply_common_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Server', '')
        self.send_header('X-Frame-Options', 'DENY')
        self.send_header('Content-Security-Policy', "'frame-ancestors 'self'; unsafe-inline 'self' script-src 'self''")
        self.send_header('Content-type', 'text/html')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()

    #TODO: link root to landing page or something
    def get_root(self):
        template = self.read_template('streamtools.html')
        if template is None:
            return None
        return template.format()

    #TODO: move all playaudio here
    def get_clips(self):
        template = self.read_template('clips.html')
        if template is None:
            return None
        file_list = ["<ul>"]
        for path in s.content.items():
            file_list.append(f"<li>{path[0]}: <button onclick='playAudio(\"{urllib.parse.quote(path[0])}\", \"{path[0]}\", \"{path[0]}\")'>Play {path[0]} on server</button></li>")
        file_list.append("</ul>")
        return template.format(clips="".join(file_list))

    def get_config(self):
        return self.read_template('settings.html')

    def do_GET(self):
        match self.path:
            case '/':
                message = self.get_root()
                if message is None:
                    self.apply_common_headers(500)
                    print("ERROR")
                else:
                    self.apply_common_headers()
                    self.wfile.write(bytes(message, "utf8"))
            case '/settings':
                message = self.get_config()
                self.apply_common_headers()
                self.wfile.write(bytes(message, "utf8"))
            case '/clips':
                #TODO: move this
                message = self.get_clips()
                if message is None:
                    self.apply_common_headers(500)
                    print("ERROR")
                else:
                    self.apply_common_headers()
                    self.wfile.write(bytes(message, "utf8"))
            case _:
                super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        if self.path == '/play':
            self.apply_common_headers()
            random_audio_file = pick_audio(post_data)
            file_path = os.path.join(urllib.parse.unquote(random_audio_file.path))
            proc = subprocess.Popen(['py', os.path.join('api', 'controlcenter', 'play_audio.py'), file_path])
            time.sleep(s.config['clip_duration'])
            proc.terminate()
            
        elif self.path == '/settings':
            try:
                new_config = json.loads(post_data)
                with open('config.json', 'w') as f:
                    json.dump(new_config, f)
                self.apply_common_headers()
            except json.JSONDecodeError:
                self.apply_common_headers(400)
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
            sock.send(b"Host: " + bytes(str(self.server_address), "utf8") + b"\r\n")
            sock.send(b"Connection: close\r\n")
            sock.send(b"\r\n")

if __name__ == '__main__':
    with socketserver.TCPServer((s.config['server_bind_address'], s.config['server_port']), CommandCenter) as httpd:
        print(f"Serving at {httpd.server_address}")
        t = threading.Thread(target=httpd.serve_forever)
        t.daemon = True
        t.start()
        input("Press Enter to stop the server\n")
        httpd.shutdown()
