import mediapipe as mp
import cv2
from matplotlib import pyplot as plt

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

right_side_connections = [
    (mp_pose.PoseLandmark.RIGHT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_ELBOW.value),
    (mp_pose.PoseLandmark.RIGHT_ELBOW.value, mp_pose.PoseLandmark.RIGHT_WRIST.value),
    (mp_pose.PoseLandmark.RIGHT_HIP.value, mp_pose.PoseLandmark.RIGHT_KNEE.value),
    (mp_pose.PoseLandmark.RIGHT_KNEE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value)
]

left_side_connections = [
    (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_ELBOW.value),
    (mp_pose.PoseLandmark.LEFT_ELBOW.value, mp_pose.PoseLandmark.LEFT_WRIST.value),
    (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value),
    (mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.LEFT_ANKLE.value)
]


def draw_custom_connections(image, landmarks, connections, color):
    for connection in connections:
        start_idx, end_idx = connection
        if start_idx < len(landmarks) and end_idx < len(landmarks):
            cv2.line(image, landmarks[start_idx], landmarks[end_idx], color, 5)


def process_image(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        landmarks = [(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]))
                     for landmark in results.pose_landmarks.landmark]

        draw_custom_connections(image, landmarks, right_side_connections, (255, 0, 0))  # Rojo para el lado derecho
        draw_custom_connections(image, landmarks, left_side_connections, (0, 0, 255))  # Azul para el lado izquierdo

    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


image_path = 'images/primera_posicionn.png'
process_image(image_path)
