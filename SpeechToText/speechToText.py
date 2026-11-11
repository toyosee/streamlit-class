import streamlit as st
import whisper

st.title("Speech to Text")
# audio_file = st.file_uploader("Upload file", type=["mp3", "wav", "m4a"])
audio_file = "clinical_analysis.mp3"
transcribe_button = st.button("Transcribe")

st.audio(audio_file, format="audio/mpeg")

if audio_file is not None and transcribe_button:
                # 2. Load the model
            model = whisper.load_model("tiny")

            # 3. Transcribe using the temporary file path
            result = model.transcribe(audio_file)
            st.success("Done!")
            st.write(result["text"])


print("done")
