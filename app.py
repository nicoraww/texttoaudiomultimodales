import streamlit as st
import os
import time
import glob
from gtts import gTTS
import base64
from PIL import Image

# Configurar la página
st.set_page_config(
    page_title="Asistente de Lectura de Cuentos",
    page_icon="📚",
    layout="centered"
)

# Estilo oscuro con texto blanco y botones invertidos
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
        }
        .block-container {
            padding: 2rem;
            border-radius: 12px;
            background-color: #000000;
            box-shadow: 0 4px 6px rgba(255, 255, 255, 0.1);
        }
        /* Texto y componentes */
        .stText, .stMarkdown, .stHeader, .stSelectContainer, .stSelectbox, .stSlider {
            color: #ffffff;
        }
        .stSlider > div > div > div {
            color: #ffffff;
        }
        /* Botones con fondo blanco y texto negro */
        .stButton > button {
            background-color: #000000;
            color: #ffffff;
            border: 2px solid #ffffff;
            border-radius: 0.5rem;
            font-weight: bold;
            padding: 0.6rem 1.2rem;
        }
        .stButton > button:hover {
            background-color: #333333;
            color: #ffdd00;
            border-color: #ffdd00;
        }
        /* Ajuste de elementos de selección y slider */
        .stSelectbox > div, .stSlider > div {
            background-color: #1a1a1a;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

# Imagen de portada
image = Image.open("gato_raton.png")
st.image(image, width=300)

st.title("📚 Asistente de Lectura de Cuentos")

# Definir los cuentos disponibles con versiones en español e inglés
stories = {
    "El Gato y el Ratón": {
        "es": (
            "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. "
            "Corría y corría y me alegraba ver esos muros, a diestra y siniestra, en la distancia. Pero esas paredes se estrechan "
            "tan rápido que me encuentro en el último cuarto y ahí en el rincón está la trampa sobre la cual debo pasar. "
            "Todo lo que debes hacer es cambiar de rumbo -dijo el gato... y se lo comió."
        ),
        "en": (
            "‘Alas!’, said the mouse. ‘The world grows smaller every day. At first it was so vast that I was afraid. "
            "I ran and ran, and I was delighted to see those walls on
