from danzai_functions import *
import cv2
import sqlite3

def create_connection():
    return sqlite3.connect('danzai.db')

def find_pose(angles):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
        SELECT pose, side, variation FROM posturas
        WHERE (min_left_armpit <= ? AND left_armpit >= ?)
          AND (min_right_armpit <= ? AND right_armpit >= ?)
          AND (min_left_elbow <= ? AND left_elbow >= ?)
          AND (min_right_elbow <= ? AND right_elbow >= ?)
          AND (min_left_wrist <= ? AND left_wrist >= ?)
          AND (min_right_wrist <= ? AND right_wrist >= ?)
          AND (min_left_hip <= ? AND left_hip >= ?)
          AND (min_right_hip <= ? AND right_hip >= ?)
          AND (min_left_knee <= ? AND left_knee >= ?)
          AND (min_right_knee <= ? AND right_knee >= ?)
          AND (min_left_foot <= ? AND left_foot >= ?)
          AND (min_right_foot <= ? AND right_foot >= ?);
    """
    cursor.execute(query, (
        angles['axila_izq'], angles['axila_izq'],
        angles['axila_der'], angles['axila_der'],
        angles['codo_izq'], angles['codo_izq'],
        angles['codo_der'], angles['codo_der'],
        angles['muñeca_izq'], angles['muñeca_izq'],
        angles['muñeca_der'], angles['muñeca_der'],
        angles['ingle_izq'], angles['ingle_izq'],
        angles['ingle_der'], angles['ingle_der'],
        angles['rodilla_izq'], angles['rodilla_izq'],
        angles['rodilla_der'], angles['rodilla_der'],
        angles['empeine_izq'], angles['empeine_izq'],
        angles['empeine_der'], angles['empeine_der']
    ))
    result = cursor.fetchone()
    conn.close()
    return result

cap = cv2.VideoCapture(0)  # Abre la cámara de video

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Error al leer la cámara.")
        break

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        lm = [(int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0]))
              for landmark in results.pose_landmarks.landmark]
        angles = get_angles(lm)
        pose_info = find_pose(angles)
        if pose_info:
            pose_text = f"{pose_info[0]}_{pose_info[1]}_{pose_info[2]}"
            cv2.putText(image, pose_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(image, "Neutro", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Pose', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
