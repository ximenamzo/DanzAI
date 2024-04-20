#falta el turn out / rotacion
# variasbles temporales con los nombres... if secuencia de poses, entonces es un paso

import mediapipe as mp
import cv2
from matplotlib import pyplot as plt

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

point = mp_pose.PoseLandmark

NARIZ = point.NOSE
OJO_IZQ_INT = point.LEFT_EYE_INNER
OJO_IZQ = point.LEFT_EYE
OJO_IZQ_EXT = point.LEFT_EYE_OUTER
OJO_DER_INT = point.RIGHT_EYE_INNER
OJO_DER = point.RIGHT_EYE
OJO_DER_EXT = point.RIGHT_EYE_OUTER
OREJA_IZQ = point.LEFT_EAR
OREJA_DER = point.RIGHT_EAR
BOCA_IZQ = point.MOUTH_LEFT
BOCA_DER = point.MOUTH_RIGHT

HOMBRO_IZQ = point.LEFT_SHOULDER
HOMBRO_DER = point.RIGHT_SHOULDER
CODO_IZQ = point.LEFT_ELBOW
CODO_DER = point.RIGHT_ELBOW
MUNECA_IZQ = point.LEFT_WRIST
MUNECA_DER = point.RIGHT_WRIST
MENIQUE_IZQ = point.LEFT_PINKY
MENIQUE_DER = point.RIGHT_PINKY
INDICE_IZQ = point.LEFT_INDEX
INDICE_DER = point.RIGHT_INDEX
PULGAR_IZQ = point.LEFT_THUMB
PULGAR_DER = point.RIGHT_THUMB

CADERA_IZQ = point.LEFT_HIP
CADERA_DER = point.RIGHT_HIP
RODILLA_IZQ = point.LEFT_KNEE
RODILLA_DER = point.RIGHT_KNEE
TOBILLO_IZQ = point.LEFT_ANKLE
TOBILLO_DER = point.RIGHT_ANKLE
TALON_IZQ = point.LEFT_HEEL
TALON_DER = point.RIGHT_HEEL
PUNTA_PIE_IZQ = point.LEFT_FOOT_INDEX
PUNTA_PIE_DER = point.RIGHT_FOOT_INDEX

# BGR
morado = (255, 0, 255)
rojo = (0, 0, 255)
amarillo = (0, 255, 255)
naranja = (0, 165, 255)
azul = (255, 0, 0)
cian = (255, 255, 0)
verde = (0, 255, 0)

custom_connections = [
    ((NARIZ.value, OJO_IZQ_INT.value), morado),  # 0-1 / Morado
    ((OJO_IZQ_INT.value, OJO_IZQ.value), morado),  # 1-2 / Morado
    ((OJO_IZQ.value, OJO_IZQ_EXT.value), morado),  # 2-3 / Morado
    ((OJO_IZQ_EXT.value, OREJA_IZQ.value), morado),  # 3-7 / Morado
    ((NARIZ.value, OJO_DER_INT.value), morado),  # 0-4 / Morado
    ((OJO_DER_INT.value, OJO_DER.value), morado),  # 4-5 / Morado
    ((OJO_DER.value, OJO_DER_EXT.value), morado),  # 5-6 / Morado
    ((OJO_DER_EXT.value, OREJA_DER.value), morado),  # 6-8 / Morado
    ((BOCA_IZQ.value, BOCA_DER.value), morado),  # 9-10 / Morado

    ((HOMBRO_IZQ.value, HOMBRO_DER.value), morado),  # 11-12 / Morado
    ((HOMBRO_IZQ.value, CADERA_IZQ.value), morado),  # 11-23 / Morado
    ((HOMBRO_DER.value, CADERA_DER.value), morado),  # 12-24 / Morado
    ((CADERA_IZQ.value, CADERA_DER.value), morado),  # 23-24 / Morado

    ((HOMBRO_DER.value, CODO_DER.value), rojo),  # 12-14 / Rojo
    ((CADERA_DER.value, RODILLA_DER.value), rojo),  # 24-26 / Rojo

    ((CODO_DER.value, MUNECA_DER.value), amarillo),  # 14-16 / Amarillo
    ((RODILLA_DER.value, TOBILLO_DER.value), amarillo),  # 26-28 / Amarillo

    ((MUNECA_DER.value, MENIQUE_DER.value), naranja),  # 16-18 / Naranja
    ((MUNECA_DER.value, INDICE_DER.value), naranja),  # 16-20 / Naranja
    ((MUNECA_DER.value, PULGAR_DER.value), naranja),  # 16-22 / Naranja
    ((MENIQUE_DER.value, INDICE_DER.value), naranja),  # 18-20 / Naranja
    ((TOBILLO_DER.value, TALON_DER.value), naranja),  # 28-30 / Naranja
    ((TOBILLO_DER.value, PUNTA_PIE_DER.value), naranja),  # 28-32 / Naranja
    ((TALON_DER.value, PUNTA_PIE_DER.value), naranja),  # 30-32 / Naranja

    ((HOMBRO_IZQ.value, CODO_IZQ.value), azul),  # 11-13 / Azul
    ((CADERA_IZQ.value, RODILLA_IZQ.value), azul),  # 23-25 / Azul

    ((CODO_IZQ.value, MUNECA_IZQ.value), cian),  # 13-15 / Cian
    ((RODILLA_IZQ.value, TOBILLO_IZQ.value), cian),  # 25-27 / Cian

    ((MUNECA_IZQ.value, MENIQUE_IZQ.value), verde),  # 15-17 / Verde
    ((MUNECA_IZQ.value, INDICE_IZQ.value), verde),  # 15-19 / Verde
    ((MUNECA_IZQ.value, PULGAR_IZQ.value), verde),  # 15-21 / Verde
    ((MENIQUE_IZQ.value, INDICE_IZQ.value), verde),  # 17-19 / Verde
    ((TOBILLO_IZQ.value, TALON_IZQ.value), verde),  # 27-29 / Verde
    ((TOBILLO_IZQ.value, PUNTA_PIE_IZQ.value), verde),  # 27-31 / Verde
    ((TALON_IZQ.value, PUNTA_PIE_IZQ.value), verde),  # 29-31 / Verde
]