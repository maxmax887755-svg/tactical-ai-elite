

import numpy as np

def prob_gol_tras_pase(
    tipo,
    x,
    y,
    ancho,
    alto
):

    distancia = np.sqrt(
        (ancho - x)**2
        +
        (alto/2 - y)**2
    )

    xg = max(
        0,
        1 - (distancia / 900)
    )

    if tipo == "key_pass":
        xg *= 1.8

    elif tipo == "danger_pass":
        xg *= 1.3

    else:
        xg *= 0.8

    return round(
        min(xg, 1),
        3
    )