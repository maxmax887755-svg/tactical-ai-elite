import numpy as np

def predecir_jugada(
    balon,
    azules,
    rojos
):

    if not balon:
        return "Sin balon"

    bx,by = balon

    cerca_azul = 0
    cerca_rojo = 0

    for x,y in azules:

        d = np.linalg.norm(
            np.array([x,y]) -
            np.array([bx,by])
        )

        if d < 150:
            cerca_azul += 1

    for x,y in rojos:

        d = np.linalg.norm(
            np.array([x,y]) -
            np.array([bx,by])
        )

        if d < 150:
            cerca_rojo += 1

    if cerca_azul >= 3:
        return "Azul ataca"

    if cerca_rojo >= 3:
        return "Rojo ataca"

    return "Juego equilibrado"