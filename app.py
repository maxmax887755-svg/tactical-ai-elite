

import streamlit as st
import cv2

from detector import analizar_frame


if "running" not in st.session_state:
    st.session_state.running = False

if "score_blue" not in st.session_state:
    st.session_state.score_blue = 0

if "score_red" not in st.session_state:
    st.session_state.score_red = 0

if "pos_blue" not in st.session_state:
    st.session_state.pos_blue = 50

if "xg_pass" not in st.session_state:
    st.session_state.xg_pass = 0

if "next_pass" not in st.session_state:
    st.session_state.next_pass = None

if "counter_attack" not in st.session_state:
    st.session_state.counter_attack = False



st.title("⚽ Tactical AI Elite")


st.subheader("🎨 Configuración de Equipos")

color_equipo1 = st.color_picker(
    "Color Equipo 1",
    "#0000FF"
)

color_equipo2 = st.color_picker(
    "Color Equipo 2",
    "#FF0000"
)


col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶️ Iniciar"):
        st.session_state.running = True

with col2:
    if st.button("⏸ Pausar"):
        st.session_state.running = False

with col3:
    if st.button("🔄 Reset"):
        st.session_state.running = False

        st.session_state.score_blue = 0
        st.session_state.score_red = 0

        st.session_state.pos_blue = 50

        st.session_state.xg_pass = 0

        st.session_state.next_pass = None

        st.session_state.counter_attack = False



st.subheader("⚽ Marcador")

st.write(
    f"🔵 Azul: {st.session_state.score_blue}"
)

st.write(
    f"🔴 Rojo: {st.session_state.score_red}"
)



st.subheader("📊 Posesión")

st.progress(
    st.session_state.pos_blue / 100
)

st.write(
    f"🔵 Azul: {st.session_state.pos_blue:.1f}%"
)

st.write(
    f"🔴 Rojo: {100 - st.session_state.pos_blue:.1f}%"
)



st.subheader("🎯 xG tras pase")

st.metric(
    "xG",
    st.session_state.xg_pass
)



st.subheader("🧠 Predicción siguiente pase")

if st.session_state.next_pass is not None:

    st.success(
        f"Jugador probable: #{st.session_state.next_pass}"
    )

else:

    st.warning("Sin predicción")



st.subheader("⚡ Contraataque")

if st.session_state.counter_attack:

    st.error(
        "⚡ CONTRAATAQUE DETECTADO"
    )

else:

    st.success(
        "Juego normal"
    )



video = st.file_uploader(
    "Sube un partido",
    type=["mp4"]
)

frame_box = st.empty()



if video is not None and st.session_state.running:

    cap = cv2.VideoCapture(video.name)

    while cap.isOpened() and st.session_state.running:

        ret, frame = cap.read()

        if not ret:
            break

        resultado, eventos = analizar_frame(
            frame,
            color_equipo1,
            color_equipo2
        )

        
        if eventos.get("gol_azul"):
            st.session_state.score_blue += 1

        if eventos.get("gol_rojo"):
            st.session_state.score_red += 1

        
        st.session_state.pos_blue = eventos.get(
            "posesion_azul",
            50
        )

        
        st.session_state.xg_pass = eventos.get(
            "xg_pass",
            0
        )

        
        st.session_state.next_pass = eventos.get(
            "next_pass",
            None
        )

        
        st.session_state.counter_attack = eventos.get(
            "counter_attack",
            False
        )

        frame_box.image(
            resultado,
            channels="BGR"
        )