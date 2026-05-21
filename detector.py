import cv2
from ultralytics import YOLO

from colores import detectar_equipo
from formaciones import detectar_formacion
from predicciones import predecir_jugada
from xg import calcular_xg

model = YOLO("yolov8n.pt")

def analizar_frame(frame):

    results = model(frame)[0]

    azules = []
    rojos = []
    posiciones = []

    posesion_azul = 0
    posesion_rojo = 0

    balon = None

    for box in results.boxes:

        cls = int(box.cls[0])

        x1,y1,x2,y2 = map(
            int,
            box.xyxy[0]
        )

        # JUGADORES
        if cls == 0:

            cx = int((x1+x2)/2)
            cy = int((y1+y2)/2)

            posiciones.append((cx,cy))

            torso = frame[
                y1:y1+(y2-y1)//2,
                x1:x2
            ]

            if torso.size == 0:
                continue

            equipo = detectar_equipo(
                torso
            )

            if equipo == "Azul":

                azules.append((cx,cy))
                color = (255,0,0)

            elif equipo == "Rojo":

                rojos.append((cx,cy))
                color = (0,0,255)

            else:
                color = (0,255,0)

            cv2.rectangle(
                frame,
                (x1,y1),
                (x2,y2),
                color,
                2
            )

            cv2.putText(
                frame,
                equipo,
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )

        # BALON
        elif cls == 32:

            bx = int((x1+x2)/2)
            by = int((y1+y2)/2)

            balon = (bx,by)

            cv2.circle(
                frame,
                (bx,by),
                15,
                (0,255,255),
                3
            )

            cv2.putText(
                frame,
                "BALON",
                (x1,y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0,255,255),
                2
            )

    # POSESION
    if balon:

        bx,by = balon

        for x,y in azules:

            d = ((x-bx)**2 + (y-by)**2)**0.5

            if d < 120:
                posesion_azul += 1

        for x,y in rojos:

            d = ((x-bx)**2 + (y-by)**2)**0.5

            if d < 120:
                posesion_rojo += 1

    formacion_azul = detectar_formacion(
        azules
    )

    formacion_rojo = detectar_formacion(
        rojos
    )

    prediccion = predecir_jugada(
        balon,
        azules,
        rojos
    )

    xg = calcular_xg(
        balon,
        1280,
        720
    )

    return (
        frame,
        azules,
        rojos,
        posiciones,
        posesion_azul,
        posesion_rojo,
        formacion_azul,
        formacion_rojo,
        prediccion,
        xg
    )