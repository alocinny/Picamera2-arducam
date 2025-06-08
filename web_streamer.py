import logging
import socketserver
from http import server

# página HTML simples para exibir o stream
PAGE = """
<html>
<head>
<title>Raspberry Pi - Câmera com OpenCV</title>
<style>
  body { font-family: Arial, sans-serif; text-align: center; background-color: #282c34; color: white; }
  img { display: block; margin: 20px auto; border: 3px solid #00FF00; }
  h1 { color: #00FF00; }
</style>
</head>
<body>
<h1>Streaming com Picamera2 e OpenCV</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:

                    frame = self.server.camera.get_frame()
                    if frame is None:
                        continue
                    
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning('Cliente removido: %s', str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

class WebStreamer:
    def __init__(self, camera, port=8000):
        self.camera = camera
        self.port = port
        self.server = StreamingServer(('', self.port), StreamingHandler)
        self.server.camera = camera

    def run(self):
        """Inicia o servidor web."""
        print(f"Servidor de streaming iniciado. Acesse em http://<IP_DA_RASPBERRY>:{self.port}")
        self.server.serve_forever()

    def stop(self):
        """Para o servidor web."""
        print("Parando o servidor web...")
        self.server.shutdown()
        self.server.server_close()
        print("Servidor web parado.")