import cv2
import mediapipe as mp

# Inicializa MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializa MediaPipe Drawing para dibujar las posturas.
mp_drawing = mp.solutions.drawing_utils

# Abre el archivo de video.
video_path = 'ruta/a/tu/video.mp4'  # Cambia esto por la ruta a tu video.
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Fin del video o error al leer el archivo.")
        break

    # Convierte la imagen capturada a RGB.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Realiza la detección.
    image.flags.writeable = False
    results = pose.process(image)

    # Dibuja las anotaciones en la imagen.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Muestra la imagen.
    cv2.imshow('MediaPipe Pose', image)

    # Presiona 'q' para salir del loop.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
