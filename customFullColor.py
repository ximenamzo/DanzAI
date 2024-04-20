import mediapipe as mp
import cv2, math
from matplotlib import pyplot as plt
from db import *

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def draw_custom_connections(image, landmarks, connections):
    for connection, color in connections:
        start_idx, end_idx = connection
        if start_idx < len(landmarks) and end_idx < len(landmarks):
            cv2.line(image, landmarks[start_idx], landmarks[end_idx], color, 5)


def draw_center_line(img, landmarks, hip_left, hip_right, knee, color, thickness=5):
    # Calcula el punto medio de la cadera
    hip_center = ((landmarks[hip_left][0] + landmarks[hip_right][0]) // 2,
                  (landmarks[hip_left][1] + landmarks[hip_right][1]) // 2)

    # Dibuja una línea desde el punto medio de la cadera hasta la rodilla
    cv2.line(img, hip_center, landmarks[knee], color, thickness)


# Función para calcular los ángulos
def calculate_angle(point1, point2, point3):
    # Extracción de coordenadas
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Calculo de longitudes de los lados del triángulo
    a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    b = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    c = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)

    # Ley de Coseno
    angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    # Conversión a grados
    angle = math.degrees(angle)
    return angle


def process_image(img_path):
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # Extracción de coordenadas de landmarks
        # lm = landmarks
        lm = [(int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]))
                     for landmark in results.pose_landmarks.landmark]
        draw_custom_connections(img, lm, custom_connections)
        right_armpit_angle = calculate_angle(lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                             lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                             lm[mp_pose.PoseLandmark.RIGHT_HIP.value])

        # Salida en terminal
        print(f"Ángulo de la axila derecha: {right_armpit_angle:.2f} grados")

        # Configura los parámetros para el texto
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 0, 0)  # Color negro
        thickness = 2

        # Escribe los ángulos en la imagen
        cv2.putText(img, str(round(right_armpit_angle, 2)), lm[HOMBRO_DER.value], font, font_scale, color, thickness)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


image_path = 'images/segunda_posicionn.png'
process_image(image_path)
