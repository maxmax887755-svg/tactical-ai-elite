import numpy as np

def calcular_xg(
    balon,
    ancho,
    alto
):

    if not balon:
        return 0

    bx,by = balon

    porteria_x = ancho
    porteria_y = alto // 2

    distancia = np.linalg.norm(
        np.array([bx,by]) -
        np.array([porteria_x,porteria_y])
    )

    xg = max(
        0,
        1 - (distancia / 1200)
    )

    return round(xg,2)