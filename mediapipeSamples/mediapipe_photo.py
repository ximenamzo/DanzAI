import cv2
import mediapipe as mp
from screeninfo import get_monitors

# Initialize MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, model_complexity=2)

# Picking an image
image_path = '../images/pose/cou_de_pied.png'
image = cv2.imread(image_path)

# Convert to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process the image
results = pose.process(image_rgb)

# Draw landmarks
annotated_image = image.copy()
mp_drawing = mp.solutions.drawing_utils
if results.pose_landmarks:
    mp_drawing.draw_landmarks(
        image=annotated_image,
        landmark_list=results.pose_landmarks,
        connections=mp_pose.POSE_CONNECTIONS)

# Obtain screen dimensions
monitor = get_monitors()[0]
width = int(monitor.width * 3 / 5)
height = int(monitor.height * 3 / 5)

# Create and position the window
cv2.namedWindow('Pose Detection', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Pose Detection', width, height)
cv2.moveWindow('Pose Detection', (monitor.width - width) // 2, (monitor.height - height) // 2)

# Show the image
cv2.imshow('Pose Detection', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()