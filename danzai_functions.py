import cv2
import math
from danzai_data import *


# Dibujado con color personalizado
def draw_custom_connections(img, lm, connections):
    for connection, color in connections:
        start_idx, end_idx = connection
        if start_idx < len(lm) and end_idx < len(lm):
            cv2.line(img, lm[start_idx], lm[end_idx], color, 3)

    # Dibujo para cuello
    draw_neck_line(img, lm, HOMBRO_IZQ.value, HOMBRO_DER.value, BOCA_IZQ.value, BOCA_DER.value, (255, 0, 255),
                   3)

    # Dibujo para ingles
    draw_center_line(img, lm, CADERA_IZQ.value, CADERA_DER.value, RODILLA_IZQ.value, (255, 50, 50), 3)
    draw_center_line(img, lm, CADERA_IZQ.value, CADERA_DER.value, RODILLA_DER.value, (50, 50, 255), 3)


# Punto medio
def midpoint(point1, point2):
    return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2


# Línea del cuello
def draw_neck_line(image, lm, mouth_left, mouth_right, shoulder_left, shoulder_right, color, thickness=2):
    # Calcula el punto medio entre los landmark de la boca
    mouth_center = midpoint(lm[mouth_left], lm[mouth_right])

    # Calcula el punto medio entre los landmark de los hombros
    shoulder_center = midpoint(lm[shoulder_left], lm[shoulder_right])

    # Dibuja una línea entre los puntos medios
    cv2.line(image, mouth_center, shoulder_center, color, thickness)


# Marcado en medio de las piernas
def draw_center_line(img, lm, hip_left, hip_right, knee, color, thickness=5):
    # Calcula el punto medio de la cadera
    hip_center = ((lm[hip_left][0] + lm[hip_right][0]) // 2,
                  (lm[hip_left][1] + lm[hip_right][1]) // 2)

    # Dibuja una línea desde el punto medio de la cadera hasta la rodilla
    cv2.line(img, hip_center, lm[knee], color, thickness)


# Función para calcular los ángulos
def calc_angle(point1, point2, point3):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Cálculo de longitudes de los lados del triángulo
    a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    b = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    c = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)

    # Ley de Coseno para calcular el ángulo
    cos_angle = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
    # Aseguramos que el valor esté en el rango válido para acos()
    cos_angle = max(-1.0, min(1.0, cos_angle))

    angle = math.acos(cos_angle)
    # Conversión a grados
    angle = math.degrees(angle)
    return angle


def get_angles(lm):
    angles = dict(axila_izq=calc_angle(lm[CODO_IZQ.value], lm[HOMBRO_IZQ.value], lm[CADERA_IZQ.value]),
                  axila_der=calc_angle(lm[CODO_DER.value], lm[HOMBRO_DER.value], lm[CADERA_DER.value]),
                  codo_izq=calc_angle(lm[HOMBRO_IZQ.value], lm[CODO_IZQ.value], lm[MUNECA_IZQ.value]),
                  codo_der=calc_angle(lm[HOMBRO_DER.value], lm[CODO_DER.value], lm[MUNECA_DER.value]),
                  muñeca_izq=calc_angle(lm[CODO_IZQ.value], lm[MUNECA_IZQ.value], lm[INDICE_IZQ.value]),
                  muñeca_der=calc_angle(lm[CODO_DER.value], lm[MUNECA_DER.value], lm[INDICE_DER.value]),
                  ingle_izq=calc_angle(lm[CADERA_DER.value], lm[CADERA_IZQ.value], lm[RODILLA_IZQ.value]),
                  ingle_der=calc_angle(lm[CADERA_IZQ.value], lm[CADERA_DER.value], lm[RODILLA_DER.value]),
                  rodilla_izq=calc_angle(lm[CADERA_IZQ.value], lm[RODILLA_IZQ.value], lm[TOBILLO_IZQ.value]),
                  rodilla_der=calc_angle(lm[CADERA_DER.value], lm[RODILLA_DER.value], lm[TOBILLO_DER.value]),
                  empeine_izq=calc_angle(lm[RODILLA_IZQ.value], lm[TOBILLO_IZQ.value], lm[PUNTA_PIE_IZQ.value]),
                  empeine_der=calc_angle(lm[RODILLA_DER.value], lm[TOBILLO_DER.value], lm[PUNTA_PIE_DER.value]))
    return angles


def calculate_similarity(angle_ideal, angle_observed, threshold=20):
    difference = abs(angle_ideal - angle_observed)
    return max(0, (1 - difference / threshold)) * 100


def calculate_percentage_difference(angle_ideal, angle_observed):
    difference = abs(angle_ideal - angle_observed)
    if angle_ideal == 0:  # Para evitar la división por cero
        return 100  # Máxima diferencia
    return (difference / angle_ideal) * 100