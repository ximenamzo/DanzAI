from danzai_data import *
from danzai_functions import *


# Dibujado con color personalizado
def draw_custom_connections(image, landmarks, connections):
    for connection, color in connections:
        start_idx, end_idx = connection
        if start_idx < len(landmarks) and end_idx < len(landmarks):
            cv2.line(image, landmarks[start_idx], landmarks[end_idx], color, 3)


# Dibujado de líneas
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

        # Ángulos - Cálculo
        axila_der = calculate_angle(lm[CODO_DER.value],lm[HOMBRO_DER.value],lm[CADERA_DER.value])

        #Dibujo para cuello
        draw_neck_line(img, lm, HOMBRO_IZQ.value, HOMBRO_DER.value, BOCA_IZQ.value, BOCA_DER.value, (255, 0, 255), 3)

        # Dibujo para ingles
        draw_center_line(img, lm, CADERA_IZQ.value, CADERA_DER.value, RODILLA_IZQ.value, (255, 50, 50), 3)
        draw_center_line(img, lm, CADERA_IZQ.value, CADERA_DER.value, RODILLA_DER.value, (50, 50, 255), 3)

        # Ángulos - Salida en terminal
        print(f"Ángulo de la axila derecha: {axila_der:.2f} grados")

        # Escribe los ángulos en la imagen
        cv2.putText(img, str(round(axila_der, 2)), lm[HOMBRO_DER.value], cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()


image_path = 'images/pose/primera_posicion.png'
process_image(image_path)
