import streamlit as st
import requests
import tempfile
import os

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f0f0f 0%, #1a0533 50%, #0f0f0f 100%); }
    h1 { color: #b44fff !important; text-align: center; text-shadow: 0 0 20px #b44fff; }
    h2, h3 { color: #b44fff !important; }
    .stButton>button { 
        background: linear-gradient(90deg, #b44fff, #7b2fff); 
        color: white; border-radius: 20px; border: none;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

API_KEY = "28dff0a3f0bcf7483f30748b3163b286"

st.markdown("<h1>🎵 Muziek Herkenner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888;'>Upload een video of audio en ontdek het liedje!</p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 📁 Upload je bestand")
    uploaded_file = st.file_uploader("Kies een video of audio bestand", type=["mp4", "mp3", "wav", "m4a", "mov"])

    if uploaded_file is not None:
        st.success(f"✅ Bestand geüpload: {uploaded_file.name}")
        
        if st.button("🔍 Herken Muziek", use_container_width=True):
            with st.spinner("🎵 AI luistert naar je muziek..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                with open(tmp_path, "rb") as f:
                    response = requests.post(
                        "https://api.audd.io/",
                        data={"api_token": API_KEY, "return": "spotify,apple_music"},
                        files={"file": f}
                    )
                
                result = response.json()
                os.unlink(tmp_path)

                if result.get("status") == "success" and result.get("result"):
                    song = result["result"]
                    
                    st.markdown("---")
                    st.markdown("## 🎉 Liedje Gevonden!")
                    
                    r1, r2 = st.columns([2, 3])
                    with r1:
                        if song.get("spotify") and song["spotify"].get("album", {}).get("images"):
                            st.image(song["spotify"]["album"]["images"][0]["url"], use_container_width=True)
                    with r2:
                        st.markdown(f"### 🎵 {song.get('title', 'Onbekend')}")
                        st.markdown(f"**🎤 Artiest:** {song.get('artist', 'Onbekend')}")
                        st.markdown(f"**💿 Album:** {song.get('album', 'Onbekend')}")
                        st.markdown(f"**📅 Jaar:** {song.get('release_date', 'Onbekend')}")
                        
                        if song.get("spotify", {}).get("external_urls", {}).get("spotify"):
                            st.link_button("🟢 Open in Spotify", song["spotify"]["external_urls"]["spotify"])
                else:
                    st.error("❌ Liedje niet herkend. Probeer een langer fragment!")

with col2:
    st.markdown("### ℹ️ Hoe werkt het?")
    st.info("""
    1. 📁 Upload een video of audio
    2. 🔍 Klik op 'Herken Muziek'
    3. 🎵 AI herkent het liedje
    4. 🎉 Zie titel, artiest & album!
    """)
    st.markdown("### 📋 Ondersteunde formaten")
    st.markdown("- 🎬 Video: MP4, MOV")
    st.markdown("- 🎵 Audio: MP3, WAV, M4A")