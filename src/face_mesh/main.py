from pathlib import Path
from typing import TYPE_CHECKING

import cv2
import pygame

from face_mesh.face_mesh_detector import FaceMeshDetector
from face_mesh.utils import process_drowsiness_logic, setup_pygame

if TYPE_CHECKING:
    import numpy as np


# Caminho para som
SOUND_DIR: Path = Path(__file__).resolve().parent / "sound" / "alarm.mp3"


def run_face_mesh() -> None:

    if not setup_pygame(str(SOUND_DIR)):
        return

    # Configuração da webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1000)
    cap.set(4, 1000)

    # Inicializando detecção
    detector = FaceMeshDetector(
        min_detection_confidence=0.7,
        min_track_confidence=0.7
    )

    # Variaveis de estado
    start_time: None | float = None
    alarm_status: bool = False

    while True:
        success, img = cap.read()

        if not success:
            print("Erro na câmera")
            break

        # Tirar efeito espelho
        img: np.ndarray = cv2.flip(img, 1)

        # Iniciando detecção
        img, faces = detector.find_face_mesh(img, draw=True)

        if len(faces) > 0:
            face = faces[0]

            # Calcular EAR individualmente
            left_ear = detector.get_ear(face, detector.LEFT_EYE_INDICES)
            right_ear = detector.get_ear(face, detector.RIGHT_EYE_INDICES)

            # Calcula média
            average_ear = (left_ear + right_ear) / 2.0

            start_time, alarm_status, color = process_drowsiness_logic(
                img,
                average_ear,
                start_time,
                alarm_status=alarm_status
            )

            # Mostra valor EAR na tela
            cv2.putText(
                img,
                f"EAR: {average_ear:.2f}",
                (300, 70),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                color,
                3
            )

        cv2.imshow("image", img)

        # Aperte 'q' para sair
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.quit()  # Fecha o mixer corretamente ao sair
    print("FIM DO PROGRAMA")


if __name__ == "__main__":
    run_face_mesh()
