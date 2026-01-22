import time

import cv2
import numpy as np
import pygame

# Constantes de configuração
EAR_THRESHOLD: float = 0.20
MAX_TIME: float = 1.5
COLOR_RED: tuple[int, int, int] = (0, 0, 255)
COLOR_GREEN: tuple[int, int, int] = (0, 255, 0)


def setup_pygame(sound_file: str) -> bool:

    # Inicia Pygame (mixer de som)
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(sound_file)

    except pygame.error:
        print("ERRO CRÍTICO: Arquivo não encontrado.")
        return False

    else:
        return True


def process_drowsiness_logic(
        frame: np.ndarray,
        ear: float,
        start_time: None | float,
        *,
        alarm_status: bool,
) -> tuple[None | float, bool, tuple[int, int, int]]:

    if ear < EAR_THRESHOLD:
        if start_time is None:
            start_time = time.time()

        current_time = time.time() - start_time

        # Desenha cronômetro
        cv2.putText(
            frame,
            f"Tempo: {current_time:.2f}s",
            (5, 70),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            COLOR_RED,
            2,
        )

        # Dispara Alarme
        if current_time >= MAX_TIME:
            cv2.putText(
                frame,
                "ACORDA!!!!",
                (20, 150),
                cv2.FONT_HERSHEY_PLAIN,
                4,
                COLOR_RED,
                4,
            )

            if not alarm_status:
                pygame.mixer.music.play(-1)
                alarm_status = True

        return start_time, alarm_status, COLOR_RED

    # Acordado
    if alarm_status:
        pygame.mixer.music.stop()
        alarm_status = False

    return None, alarm_status, COLOR_GREEN
