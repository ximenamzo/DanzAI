import cv2
from tkinter import *
from PIL import Image, ImageTk
import os

# Función para capturar y guardar fotos
def capturar_foto():
    frame = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    # Asegurarse de que el directorio existe
    if not os.path.exists('~/Pictures/myapp/'):
        os.makedirs('~/Pictures/myapp/')
    img.save(os.path.expanduser('~/Pictures/myapp/img_{}.png'.format(count[0])))
    count[0] += 1
    label_info.config(text="Foto capturada: {}".format(count[0]))

# Función para actualizar la imagen de la cámara en la interfaz
def video_stream():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cvimg)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, video_stream)

# Configuración inicial de la cámara
cap = cv2.VideoCapture(0)

# Configuración de la ventana principal
root = Tk()
root.title("App de Cámara")
root.configure(background='#000080')  # Azul marino

# Contador de imágenes capturadas
count = [0]

# Configuración de la etiqueta de video
lmain = Label(root, bd=10, relief=SUNKEN)
lmain.pack(padx=10, pady=10)

# Configuración del botón de captura
btn_capturar = Button(root, text="Capturar", command=capturar_foto, bg='red', fg='white')
btn_capturar.configure(width=10, height=2, font=("Calibri", 20, "bold"), relief=RAISED)
btn_capturar.pack(pady=10)

# Configuración del texto bajo el botón
label_info = Label(root, text="Haz click para empezar a capturar", font=("Calibri", 14), bg='#000080', fg='white')
label_info.pack()

# Iniciar la transmisión de video
video_stream()

# Mantener la ventana abierta
root.mainloop()

# Liberar la cámara al cerrar la aplicación
cap.release()
cv2.destroyAllWindows()
