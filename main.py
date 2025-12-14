from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import webbrowser
import socket
from threading import Thread
import time
import json
from datetime import datetime

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/save-data':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Data collection initiated')
            return
        
        if self.path == '/':
            self.path = '/web.html'
        
        return super().do_GET()
    
    def do_POST(self):
        if self.path == '/save-data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"collected_data_{timestamp}.json"
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "file": filename}).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode())
            return
        
        self.send_response(404)
        self.end_headers()

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def open_browser():
    time.sleep(2)
    webbrowser.open(f'http://{local_ip}:{port}')

if __name__ == '__main__':
    port = 8080
    local_ip = get_local_ip()
    
    print("🌀 Запуск системы сбора данных...")
    print(f"🌐 Сервер запущен: http://{local_ip}:{port}")
    print("📁 Данные сохраняются в JSON файлы")
    print("🛑 Ctrl+C для остановки")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        server = HTTPServer(('', port), CORSHTTPRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️ Сервер остановлен")