from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import pyaudio
import wave

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    audio_file = request.files['audio']
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        # Attempt to recognize speech in English
        text = recognizer.recognize_google(audio, language="en-IN")
    except sr.UnknownValueError:
        try:
            # If English fails, attempt Hindi
            text = recognizer.recognize_google(audio, language="hi-IN")
        except sr.UnknownValueError:
            text = "Could not understand audio"
    except sr.RequestError:
        text = "Could not request results from the speech recognition service"
    
    return jsonify({'transcription': text})

if __name__ == '__main__':
    app.run(debug=True)
