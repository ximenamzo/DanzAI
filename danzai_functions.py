import cv2
import math


# Función para calcular los ángulos
def calculate_angle(point1, point2, point3):
    # Extracción de coordenadas
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    # Cálculo de longitudes de los lados del triángulo
    a = math.sqrt((x2 - x3) ** 2 + (y2 - y3) ** 2)
    b = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    c = math.sqrt((x1 - x3) ** 2 + (y1 - y3) ** 2)

    # Ley de Coseno
    angle = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
    # Conversión a grados
    angle = math.degrees(angle)
    return angle


# Punto medio
def midpoint(point1, point2):
    return (point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2


# Línea del cuello
def draw_neck_line(image, landmarks, mouth_left, mouth_right, shoulder_left, shoulder_right, color, thickness=2):
    # Calcula el punto medio entre los landmarks de la boca
    mouth_center = midpoint(landmarks[mouth_left], landmarks[mouth_right])

    # Calcula el punto medio entre los landmarks de los hombros
    shoulder_center = midpoint(landmarks[shoulder_left], landmarks[shoulder_right])

    # Dibuja una línea entre los puntos medios
    cv2.line(image, mouth_center, shoulder_center, color, thickness)


# Marcado en medio de las piernas
def draw_center_line(img, landmarks, hip_left, hip_right, knee, color, thickness=5):
    # Calcula el punto medio de la cadera
    hip_center = ((landmarks[hip_left][0] + landmarks[hip_right][0]) // 2,
                  (landmarks[hip_left][1] + landmarks[hip_right][1]) // 2)

    # Dibuja una línea desde el punto medio de la cadera hasta la rodilla
    cv2.line(img, hip_center, landmarks[knee], color, thickness)