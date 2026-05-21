import cv2
import numpy as np

heatmap_global = np.zeros(
    (720,1280),
    dtype=np.float32
)

def actualizar_heatmap(posiciones):

    global heatmap_global

    for x,y in posiciones:

        cv2.circle(
            heatmap_global,
            (x,y),
            30,
            1,
            -1
        )

def obtener_heatmap():

    global heatmap_global

    mapa = cv2.normalize(
        heatmap_global,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    mapa = mapa.astype(np.uint8)

    mapa = cv2.applyColorMap(
        mapa,
        cv2.COLORMAP_JET
    )

    return mapa