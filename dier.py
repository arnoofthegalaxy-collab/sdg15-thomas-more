import streamlit as st
import sounddevice as sd
from scipy.io.wavfile import write
import requests
from transformers import pipeline

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f2010 0%, #1a3a0f 50%, #0f2010 100%); }
    h1 { color: #4cff72 !important; text-align: center; text-shadow: 0 0 20px #4cff72; }
    </style>
""", unsafe_allow_html=True)

st.title("🐾 Diergeluid Herkenner (ECHTE AI)")

# 🐾 dierenlijst (emoji + naam)
dieren = {
    "dog": ("🐶", "Hond"),
    "cat": ("🐱", "Kat"),
    "bird": ("🐦", "Vogel"),
    "cow": ("🐄", "Koe"),
    "pig": ("🐷", "Varken"),
    "sheep": ("🐑", "Schaap"),
    "horse": ("🐴", "Paard"),
    "lion": ("🦁", "Leeuw"),
    "frog": ("🐸", "Kikker"),
    "wolf": ("🐺", "Wolf"),
    "elephant": ("🐘", "Olifant"),
    "tiger": ("🐯", "Tijger"),
    "bear": ("🐻", "Beer"),
    "monkey": ("🐒", "Aap"),
    "snake": ("🐍", "Slang"),
    "duck": ("🦆", "Eend"),
    "chicken": ("🐔", "Kip"),
    "owl": ("🦉", "Uil"),
    "eagle": ("🦅", "Adelaar"),
    "parrot": ("🦜", "Papegaai"),
    "penguin": ("🐧", "Pinguïn"),
    "dolphin": ("🐬", "Dolfijn"),
    "whale": ("🐋", "Walvis"),
    "shark": ("🦈", "Haai"),
    "crocodile": ("🐊", "Krokodil"),
    "turtle": ("🐢", "Schildpad"),
    "lizard": ("🦎", "Hagedis"),
    "fox": ("🦊", "Vos"),
    "deer": ("🦌", "Hert"),
    "rabbit": ("🐰", "Konijn"),
    "mouse": ("🐭", "Muis"),
    "rat": ("🐀", "Rat"),
    "bat": ("🦇", "Vleermuis"),
    "gorilla": ("🦍", "Gorilla"),
    "zebra": ("🦓", "Zebra"),
    "giraffe": ("🦒", "Giraf"),
    "hippo": ("🦛", "Nijlpaard"),
    "rhino": ("🦏", "Neushoorn"),
    "camel": ("🐪", "Kameel"),
    "kangaroo": ("🦘", "Kangoeroe"),
    "koala": ("🐨", "Koala"),
    "panda": ("🐼", "Panda"),
    "flamingo": ("🦩", "Flamingo"),
    "swan": ("🦢", "Zwaan"),
    "crab": ("🦀", "Krab"),
    "octopus": ("🐙", "Octopus"),
    "snail": ("🐌", "Slak"),
    "butterfly": ("🦋", "Vlinder"),
    "bee": ("🐝", "Bij"),
    "spider": ("🕷️", "Spin"),
    "fish": ("🐟", "Vis"),
}

# 🎤 opname
def record_audio(filename="temp.wav", duration=3):
    fs = 16000
    st.info("🎤 Opname bezig...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, recording)
    st.success("✅ Opgenomen!")
    return filename

# 🧠 AI model
@st.cache_resource
def load_model():
    return pipeline("audio-classification")

classifier = load_model()

# 🔍 detectie
def detect_animal(file):
    results = classifier(file)

    dier_keywords = list(dieren.keys()) + ["animal"]

    for r in results:
        label = r["label"].lower()

        for woord in dier_keywords:
            if woord in label:
                return woord

    return results[0]["label"].lower().split(",")[0]

# 🌐 Wikipedia
def get_wikipedia(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        data = requests.get(url).json()

        if "thumbnail" in data:
            return data["thumbnail"]["source"], data.get("extract")

        # fallback zoek
        search = requests.get(
            f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=1&format=json"
        ).json()

        if search[1]:
            new_query = search[1][0]
            data = requests.get(
                f"https://en.wikipedia.org/api/rest_v1/page/summary/{new_query}"
            ).json()

            return data.get("thumbnail", {}).get("source"), data.get("extract")

    except:
        pass

    return None, None

# 🎛️ UI
if st.button("🎤 Neem geluid op"):
    file = record_audio()
    st.audio(file)

    if st.button("🔍 Herken dier"):
        with st.spinner("🧠 AI analyseert..."):
            dier = detect_animal(file)

        emoji, naam = dieren.get(dier, ("🐾", dier.capitalize()))

        st.markdown(f"## {emoji} {naam}")

        img, text = get_wikipedia(dier)

        if img:
            st.image(img, use_container_width=True)

        if text:
            st.info(text[:300] + "...")