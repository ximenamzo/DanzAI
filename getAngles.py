import mediapipe as mp
import cv2
from matplotlib import pyplot as plt

# Inicializa MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# Inicializa MediaPipe Drawing.
mp_drawing = mp.solutions.drawing_utils


def process_image(image_path):
    # Lee la imagen usando OpenCV.
    image = cv2.imread(image_path)
    # Convierte la imagen a RGB.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Procesa la imagen y detecta la pose.
    results = pose.process(image_rgb)

    # Dibuja las anotaciones en la imagen.
    annotated_image = image.copy()
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    # Muestra la imagen original y la anotada.
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
    plt.title('Image with Pose')

    plt.show()


# Ruta a tu imagen
image_path = 'ruta/a/tu/imagen.jpg'

# Procesa la imagen
process_image(image_path)
