import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Configuración de página
st.set_page_config(page_title="Conversión de Texto a Audio", layout="centered")

# Título e imagen principal
st.title("Conversión de Texto a Audio")
image = Image.open('gato_raton.png')
st.image(image, width=350)

# Sidebar
with st.sidebar:
    st.subheader("Escribe o selecciona texto para escuchar.")

# Crear carpeta temporal si no existe
os.makedirs("temp", exist_ok=True)

# Contenido principal
st.subheader("Una pequeña Fábula")

fable_text = (
    "¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. "
    "Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. "
    "Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está "
    "la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato... y se lo comió.\n\nFranz Kafka."
)

st.write(fable_text)

st.markdown("**¿Quieres escucharlo? Copia el texto y pégalo abajo.**")
text = st.text_area("Ingresa el texto a escuchar")

# Selección de idioma
option_lang = st.selectbox("Selecciona el idioma", ("Español", "English"))
language_codes = {"Español": "es", "English": "en"}
lg = language_codes[option_lang]

def text_to_speech(texto, language):
    tts = gTTS(texto, lang=language)
    filename = (texto[:20].strip().replace(" ", "_") or "audio") + ".mp3"
    filepath = os.path.join("temp", filename)
    tts.save(filepath)
    return filepath

def download_audio(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:audio/mp3;base64,{bin_str}" download="{os.path.basename(filepath)}">Descargar Audio</a>'
    st.markdown(href, unsafe_allow_html=True)

# Botón para convertir
if st.button("Convertir a Audio"):
    if text:
        audio_path = text_to_speech(text, lg)
        st.audio(audio_path, format="audio/mp3")
        download_audio(audio_path)
    else:
        st.warning("Por favor, ingresa un texto antes de convertir.")

# Funcionalidad de limpieza de archivos antiguos
def remove_old_files(days=7):
    now = time.time()
    threshold = days * 86400
    for file in glob.glob("temp/*.mp3"):
        if os.stat(file).st_mtime < now - threshold:
            os.remove(file)

remove_old_files()
