import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS

st.title("Language Translator")
st.write("Enter text below, choose languages, and get instant translation!")

languages = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Japanese": "ja",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Russian": "ru"
}

input_text = st.text_area("Enter text to translate:")

col1, col2 = st.columns(2)
with col1:
    source_lang = st.selectbox("Source Language", list(languages.keys()), index=0)
with col2:
    target_lang = st.selectbox("Target Language", list(languages.keys()), index=1)

if st.button("Translate"):
    if input_text.strip() == "":
        st.warning("Please enter some text to translate.")
    else:
        try:
            translated = GoogleTranslator(source=languages[source_lang], target=languages[target_lang]).translate(input_text)
            st.success("Translation:")
            st.write(translated)
            tts = gTTS(text=translated, lang=languages[target_lang])
            tts.save("output.mp3")
            audio_file = open("output.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
