import time
from threading import Lock, Thread

import cv2
from picamera2 import Picamera2

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()

        config = self.picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
        self.picam2.configure(config)
        self.frame = None
        self.lock = Lock()
        self.running = False
        self.thread = Thread(target=self._capture_loop, daemon=True)

    def start(self):
        """Inicia a captura de frames em uma thread separada."""
        print("Iniciando a câmera...")
        self.running = True
        self.picam2.start()
        self.thread.start()
        print("Câmera iniciada.")

    def stop(self):
        """Para a captura de frames."""
        print("Parando a câmera...")
        self.running = False
        self.thread.join()
        self.picam2.stop()
        print("Câmera parada.")

    def _capture_loop(self):

        while self.running:
            array = self.picam2.capture_array()

            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(array, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # eh aq q deve ser chamado a função de visão e tal p testar

            success, encoded_image = cv2.imencode(".jpg", array)
            if not success:
                continue

            with self.lock:
                self.frame = encoded_image.tobytes()

    def get_frame(self):
        with self.lock:
            return self.frame