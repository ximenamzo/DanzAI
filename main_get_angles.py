from danzai_functions import *
import matplotlib.pyplot as plt
import cv2


def calculate_similarity(angle_ideal, angle_observed, threshold=20):
    difference = abs(angle_ideal - angle_observed)
    return max(0, (1 - difference / threshold)) * 100


def calculate_percentage_difference(angle_ideal, angle_observed):
    difference = abs(angle_ideal - angle_observed)
    if angle_ideal == 0:  # Para evitar la división por cero
        return 100  # Máxima diferencia
    return (difference / angle_ideal) * 100


def process_images(img_paths):
    if len(img_paths) != 2:
        print("Esta función espera exactamente dos rutas de imagen.")
        return

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    angle_data = []
    differences = []

    for idx, img_path in enumerate(img_paths):
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error cargando la imagen: {img_path}")
            continue
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        if results.pose_landmarks:
            lm = [(int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]))
                  for landmark in results.pose_landmarks.landmark]
            draw_custom_connections(img, lm, custom_connections)
            angles = get_angles(lm)
            angle_data.append(angles)

            print(f"\n {img_path}")
            for angle_name, angle_value in angles.items():
                position = lm[joints[angle_name]]
                print(f"{angle_name.replace('_', ' ').title()}: {angle_value:.2f} grados.")
                cv2.putText(img, f"{angle_value:.2f}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        axs[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axs[idx].axis('off')
        axs[idx].set_title(f'Imagen {idx + 1}')

    # Diferencia de ángulos
    if len(angle_data) == 2:
        print("\nDiferencias en porcentaje de los ángulos:")
        for angle in angle_data[0]:
            if angle in angle_data[1]:
                difference = calculate_percentage_difference(angle_data[0][angle], angle_data[1][angle])
                differences.append(difference)
                print(f"Diferencia en {angle.replace('_', ' ').title()}: {difference:.2f}%")

        if differences:
            max_difference = max(differences)
            min_difference = min(differences)
            avg_difference = sum(differences) / len(differences)
            print(f"\nDiferencia más alta: {max_difference:.2f}%")
            print(f"Diferencia más baja: {min_difference:.2f}%")
            print(f"Promedio de todas las diferencias: {avg_difference:.2f}%")

    plt.show()


# Lista de rutas a las imágenes
image_paths = ['images/pao/battement_derecha_segunda_frente.PNG',
               'images/pao/battement_derecha_segunda_frente_incorrecta.jpg']
process_images(image_paths)
