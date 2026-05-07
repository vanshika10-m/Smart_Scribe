from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import time

app = Flask(__name__)


# TEXT TO SPEECH FUNCTION
def speak_text(text, lang):

    try:

        tts = gTTS(
            text=text,
            lang=lang
        )

        # UNIQUE AUDIO FILE NAME
        filename = f"static/voice_{int(time.time())}.mp3"

        tts.save(filename)

        return filename

    except Exception as e:

        print("Speech Error:", e)

        return None


# HOME PAGE
@app.route('/')
def home():

    return render_template('index.html')


# TRANSLATION ROUTE
@app.route('/translate', methods=['POST'])
def translate_text():

    text = request.form['text']

    lang = request.form['lang']

    # TRANSLATE TEXT
    translated = GoogleTranslator(
        source='auto',
        target=lang
    ).translate(text)

    # GENERATE AUDIO
    audio_file = speak_text(translated, lang)

    return jsonify({

        'translated': translated,

        'audio': audio_file
    })


if __name__ == '__main__':

    app.run(debug=True)