import cv2
import mediapipe as mp
import time


# Selecionar webcam
cap = cv2.VideoCapture(0)

# Configuração
cap.set(3, 640)
cap.set(4, 480)

previous_time = 0

# Iniciando Media Pipe
mp_draw = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Configuração da Malha
# refine_landmarks=True, dá mais precisão nos olhos e lábios
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Configuração do desenho no video
draw_spec = mp_draw.DrawingSpec(
    thickness=1, circle_radius=1, color=(0, 255, 0)
)

while True:
    success, img = cap.read()

    if not success:
        print("Erro na câmera")
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Processo de detecção
    results = face_mesh.process(img_rgb)

    # Desenhar malha (caso encontre algo)
    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:
            mp_draw.draw_landmarks(
                img,
                face_landmarks,
                mp_face_mesh.FACEMESH_CONTOURS,
                draw_spec, draw_spec
            )

            for landmarks in face_landmarks.landmark:
                ...

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
