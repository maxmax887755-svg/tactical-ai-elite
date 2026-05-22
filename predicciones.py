import numpy as np

def predecir_siguiente_pase(
    balon,
    jugadores,
    porteria_x
):

    if not balon:
        return None

    bx, by = balon

    best = None
    best_score = -999

    for i, (x, y) in enumerate(jugadores):

        dist = np.linalg.norm([
            bx - x,
            by - y
        ])

        progreso = x / porteria_x

        score = (
            (1 / (dist + 1))
            + progreso
        )

        if score > best_score:

            best_score = score
            best = i

    return best


def detectar_contraataque(
    balon_actual,
    balon_anterior,
    ancho
):

    if not balon_actual or not balon_anterior:
        return False

    x1, y1 = balon_anterior
    x2, y2 = balon_actual

    avance = x2 - x1

    if avance > ancho * 0.15:
        return True

    return False