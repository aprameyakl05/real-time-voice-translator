import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator


# Initialize the translator and pygame mixer
translator = Translator()
pygame.mixer.init()

# Create a mapping between language names and language codes
language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src=from_language, dest=to_language)

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang=to_language, slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()

    return "cache_file.mp3"

    while pygame.mixer.get_busy():  # Wait for the audio to finish playing
        time.sleep(0.1)
    os.remove("cache_file.mp3")  # Remove the audio file after playing

def main_process(output_placeholder, from_language, to_language):
    rec = sr.Recognizer()
    with sr.Microphone() as source:
        output_placeholder.text("Listening...")
        rec.pause_threshold = 1
        audio = rec.listen(source, phrase_time_limit=10)

        try:
            def abc():
                output_placeholder.text("Processing...")
                spoken_text = rec.recognize_google(audio, language=from_language)

                return spoken_text

            output_placeholder.text("Translating...")
            speaked_text=abc()
            translated_text = translator_function(speaked_text, from_language, to_language)

            st.write(f"Spoken Text: {speaked_text}")

            output_placeholder.text(f"Translated Text: {translated_text.text}")
            text_to_voice(translated_text.text, to_language)

        except Exception as e:
            output_placeholder.text("Error: " + str(e))

# UI layout

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Home", "Translate", "About","Logout"])


# Home page
if page == "Home":
    st.title("Real-Time Voice Translator")
    st.write("Welcome to the Real-Time Voice Translator!")

    st.subheader("Transform Your Conversations")
    st.write(
        "Our application allows you to communicate effortlessly across language barriers. Whether you're traveling, conducting business, or connecting with friends from different cultures, our voice translator is here to help.")

    st.subheader("Get Started")
    st.write(
        "To begin, select your languages from the dropdown menu and click the 'Start' button. Speak into your microphone, and watch as your words are translated in real-time!")

    st.subheader("Why Use Our Translator?")
    st.write("""
    - **Enhance Communication**: Break down language barriers and connect with people from around the world.
    - **Travel with Confidence**: Navigate new countries and cultures with ease.
    - **Boost Your Business**: Communicate effectively with international clients and partners.
    """)

    st.subheader("Join Our Community")
    st.write(
        "Follow us on social media for updates, tips, and user stories. Share your experiences and help us improve our service!")

    st.write("Ready to start translating? Click on the 'Translate' tab to begin your journey!")

# Translate page
if page == "Translate":
    st.title("Language Translator")
    # Dropdowns for selecting languages
    from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()))
    to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()))

    # Convert language names to language codes
    from_language = get_language_code(from_language_name)
    to_language = get_language_code(to_language_name)

    # Initialize session state for translation control
    if 'isTranslateOn' not in st.session_state:
        st.session_state.isTranslateOn = False

    # Button to trigger translation
    start_button = st.button("Start")
    stop_button = st.button("Stop")

    # Button for replaying the sound
    def play_sound():
        st.audio("cache_file.mp3", format="audio/mp3")

    if st.button("🔊"):
        play_sound()

    # Check if "Start" button is clicked
    if start_button:
        if not st.session_state.isTranslateOn:
            st.session_state.isTranslateOn = True
            output_placeholder = st.empty()
            output_placeholder.text(f"Starting translation from **{from_language_name}** to **{to_language_name}**...")
            main_process(output_placeholder, from_language, to_language)

    # Check if "Stop" button is clicked
    if stop_button:
        st.session_state.isTranslateOn = False
        st.write(f"Translation stopped. Last translation was from **{from_language_name}** to **{to_language_name}**.")

if page == "About":
        st.title("About Us")
        st.write(
            "Welcome to the Real-time Voice Translator application! This project aims to provide a seamless translation experience using voice input.")

        st.write("### Project Overview")
        st.write(
            "This application leverages advanced speech recognition and translation technologies to allow users to communicate in different languages effortlessly. "
            "Whether you're traveling, learning a new language, or communicating with friends, our tool is designed to help you bridge language barriers.")

        st.write("### Features")
        st.write("- Real-time voice translation")
        st.write("- Supports for multiple languages")
        st.write("- User-friendly interface")
        st.write("- Audio playback of translated text")

        st.write("### Team Members")
        st.write("This project is developed by:")


        # Create columns for team members
        col1, col2 = st.columns(2)

        with col1:
            st.image("profile.png", caption="Aneesh",
                     width=250)  # Replace with the correct image path
            st.write("")

        with col2:
            st.image("profile.png", caption="Aprameya",
                     width=250)  # Replace with the correct image path
            st.write("")

        col3, col4 =st.columns(2)

        with col3:
            st.image("profile.png", caption="Chiranth",
                     width=250)  # Replace with the correct image path
            st.write("")

        with col4:
            st.image("profile1.png", caption="Anushree",
                     width=250)  # Replace with the correct image path
            st.write("")

        # Display an image for the team working on the project
        # st.image("trial.png", caption="Team working on the project", width=400)
        # Save the resized image
        #img.save("resized_trial.png")

        st.write("### Contact Us")
        st.write(
            "For any inquiries or feedback, please reach out to us at: [sainapuraneesh@gmail.com](mailto:sainapuraneesh@gmail.com)")

if page == "Logout":
    st.title("Logout")
    st.write("")
    st.link_button("Logout", "http://localhost:63342/real-time-language-translator-main/soruce/login.html")



