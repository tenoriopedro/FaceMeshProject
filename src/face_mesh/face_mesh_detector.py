import math
from typing import Any

import cv2
import mediapipe as mp
import numpy as np


class FaceMeshDetector:

    def __init__(
            self,
            *,
            static_mode: bool = False,
            max_faces: int = 1,
            refine_landmarks: bool = True,
            min_detection_confidence: float = 0.5,
            min_track_confidence: float = 0.5,
    ) -> None:

        self.static_mode = static_mode
        self.max_faces = max_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_track_confidence = min_track_confidence

        # Iniciando Media Pipe
        self.mp_draw: Any = mp.solutions.drawing_utils  # type: ignore
        self.mp_face_mesh: Any = mp.solutions.face_mesh  # type: ignore

        # Configuração da Malha
        # refine_landmarks=True, dá mais precisão nos olhos e lábios
        self.face_mesh: Any = self.mp_face_mesh.FaceMesh(
            self.static_mode,
            self.max_faces,
            self.refine_landmarks,
            self.min_detection_confidence,
            self.min_track_confidence
        )

        # Configuração do desenho no video
        self.draw_spec: Any = self.mp_draw.DrawingSpec(
            thickness=1, circle_radius=0, color=(0, 255, 0)
        )

        # Olho ESQUERDO
        self.LEFT_EYE_INDICES: dict[str, tuple[int, int]] = {
            "horizontal": (33, 133),
            "vertical_1": (160, 144),
            "vertical_2": (158, 153),
        }

        # Olho DIREITO
        self.RIGHT_EYE_INDICES: dict[str, tuple[int, int]] = {
            "horizontal": (362, 263),
            "vertical_1": (385, 373),
            "vertical_2": (387, 374)
        }

    def find_face_mesh(
            self, img: np.ndarray, *, draw: bool = True
    ) -> tuple[np.ndarray, list[list[list[int]]]]:

        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Processo de detecção
        self.results: Any = self.face_mesh.process(self.img_rgb)

        # Para mais de um objeto(rosto) detectado
        faces: list[list[list[int]]] = []

        # Desenhar malha (caso encontre algo)
        if self.results.multi_face_landmarks:

            for face_landmarks in self.results.multi_face_landmarks:

                if draw:
                    self.mp_draw.draw_landmarks(
                        img,
                        face_landmarks,
                        self.mp_face_mesh.FACEMESH_CONTOURS,
                        self.draw_spec, self.draw_spec
                    )

                image_height, image_witdh, _ = img.shape

                # rosto detectado individualmente
                face: list[list[int]] = []
                for landmarks in face_landmarks.landmark:

                    x, y = (
                        int(landmarks.x * image_witdh),
                        int(landmarks.y * image_height)
                    )

                    face.append([x, y])

                faces.append(face)

        return img, faces

    def calculate_distance(
            self, point1: list[int], point2: list[int]
    ) -> float:
        x1, y1 = point1
        x2, y2 = point2
        return math.hypot(x2 - x1, y2 - y1)

    def get_ear(
            self, face: list[list[int]],
            eye_indices: dict[str, tuple[int, int]]
    ) -> float:
        # desempacota os indices do dicionário
        left_horizontal_pont, \
            right_horizontal_point = eye_indices["horizontal"]
        top_vert1_point, bottom_vert1_point = eye_indices["vertical_1"]
        top_vert2_point, bottom_vert2_point = eye_indices["vertical_2"]

        # Calcula distâncias
        horizontal_distance = self.calculate_distance(
            face[left_horizontal_pont],
            face[right_horizontal_point]
        )
        vert1_distance = self.calculate_distance(
            face[top_vert1_point],
            face[bottom_vert1_point]
        )
        vert2_distance = self.calculate_distance(
            face[top_vert2_point],
            face[bottom_vert2_point]
        )

        # Evita divisão por zero
        if horizontal_distance == 0:
            return 0

        # Calcula EAR(EYE ASPECT RATIO)
        return (
            (vert1_distance + vert2_distance) / (2.0 * horizontal_distance)
        )
