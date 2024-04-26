from danzai_functions import *
import matplotlib.pyplot as plt


# Dibujado de líneas
def process_image(img_paths):
    n_imgs = len(img_paths)
    fig, axs = plt.subplots(1, n_imgs, figsize=(5 * n_imgs, 5))

    for idx, img_path in enumerate(img_paths):
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error cargando la imagen: {img_path}")
            continue
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)

        if results.pose_landmarks:
            # Extracción de coordenadas de landmarks
            # lm = landmarks
            lm = [(int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]))
                  for landmark in results.pose_landmarks.landmark]
            draw_custom_connections(img, lm, custom_connections)

            angles = get_angles(lm)

            print(f"\n {img_path}")
            # Ángulos - Salida en terminal y Escritura en imagen
            for angle_name, angle_value in angles.items():
                position = lm[joints[angle_name]]  # Asegúrate de que joints[angle_name] es un índice y no una cadena
                print(f"{angle_name.replace('_', ' ').title()}: {angle_value:.2f} grados. Coordenadas{position}")
                cv2.putText(img, f"{angle_value:.2f}", position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        axs[idx].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axs[idx].axis('off')
        axs[idx].set_title(f'Imagen {idx + 1}')

    plt.show()


image_paths = ['images/pao/primera_perfil.JPG',
               'images/pao/primera_frente.JPG',
               'images/pao/primera_frente_incorrecta.JPG']
process_image(image_paths)
