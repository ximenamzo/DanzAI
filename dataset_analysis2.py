import os
import cv2
from danzai_functions import *
from statistics import mean

def calculate_percentage_difference(correct, incorrect):
    if correct == 0:
        return 100 if incorrect != 0 else 0
    return abs((incorrect - correct) / correct) * 100

def process_images_from_folder(folder_path):
    angles_data = {}
    for image_name in os.listdir(folder_path):
        if image_name.endswith(".jpg"):
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
    base_path = '/home/xime/PycharmProjects/DanzAI/images/analisis'
    results = {}
    for i in range(6):
        folder_path = os.path.join(base_path, str(i))
        if os.path.exists(folder_path):
            angles_data = process_images_from_folder(folder_path)
            for pose_key, angles_dict in angles_data.items():
                if pose_key not in results:
                    results[pose_key] = angles_dict
                else:
                    for key in angles_dict:
                        results[pose_key][key].extend(angles_dict[key])

    pose_errors = {}
    for pose_key, angles_dict in results.items():
        if 'incorrecta' in pose_key:
            correct_key = pose_key.replace('incorrecta', 'correcta')
            if correct_key in results:
                pose_error = []
                errors = []
                print(f"\nPose: {correct_key.replace('_correcta', '')}")
                for key in results[correct_key]:
                    if key in results[pose_key]:
                        avg_correct = mean(results[correct_key][key])
                        avg_incorrect = mean(results[pose_key][key])
                        error = calculate_percentage_difference(avg_correct, avg_incorrect)
                        errors.append(error)
                        print(f"{key} error: {error:.2f}%")
                pose_error_average = mean(errors)
                pose_errors[correct_key] = pose_error_average
                print(f"Average error for {correct_key.replace('_correcta', '')}: {pose_error_average:.2f}%")

    if pose_errors:
        general_error = mean(pose_errors.values())
        print(f"\nGeneral percentage of error across all poses: {general_error:.2f}%")

if __name__ == "__main__":
    main()
