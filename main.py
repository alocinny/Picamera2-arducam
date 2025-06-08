import sys
import time
from camera import Camera
from web_streamer import WebStreamer

def main():
    """Função principal para iniciar a câmera e o servidor web."""
    camera = None
    web_server = None
    try:

        camera = Camera()
        camera.start()

        time.sleep(2) 

        web_server = WebStreamer(camera=camera, port=8000)
        web_server.run() 

    except KeyboardInterrupt:
        print("\nRecebido comando para desligar (Ctrl+C).")
    finally:
        if camera:
            camera.stop()
        if web_server:
            pass
        print("Aplicação encerrada.")
        sys.exit(0)

if __name__ == "__main__":
    main()