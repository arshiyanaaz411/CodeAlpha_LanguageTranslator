import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        color: #4A90E2;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
        width: 100%;
    }
    .result-box {
        background-color: #1E1E2F;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4A90E2;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌐 Language Translator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Translate text instantly across multiple languages with audio support</p>', unsafe_allow_html=True)

languages = {
    "English": "en", "Hindi": "hi", "Kannada": "kn", "French": "fr",
    "Spanish": "es", "German": "de", "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN", "Arabic": "ar", "Russian": "ru"
}

if "source_lang" not in st.session_state:
    st.session_state.source_lang = "English"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Hindi"
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("ℹ️ About")
    st.write("This tool uses Google Translate to convert text between 10+ languages, with text-to-speech support.")
    st.divider()
    st.header("📜 History")
    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            st.caption(f"**{h[0]}** → **{h[1]}**")
            st.text(h[2][:40] + "..." if len(h[2]) > 40 else h[2])
    else:
        st.caption("No translations yet.")

col1, col2, col3 = st.columns([5, 1, 5])
with col1:
    source_lang = st.selectbox("Source Language", list(languages.keys()),
                                index=list(languages.keys()).index(st.session_state.source_lang))
with col2:
    st.write("")
    st.write("")
    if st.button("🔄"):
        st.session_state.source_lang, st.session_state.target_lang = (
            st.session_state.target_lang, st.session_state.source_lang
        )
        st.rerun()
with col3:
    target_lang = st.selectbox("Target Language", list(languages.keys()),
                                index=list(languages.keys()).index(st.session_state.target_lang))

st.session_state.source_lang = source_lang
st.session_state.target_lang = target_lang

input_text = st.text_area("Enter text to translate:", height=150, placeholder="Type or paste your text here...")
st.caption(f"{len(input_text)} characters")

if st.button("Translate ➤"):
    if input_text.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            try:
                translated = GoogleTranslator(
                    source=languages[source_lang],
                    target=languages[target_lang]
                ).translate(input_text)

                st.markdown("### ✅ Translated Text")
                st.markdown(f'<div class="result-box">{translated}</div>', unsafe_allow_html=True)

                st.session_state.history.append((source_lang, target_lang, translated))

                tts = gTTS(text=translated, lang=languages[target_lang])
                tts.save("output.mp3")
                audio_file = open("output.mp3", "rb")
                st.audio(audio_file.read(), format="audio/mp3")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
