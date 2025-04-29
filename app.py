import streamlit as st
import os
import time
import glob
from gtts import gTTS
import base64
from PIL import Image

# Configurar la página
theme = {
    'primaryColor': '#000000',
    'backgroundColor': '#000000',
    'secondaryBackgroundColor': '#1a1a1a',
    'textColor': '#ffffff',
    'font': 'sans serif'
}
st.set_page_config(
    page_title="Asistente de Lectura de Cuentos",
    page_icon="📚",
    layout="centered",
)
st.markdown(f"<style> .css-18e3th9 {{background-color: {theme['backgroundColor']}}} </style>", unsafe_allow_html=True)

# Estilo adicional
st.markdown("""
    <style>
        .block-container { padding: 2rem; background-color: #000000; }
        .stButton > button { background-color: #000000; color: #ffffff; border: 2px solid #ffffff; border-radius: 0.5rem; padding: 0.6rem 1.2rem; font-weight: bold; }
        .stButton > button:hover { background-color: #333333; color: #ffdd00; border-color: #ffdd00; }
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
            "I ran and ran, and I was delighted to see those walls on my right and left at a distance. But those walls narrow "
            "so quickly that I find myself in the last chamber, and in the corner stands the trap I must pass over. "
            "‘All you must do is change your course,’ said the cat... and it ate him."
        )
    },
    "Caperucita Roja": {
        "es": (
            "Había una vez una niña llamada Caperucita Roja, que vivía en un pueblo al borde de un inmenso bosque. "
            "Un día su madre le pidió llevar una cesta con deliciosos pasteles a su abuelita enferma..."
        ),
        "en": (
            "Once upon a time there was a girl named Little Red Riding Hood, who lived in a village at the edge of a great forest. "
            "One day, her mother asked her to bring a basket of delicious cakes to her sick grandmother..."
        )
    },
    "Los Tres Cerditos": {
        "es": (
            "Érase una vez tres cerditos que decidieron construir cada uno una casa para protegerse del lobo. "
            "El primero usó paja, el segundo usó madera y el tercero ladrillos. Cuando el lobo llegó..."
        ),
        "en": (
            "Once upon a time there were three little pigs who decided to each build a house to protect themselves from the wolf. "
            "The first used straw, the second used wood, and the third used bricks. When the wolf arrived..."
        )
    }
}

# Mostrar lista de títulos y asignar índices
title_list = list(stories.keys())
options_display = "\n".join(f"{i+1}. {t}" for i, t in enumerate(title_list))
st.markdown("**Cuentos disponibles:**\n" + options_display)

# Selector mediante slider numérico
title_index = st.slider("Selecciona un número de cuento:", 1, len(title_list), 1)
story_title = title_list[title_index - 1]

# Selección de idioma de narración
language = st.selectbox("Idioma de la narración", ["Español", "English"])
language_code = "es" if language == "Español" else "en"

# Obtener texto según idioma
story_text = stories[story_title][language_code]

# Mostrar título y texto
st.header(story_title)
st.markdown(story_text)

# Función de conversión de texto a audio
def text_to_speech(text_input, lang, title):
    tts = gTTS(text_input, lang=lang)
    filename = title.replace(" ", "_") + f"_{lang}.mp3"
    filepath = os.path.join("temp", filename)
    tts.save(filepath)
    return filepath

# Botón para descargar audio sin reproductor
audio_button_label = "📥 Descargar Audio"
if st.button(audio_button_label):
    os.makedirs("temp", exist_ok=True)
    audio_path = text_to_speech(story_text, language_code, story_title)
    with open(audio_path, "rb") as f:
        bin_str = base64.b64encode(f.read()).decode()
    href = f'<a href="data:audio/mp3;base64,{bin_str}" download="{os.path.basename(audio_path)}">{audio_button_label}</a>'
    st.markdown(href, unsafe_allow_html=True)

# Limpieza de archivos antiguos
def clean_temp_folder(folder="temp", days=7):
    now = time.time()
    for file in glob.glob(f"{folder}/*.mp3"):
        if os.stat(file).st_mtime < now - days * 86400:
            os.remove(file)

clean_temp_folder()
