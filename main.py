from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import os

app = Flask(__name__)


# TEXT TO SPEECH FUNCTION
def speak_text(text, lang):

    try:

        tts = gTTS(
            text=text,
            lang=lang
        )

        filename = "voice.mp3"

        tts.save(filename)

        playsound(filename)

        os.remove(filename)

    except Exception as e:

        print("Speech Error:", e)


# HOME PAGE
@app.route('/')
def home():

    return render_template('index.html')


# TRANSLATION ROUTE
@app.route('/translate', methods=['POST'])
def translate_text():

    text = request.form['text']

    lang = request.form['lang']

    translated = GoogleTranslator(
        source='auto',
        target=lang
    ).translate(text)

    # SPEAK TRANSLATED TEXT
    speak_text(translated, lang)

    return jsonify({
        'translated': translated
    })


# VOICE INPUT ROUTE
@app.route('/voice', methods=['GET'])
def voice_input():

    recognizer = sr.Recognizer()

    try:

        with sr.Microphone() as source:

            print("Listening...")

            recognizer.adjust_for_ambient_noise(source)

            audio = recognizer.listen(source)

            text = recognizer.recognize_google(audio)

            return jsonify({
                'text': text
            })

    except Exception as e:

        return jsonify({
            'text': 'Error: ' + str(e)
        })


if __name__ == '__main__':

    app.run(debug=True)