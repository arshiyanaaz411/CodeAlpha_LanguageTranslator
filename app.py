import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64

st.set_page_config(page_title="Language Translator", page_icon="🌐", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        background-image: 
            linear-gradient(rgba(74,144,226,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(74,144,226,0.05) 1px, transparent 1px);
        background-size: 25px 25px;
    }
    .main-title {
        font-size: 46px;
        font-weight: 800;
        text-align: center;
        font-family: 'Courier New', monospace;
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #8b949e;
        margin-bottom: 25px;
        font-size: 14px;
        font-family: 'Courier New', monospace;
    }
    div[data-testid="stTextArea"] textarea {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        color: #c9d1d9;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        background: linear-gradient(90deg, #238636, #2ea043);
        color: white;
        border: 1px solid #2ea043;
        border-radius: 8px;
        height: 48px;
        font-weight: 700;
        width: 100%;
        font-family: 'Courier New', monospace;
        transition: 0.3s;
    }
    .stButton>button:hover {
        box-shadow: 0 0 12px rgba(46,160,67,0.5);
    }
    .glass-card {
        background: #161b22;
        padding: 22px;
        border-radius: 10px;
        border-left: 3px solid #58a6ff;
        border: 1px solid #30363d;
        font-family: 'Courier New', monospace;
        color: #c9d1d9;
        margin-top: 15px;
    }
    .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22;
        border-radius: 8px;
        border: 1px solid #30363d;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🌐 Language Translator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Real-time translation powered by AI · Built for CodeAlpha Internship</p>', unsafe_allow_html=True)

languages = {
    "Auto Detect": "auto", "English": "en", "Hindi": "hi", "Kannada": "kn",
    "French": "fr", "Spanish": "es", "German": "de", "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN", "Arabic": "ar", "Russian": "ru",
    "Tamil": "ta", "Telugu": "te", "Marathi": "mr", "Bengali": "bn",
    "Gujarati": "gu", "Punjabi": "pa", "Malayalam": "ml", "Urdu": "ur",
    "Portuguese": "pt", "Italian": "it", "Korean": "ko", "Dutch": "nl",
    "Turkish": "tr", "Vietnamese": "vi", "Thai": "th", "Indonesian": "id",
    "Polish": "pl", "Greek": "el", "Hebrew": "iw", "Swedish": "sv"
}
target_languages = {k: v for k, v in languages.items() if k != "Auto Detect"}

if "history" not in st.session_state:
    st.session_state.history = []
if "source_lang" not in st.session_state:
    st.session_state.source_lang = "Auto Detect"
if "target_lang" not in st.session_state:
    st.session_state.target_lang = "Hindi"

tab1, tab2, tab3 = st.tabs(["🔤 Translate", "🕘 History", "ℹ️ About"])

with tab1:
    col1, col2, col3 = st.columns([5, 1, 5])
    with col1:
        source_lang = st.selectbox("From", list(languages.keys()),
                                    index=list(languages.keys()).index(st.session_state.source_lang))
    with col2:
        st.write("")
        st.write("")
        if st.button("🔄"):
            if st.session_state.source_lang != "Auto Detect":
                st.session_state.source_lang, st.session_state.target_lang = (
                    st.session_state.target_lang, st.session_state.source_lang
                )
                st.rerun()
    with col3:
        target_lang = st.selectbox("To", list(target_languages.keys()),
                                    index=list(target_languages.keys()).index(st.session_state.target_lang))

    st.session_state.source_lang = source_lang
    st.session_state.target_lang = target_lang

    input_text = st.text_area("", height=160, placeholder="Type or paste your text here...", label_visibility="collapsed")

    c1, c2 = st.columns([3, 1])
    with c1:
        st.caption(f"📝 {len(input_text)} characters")
    with c2:
        if len(input_text) > 4500:
            st.caption("⚠️ Getting long")

    translate_clicked = st.button("✨ Translate")

    if translate_clicked:
        if input_text.strip() == "":
            st.warning("Please enter some text to translate.")
        else:
            with st.spinner("Translating..."):
                try:
                    src_code = "auto" if source_lang == "Auto Detect" else languages[source_lang]
                    translated = GoogleTranslator(source=src_code, target=languages[target_lang]).translate(input_text)

                    st.markdown(f'<div class="glass-card">{translated}</div>', unsafe_allow_html=True)

                    st.session_state.history.append((source_lang, target_lang, input_text, translated))

                    colA, colB, colC = st.columns(3)
                    with colA:
                        tts = gTTS(text=translated, lang=languages[target_lang])
                        tts.save("output.mp3")
                        audio_bytes = open("output.mp3", "rb").read()
                        st.audio(audio_bytes, format="audio/mp3")
                    with colB:
                        st.download_button("⬇️ Download", translated, file_name="translation.txt")
                    with colC:
                        b64 = base64.b64encode(translated.encode()).decode()
                        st.markdown(f'<a href="data:text/plain;base64,{b64}" download="translation.txt" style="color:#58a6ff;">📋 Copy link</a>', unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

with tab2:
    st.subheader("Recent Translations")
    if st.session_state.history:
        for i, (s, t, orig, trans) in enumerate(reversed(st.session_state.history[-10:])):
            st.markdown(f"""
            <div class="glass-card">
            <b>{s} → {t}</b><br>
            <span style="color:#8b949e;">{orig[:60]}{'...' if len(orig)>60 else ''}</span><br>
            <span style="color:#58a6ff;">{trans[:60]}{'...' if len(trans)>60 else ''}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No translations yet. Start translating to see history here.")

with tab3:
    st.markdown("""
    <div class="glass-card">
    <h4>About this App</h4>
    <p>A real-time language translator built using Streamlit, Deep Translator, and Google Text-to-Speech.</p>
    <p><b>Features:</b> Auto language detection, 10+ languages, audio playback, downloadable translations, session history.</p>
    <p><b>Built for:</b> CodeAlpha AI Internship — Task 1</p>
    </div>
    """, unsafe_allow_html=True)
