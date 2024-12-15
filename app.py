import streamlit as st
from elevenlabs import ElevenLabs

# Set background image
def set_background(image_path):
    """Set the background image for the Streamlit app."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url({image_path});
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function to set the background
set_background("ast/barq_logo.png")

# Streamlit UI
st.title("barq T2S")
st.sidebar.header("Configuration")

# User inputs for API key, voice, and text
api_key = st.sidebar.text_input("Enter your Eleven Labs API Key", type="password")
text = st.text_area("Enter text to convert to speech:")

if st.button("Generate Speech"):
    if not api_key:
        st.error("Please enter your API key.")
    elif not text.strip():
        st.error("Please enter some text.")
    else:
        st.info("Generating speech...")
        try:
            # Eleven Labs client setup
            client = ElevenLabs(api_key=api_key)

            # Text-to-speech conversion
            res = client.text_to_speech.convert(
                voice_id="mRdG9GYEjJmIzqbYTidv",
                output_format="mp3_44100_128",
                text=text,
                model_id="eleven_multilingual_v2",
            )

            # Save the audio file locally
            audio_file_path = "output_audio.mp3"
            with open(audio_file_path, "wb") as audio_file:
                for chunk in res:
                    audio_file.write(chunk)

            st.success("Speech generated successfully!")
            # Provide download link for the audio file
            with open(audio_file_path, "rb") as file:
                st.download_button(
                    label="Download Audio",
                    data=file,
                    file_name="output_audio.mp3",
                    mime="audio/mpeg",
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
