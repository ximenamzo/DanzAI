import os
import pyheif
from PIL import Image

# Definir las carpetas de origen y destino
source_folder = '/home/xime/PycharmProjects/DanzAI/images/analisis/paoCopy'
destination_folder = '/home/xime/PycharmProjects/DanzAI/images/analisis/0'

# Crear la carpeta de destino si no existe
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)


# Función para convertir diferentes formatos de imagen a JPG
def convert_to_jpg(source_path, destination_path):
    try:
        # Detectar el tipo de archivo y abrir la imagen según el formato
        file_extension = os.path.splitext(source_path)[1].lower()

        if file_extension in ['.png', '.jpeg', '.bmp', '.tiff', '.gif']:
            image = Image.open(source_path)
        elif file_extension == '.heic':
            heif_file = pyheif.read(source_path)
            image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride
            )
        elif file_extension == '.jpg':
            # Si ya es JPG, solo copiar a la carpeta destino
            image = Image.open(source_path)

        # Convertir la imagen a formato JPG y guardar
        if image is not None:
            image = image.convert("RGB")  # Asegurarse de convertir a RGB
            image.save(destination_path, "JPEG")
            print(f"Convertido: {destination_path}")
        else:
            print(f"Archivo no soportado: {source_path}")

    except Exception as e:
        print(f"Error al convertir {source_path}: {e}")


# Recorrer todas las imágenes en la carpeta de origen
for filename in os.listdir(source_folder):
    source_path = os.path.join(source_folder, filename)
    destination_path = os.path.join(destination_folder, os.path.splitext(filename)[0] + ".jpg")

    # Si el archivo no es un directorio, intentar la conversión
    if not os.path.isdir(source_path):
        convert_to_jpg(source_path, destination_path)

print("Conversión completada.")
