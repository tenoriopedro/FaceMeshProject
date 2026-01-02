import cv2
import mediapipe as mp
import time


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

    def find_face_mesh(self, img, draw=True):

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

                # rosto detectado individualmente
                face = []
                for id, landmarks in enumerate(face_landmarks.landmark):

                    image_height, image_witdh, image_channels = img.shape

                    x, y = (
                        int(landmarks.x * image_witdh),
                        int(landmarks.y * image_height)
                    )

                    cv2.putText(
                        img,
                        str(id),
                        (x, y),
                        cv2.FONT_HERSHEY_PLAIN,
                        0.40,
                        (0, 255, 0),
                        0
                    )

                    face.append([x, y])

                faces.append(face)

        return img, faces


def main():

    # Selecionar webcam
    cap = cv2.VideoCapture(0)

    # Configuração
    cap.set(3, 1000)
    cap.set(4, 1000)

    previous_time = 0

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

        img, faces = detector.find_face_mesh(img)

        # if len(faces) != 0:
        #     print(faces[0])

        # Frame Rate
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time
        cv2.putText(
            img,
            f'FPS: {int(fps)}',
            (20, 70),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (0, 255, 0),
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
