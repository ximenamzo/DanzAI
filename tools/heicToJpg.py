import os
import pyheif
from PIL import Image

# Definir las carpetas de origen y destino
source_folder = '/home/xime/PycharmProjects/DanzAI/images/Contempo'
destination_folder = '/home/xime/PycharmProjects/DanzAI/images/analisis'

# Crear la carpeta de destino si no existe
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Función para convertir y guardar imágenes en formato JPG
def convert_heic_to_jpg(source_path, destination_path):
    # Leer el archivo HEIC
    heif_file = pyheif.read(source_path)
    # Convertirlo a una imagen PIL
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride
    )
    # Guardar la imagen en formato JPG
    image.save(destination_path, "JPEG")

# Recorrer todas las imágenes en la carpeta de origen
for filename in os.listdir(source_folder):
    if filename.lower().endswith('.heic'):
        source_path = os.path.join(source_folder, filename)
        # Crear el nombre de archivo .jpg
        new_filename = os.path.splitext(filename)[0] + ".jpg"
        destination_path = os.path.join(destination_folder, new_filename)
        # Convertir y guardar la imagen
        convert_heic_to_jpg(source_path, destination_path)

print("Conversión completada.")
