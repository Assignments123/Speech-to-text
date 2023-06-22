import speech_recognition as sr
from flask import Flask ,request, render_template ,redirect, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import tempfile
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('audio.html')


@app.route("/stt", methods=["POST"])
def speech_to_text():
    audio_file = request.files['audio']
    
    audio_file.save(f"./audio/{audio_file.filename}")
    audio = AudioSegment.from_file(f"./audio/{audio_file.filename}")
    audio.export(f"./audio/processed/{audio_file.filename}", format='wav')
    
    # Perform speech-to-text processing using the converted audio file
    import speech_recognition as sr
    
    r = sr.Recognizer()
    with sr.AudioFile(f"./audio/processed/{audio_file.filename}") as source:
        audio = r.record(source)
    
    try:
        text = r.recognize_google(audio)
        # return jsonify({'text': text})
        print(text)
        return jsonify(text)
    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand the speech'})
    except sr.RequestError as e:
        return jsonify({'error': 'Error: {0}'.format(e)})


@app.route('/audio/',methods = ['POST']) 
def audio():
    """endpoint to save and generate transcript of the audio file sent from Client

        methods:
        -------
            POST

        parameter:
        ---------
            audio file
        
        returns:
        -------
            transcript of audio file
        raises:
        ------
            unknownvalueerror:
                if audio is not clear
                if audio language is not english
        
    """
    
    print("Inside audio")

    audio_file = request.files['audio']
    if audio_file.filename == "":
        return "no file available"

    # save the audio file sent by user
    audio_file.save(f"./audio/{audio_file.filename}")
    # read audio content of file and store it into a variable
    audio = AudioSegment.from_file(f"./audio/{audio_file.filename}")
    # export the audio data into another file and store that file in required extension 
    audio.export(f"./audio/processed/{audio_file.filename}", format='wav')

    try:
        # create object of speech recognizer
        recognizer = sr.Recognizer()
        # provide audio file of which we want to get transcript
        audioFile = sr.AudioFile(f"./audio/processed/{audio_file.filename}")
        # open the audio file 
        with audioFile as source:
            # record the audio and save it into variable
            data = recognizer.record(source)
        # get transcript of audio
        transcript = recognizer.recognize_google(data)
        print('transcript', transcript)
        return jsonify(transcript)

    except sr.UnknownValueError:
        return jsonify({'error': 'Could not understand the speech'})
    except sr.RequestError as e:
        return jsonify({'error': 'Error: {0}'.format(e)})



@app.route('/main/' , methods = ['GET','POST'])
def main():
    """endpoint for accepting user input as voice and print transcript of the audio
        this works with console only 
    """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("say something")

        audio = r.listen(source)

        try:
            print("You have said "  + r.recognize_google(audio))

        except Exception:

            print("Exception occured")


if __name__ == "__main__":
    app.run(debug = True)