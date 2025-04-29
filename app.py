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

# Definir los cuentos disponibles
stories = {
    "El Gato y el Ratón": (
        "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. "
        "Corría y corría y me alegraba ver esos muros, a diestra y siniestra, en la distancia. Pero esas paredes se estrechan "
        "tan rápido que me encuentro en el último cuarto y ahí en el rincón está la trampa sobre la cual debo pasar. "
        "Todo lo que debes hacer es cambiar de rumbo -dijo el gato... y se lo comió."
    ),
    "Caperucita Roja": (
        "Había una vez una niña llamada Caperucita Roja, que vivía en un pueblo al borde de un inmenso bosque. "
        "Un día su madre le pidió llevar una cesta con deliciosos pasteles a su abuelita enferma..."
    ),
    "Los Tres Cerditos": (
        "Érase una vez tres cerditos que decidieron construir cada uno una casa para protegerse del lobo. "
        "El primero usó paja, el segundo usó madera y el tercero ladrillos. Cuando el lobo llegó..."
    )
}

# Selector de cuento mediante slider
title_list = list(stories.keys())
story_title = st.select_slider("Selecciona un cuento:", options=title_list)
story_text = stories[story_title]

# Mostrar título y texto del cuento
st.header(story_title)
st.markdown(story_text)

# Selección de idioma de narración
language = st.selectbox("Idioma de la narración", ["Español", "English"])
language_code = {"Español": "es", "English": "en"}[language]

# Función de conversión de texto a audio
def text_to_speech(text_input, lang, title):
    tts = gTTS(text_input, lang=lang)
    filename = title.replace(" ", "_") + f"_{lang}.mp3"
    filepath = os.path.join("temp", filename)
    tts.save(filepath)
    return filepath

# Botón para reproducir audio del cuento
if st.button("🔊 Escuchar Cuento"):
    os.makedirs("temp", exist_ok=True)
    # Generar audio
    audio_path = text_to_speech(story_text, language_code, story_title)
    # Reproducir directamente desde el archivo
    st.audio(audio_path, format="audio/mp3")

    # Enlace de descarga
    with open(audio_path, "rb") as f:
        bin_str = base64.b64encode(f.read()).decode()
    href = f'<a href="data:audio/mp3;base64,{bin_str}" download="{os.path.basename(audio_path)}">📥 Descargar Audio</a>'
    st.markdown(href, unsafe_allow_html=True)

# Limpieza de archivos antiguos
def clean_temp_folder(folder="temp", days=7):
    now = time.time()
    for file in glob.glob(f"{folder}/*.mp3"):
        if os.stat(file).st_mtime < now - days * 86400:
            os.remove(file)

clean_temp_folder()
