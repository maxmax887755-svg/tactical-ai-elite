import numpy as np
from scipy.spatial.distance import pdist

def compactacion(jugadores):

    if len(jugadores) < 2:
        return 0

    return np.mean(
        pdist(jugadores)
    )

def presion(jugadores):

    p = 0

    for i in range(len(jugadores)):

        for j in range(i+1,len(jugadores)):

            d = np.linalg.norm(
                np.array(jugadores[i]) -
                np.array(jugadores[j])
            )

            if d < 100:
                p += 1

    return p

def analizar(azules,rojos):

    ca = compactacion(azules)
    cr = compactacion(rojos)

    pa = presion(azules)
    pr = presion(rojos)

    mensaje = ""

    if ca < cr:
        mensaje += "Azul compacto | "
    else:
        mensaje += "Rojo compacto | "

    if pa > pr:
        mensaje += "Azul presiona"
    else:
        mensaje += "Rojo presiona"

    return mensaje,pa,pr