import streamlit as st
import cv2
import tempfile

from detector import analizar_frame
from tactica import analizar
from heatmap import (
    actualizar_heatmap,
    obtener_heatmap
)

st.set_page_config(
    page_title="Tactical AI Elite",
    layout="wide"
)

with open("style.css") as f:

    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

st.title("Tactical AI Elite")

video = st.file_uploader(
    "Sube un partido",
    type=["mp4"]
)

if video:

    temp = tempfile.NamedTemporaryFile(
        delete=False
    )

    temp.write(video.read())

    cap = cv2.VideoCapture(
        temp.name
    )

    c1,c2,c3,c4,c5,c6,c7 = st.columns(7)

    total_box = c1.empty()
    azul_box = c2.empty()
    rojo_box = c3.empty()
    posesion_box = c4.empty()
    tactica_box = c5.empty()
    formacion_box = c6.empty()
    xg_box = c7.empty()

    frame_box = st.empty()

    heatmap_box = st.empty()

    while True:

        ret,frame = cap.read()

        if not ret:
            break

        frame = cv2.resize(
            frame,
            (1280,720)
        )

        (
            analizado,
            azules,
            rojos,
            posiciones,
            pa,
            pr,
            formacion_azul,
            formacion_rojo,
            prediccion,
            xg
        ) = analizar_frame(frame)

        mensaje,presion_a,presion_r = analizar(
            azules,
            rojos
        )

        total = len(azules) + len(rojos)

        if pa > pr:
            posesion = "Azul"
        elif pr > pa:
            posesion = "Rojo"
        else:
            posesion = "Dividida"

        total_box.metric(
            "Jugadores",
            total
        )

        azul_box.metric(
            "Azules",
            len(azules)
        )

        rojo_box.metric(
            "Rojos",
            len(rojos)
        )

        posesion_box.metric(
            "Posesion",
            posesion
        )

        tactica_box.metric(
            "Presion",
            f"A:{presion_a} | R:{presion_r}"
        )

        formacion_box.metric(
            "Formaciones",
            f"A:{formacion_azul} | R:{formacion_rojo}"
        )

        xg_box.metric(
            "xG",
            xg
        )

        cv2.putText(
            analizado,
            mensaje,
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            3
        )

        cv2.putText(
            analizado,
            prediccion,
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            3
        )

        actualizar_heatmap(
            posiciones
        )

        mapa = obtener_heatmap()

        frame_box.image(
            analizado,
            channels="BGR"
        )

        heatmap_box.image(
            mapa,
            channels="BGR"
        )