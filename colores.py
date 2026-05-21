import cv2
import numpy as np

def detectar_equipo(img):

    img = cv2.resize(img,(50,50))

    hsv = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2HSV
    )

    promedio = np.mean(
        hsv.reshape(-1,3),
        axis=0
    )

    h = promedio[0]

    if h < 20 or h > 160:
        return "Rojo"

    elif 90 < h < 140:
        return "Azul"

    return "Otro"