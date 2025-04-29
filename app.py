import streamlit as st
import os
import time
import glob
from gtts import gTTS
import base64
from PIL import Image

# Configurar la página
st.set_page_config(
    page_title="Texto a Audio",
    page_icon="🔊",
    layout="centered"
)

# Estilo minimalista con colores suaves
st.markdown("""
    <style>
        body {
            background-color: #f5f5dc;
        }
        .block-container {
            padding: 2rem 2rem;
            border-radius: 12px;
            background-color: #ffffff;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stTextArea textarea {
            background-color: #fffaf0;
            border: 1px solid #e6e6e6;
            border-radius: 0.5rem;
        }
        .stButton > button {
            background-color: #e2c799;
            color: black;
            border-radius: 0.5rem;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #d4b277;
        }
    </style>
""", unsafe_allow_html=True)

# Imagen de portada
image = Image.open("gato_raton.png")
st.image(image, width=300)

st.title("🔊 Conversor de Texto a Audio")

# Fábula introductoria
st.markdown("""
#### Una pequeña fábula
> "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo.
Corría y corría y me alegraba ver esos muros, a diestra y siniestra, en la distancia. Pero esas paredes se
estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está la trampa sobre la cual
debo pasar.\nTodo lo que debes hacer es cambiar de rumbo -dijo el gato... y se lo comió."  
— *Franz Kafka*
""")

# Entrada de texto
st.markdown("**¿Quieres escuchar un texto? Escríbelo abajo:**")
text = st.text_area("Ingresa el texto aquí")

# Selección de idioma
language = st.selectbox("Idioma de la voz", ["Español", "English"])
language_code = {"Español": "es", "English": "en"}[language]

# Función de conversión
def text_to_speech(text_input, lang):
    tts = gTTS(text_input, lang=lang)
    filename = (text_input[:20].strip().replace(" ", "_") or "audio") + ".mp3"
    filepath = os.path.join("temp", filename)
    tts.save(filepath)
    return filepath

# Botón para convertir
if st.button("🎧 Escuchar Audio"):
    if text:
        os.makedirs("temp", exist_ok=True)
        audio_path = text_to_speech(text, language_code)
        st.audio(audio_path, format="audio/mp3")

        with open(audio_path, "rb") as f:
            data = f.read()
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:audio/mp3;base64,{bin_str}" download="{os.path.basename(audio_path)}">📥 Descargar Audio</a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Por favor escribe un texto antes de convertir.")

# Limpieza de archivos antiguos
now = time.time()
for file in glob.glob("temp/*.mp3"):
    if os.stat(file).st_mtime < now - 7 * 86400:
        os.remove(file)
