import os
from danzai_functions import *
from statistics import mean, stdev


# Calcular el porcentaje de diferencia
def calculate_percentage_difference(correct, incorrect):
    # Evitar división por cero y calcular diferencia porcentual
    if correct == 0:
        return 0
    return abs(correct - incorrect) / correct * 100

def process_images_from_folder(folder_path):
    # Diccionario de los datos de los ángulos
    angles_data = {}

    # Lista todas las imágenes en cada carpeta
    for image_name in os.listdir(folder_path):
        # Procesa solo imágenes
        if image_name.endswith(".jpg"):

            # Excluye "correcta" o "incorrecta"
            pose_name = '_'.join(image_name.split('_')[:-1])
            correct = "correcta" in image_name

            image_path = os.path.join(folder_path, image_name)
            img = cv2.imread(image_path)

            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                results = pose.process(img_rgb)

                if results.pose_landmarks:
                    lm = [(int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]))
                          for landmark in results.pose_landmarks.landmark]

                    angles = get_angles(lm)

                    pose_key = f"{pose_name}_{'correcta' if correct else 'incorrecta'}"

                    if pose_key in angles_data:
                        for key, angle in angles.items():
                            angles_data[pose_key][key].append(angle)
                    else:
                        angles_data[pose_key] = {key: [angle] for key, angle in angles.items()}
    return angles_data


def main():
    # Donde están todas las carpetas
    base_path = '/home/xime/PycharmProjects/DanzAI/images/analisis'
    results = {}

    # 6 carpetas, una para cada bailarina
    for i in range(6):
        # Añade el número
        folder_path = os.path.join(base_path, str(i))

        if os.path.exists(folder_path):
            angles_data = process_images_from_folder(folder_path)
            for pose_key, angles_dict in angles_data.items():
                if pose_key not in results:
                    results[pose_key] = angles_dict
                else:
                    for key in angles_dict:
                        results[pose_key][key].extend(angles_dict[key])

    # Calcular el promedio y diferencia porcentual
    pose_differences = {}
    general_differences = []

    for pose_key, angles_dict in results.items():
        print(f"\nPose: {pose_key}")
        for key, angles in angles_dict.items():
            avg_angle = mean(angles)
            min_angle = min(angles)
            max_angle = max(angles)
            print(f"{key} average: {avg_angle:.2f}, min: {min_angle:.2f}, max: {max_angle:.2f}")
            if 'correcta' in pose_key:
                pose_differences[pose_key.replace('correcta', 'incorrecta')] = {}

    # Calcular diferencias entre correctas e incorrectas
    for pose_key, diffs in pose_differences.items():
        if pose_key in results and pose_key.replace('incorrecta', 'correcta') in results:
            correct_angles = results[pose_key.replace('incorrecta', 'correcta')]
            incorrect_angles = results[pose_key]
            for key in correct_angles:
                if key in incorrect_angles:
                    avg_correct = mean(correct_angles[key])
                    avg_incorrect = mean(incorrect_angles[key])
                    difference = calculate_percentage_difference(avg_correct, avg_incorrect)
                    pose_differences[pose_key][key] = difference
                    general_differences.append(difference)
                    print(f"Difference for {key} in {pose_key}: {difference:.2f}%")

    if general_differences:
        general_error = mean(general_differences)
        print(f"\nGeneral percentage of error across all poses: {general_error:.2f}%")


if __name__ == "__main__":
    main()
