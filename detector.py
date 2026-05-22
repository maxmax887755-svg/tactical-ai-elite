

import cv2

from xg import prob_gol_tras_pase

from predicciones import (
    predecir_siguiente_pase,
    detectar_contraataque
)

ultimo_balon = (250, 200)

def hex_to_bgr(hex_color):

    hex_color = hex_color.lstrip('#')

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (b, g, r)

def analizar_frame(
    frame,
    color1,
    color2
):

    global ultimo_balon

    eventos = {

        "gol_azul": False,

        "gol_rojo": False,

        "posesion_azul": 50,

        "xg_pass": 0,

        "next_pass": None,

        "counter_attack": False
    }

    bgr1 = hex_to_bgr(color1)
    bgr2 = hex_to_bgr(color2)

    balon = (300, 200)

    azules = [
        (100,100),
        (150,140),
        (200,180)
    ]

    rojos = [
        (400,300),
        (420,320),
        (440,360)
    ]

    for x, y in azules:

        cv2.circle(
            frame,
            (x, y),
            10,
            bgr1,
            -1
        )

    for x, y in rojos:

        cv2.circle(
            frame,
            (x, y),
            10,
            bgr2,
            -1
        )

    cv2.circle(
        frame,
        balon,
        7,
        (255,255,255),
        -1
    )

    eventos["xg_pass"] = prob_gol_tras_pase(
        "danger_pass",
        balon[0],
        balon[1],
        640,
        480
    )

    eventos["next_pass"] = predecir_siguiente_pase(
        balon,
        azules,
        640
    )

    contra = detectar_contraataque(
        balon,
        ultimo_balon,
        640
    )

    eventos["counter_attack"] = contra

    ultimo_balon = balon

    if balon[0] > 600:
        eventos["gol_azul"] = True

    if balon[0] < 50:
        eventos["gol_rojo"] = True

    return frame, eventos