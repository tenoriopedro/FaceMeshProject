import cv2
import mediapipe as mp
import time
import math


class FaceMeshDetector():

    def __init__(
            self,
            static_mode=False,
            max_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_track_confidence=0.5,
    ):

        self.static_mode = static_mode
        self.max_faces = max_faces
        self.refine_landmarks = refine_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_track_confidence = min_track_confidence

        # Iniciando Media Pipe
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_face_mesh = mp.solutions.face_mesh

        # Configuração da Malha
        # refine_landmarks=True, dá mais precisão nos olhos e lábios
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            self.static_mode,
            self.max_faces,
            self.refine_landmarks,
            self.min_detection_confidence,
            self.min_track_confidence
        )

        # Configuração do desenho no video
        self.draw_spec = self.mp_draw.DrawingSpec(
            thickness=1, circle_radius=0, color=(0, 255, 0)
        )

        # Olho ESQUERDO
        self.LEFT_EYE_INDICES = {
            'horizontal': (33, 133),
            'vertical_1': (160, 144),
            'vertical_2': (158, 153),
        }

        # Olho DIREITO
        self.RIGHT_EYE_INDICES = {
            'horizontal': (362, 263),
            'vertical_1': (385, 373),
            'vertical_2': (387, 374)
        }

    def find_face_mesh(self, img, draw):

        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Processo de detecção
        self.results = self.face_mesh.process(self.img_rgb)

        # Para mais de um objeto(rosto) detectado
        faces = []

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

                image_height, image_witdh, image_channels = img.shape

                # rosto detectado individualmente
                face = []
                for landmarks in face_landmarks.landmark:

                    x, y = (
                        int(landmarks.x * image_witdh),
                        int(landmarks.y * image_height)
                    )

                    face.append([x, y])

                faces.append(face)

        return img, faces

    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.hypot(x2 - x1, y2 - y1)

    def get_ear(self, face, eye_indices):
        # desempacota os indices do dicionário
        left_horizontal_pont, \
            right_horizontal_point = eye_indices['horizontal']
        top_vert1_point, bottom_vert1_point = eye_indices['vertical_1']
        top_vert2_point, bottom_vert2_point = eye_indices['vertical_2']

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
        ear = (vert1_distance + vert2_distance) / (2.0 * horizontal_distance)
        return ear


def main():

    # Selecionar webcam
    cap = cv2.VideoCapture(0)

    # Configuração
    cap.set(3, 1000)
    cap.set(4, 1000)

    # Configurações de sono
    EAR_THRESHOLD = 0.20   # Abaixo desse valor, o olho está fechado
    MAX_TIME = 1.5         # Segundos permitidos de olho fechado

    # Variáveis de Controle
    start_time = None
    alarm_status = False

    # Inicializando detecção
    detector = FaceMeshDetector(
        min_detection_confidence=0.7,
        min_track_confidence=0.7
    )

    while True:
        success, img = cap.read()

        if not success:
            print("Erro na câmera")
            break

        # Tirar efeito espelho
        img = cv2.flip(img, 1)

        img, faces = detector.find_face_mesh(img, draw=False)

        if len(faces) > 0:
            face = faces[0]

            # Calcular EAR individualmente
            left_ear = detector.get_ear(face, detector.LEFT_EYE_INDICES)
            right_ear = detector.get_ear(face, detector.RIGHT_EYE_INDICES)

            # Calcula média
            average_ear = (left_ear + right_ear) / 2.0

            # Vermelho = True / Verde = False
            cor = (0, 0, 255) if alarm_status else (0, 255, 0)

            # LIMIAR DE SONO
            if average_ear < EAR_THRESHOLD:

                if start_time is None:
                    start_time = time.time()  # Inicia o cronômetro

                current_time = time.time() - start_time

                # Mostra cronômetro na tela(DEBUG)
                cv2.putText(
                    img,
                    f'Tempo: {current_time:.2f}s',
                    (5, 70),
                    cv2.FONT_HERSHEY_PLAIN,
                    2,
                    cor,
                    2
                )

                # Trigger
                if current_time >= MAX_TIME:
                    alarm_status = True

                    cv2.putText(
                        img,
                        "ACORDA!!!!",
                        (20, 150),
                        cv2.FONT_HERSHEY_PLAIN,
                        4,
                        cor,
                        4
                    )
                    print("DORMIU", left_ear)

            else:
                start_time = None
                alarm_status = False

            # Mostra valor EAR na tela
            cv2.putText(
                img,
                f'EAR: {average_ear:.2f}',
                (300, 70),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                cor,
                3
            )

        cv2.imshow("image", img)

        # Aperte 'q' para sair
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("FIM DO PROGRAMA")


if __name__ == "__main__":
    main()
