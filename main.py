import speech_recognition as sr
from flask import Flask ,request, render_template ,redirect
from werkzeug.utils import secure_filename
# from google.cloud import speech
# from pydub import AudioSegment
# import mimetypes
# import subprocess
import tempfile

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('audio.html')



@app.route('/audio/',methods = ['POST']) 
def audio():
    """endpoint to save and generate transcript of the audio file sent from Client

        methods:
            POST

        arguments:
            audio file
        
        returns:
            transcript of audio file
        
    """
    
    print("Inside audio")

    # tried another ways to store the file so that it wont get corrupted
    # audio_file = request.files['audio'].read()

    # mp3_audio_file = "C:/Users/manoj.kanadi/manoj/speech to text/recording3.mp3"


    # with open(mp3_audio_file, 'wb') as f:
    #     f.write(audio_file)


    audio_file = request.files['audio']
    if audio_file.filename == "":
        return "no file available"
    # filename = audio_file.filename
    filename = secure_filename(audio_file.filename)
    print("filename is ",filename)
    filetype = audio_file.content_type
    print("type of file ", filetype)

   

    # Save the audio file to a temporary location

    # with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:

    #     temp_path = temp_file.name

    #     audio_file.save(temp_path)
    
    # while storing file sent from UI its getting corrupted and thats why not getting transcripted
    # audio_file.save("C:/Users/manoj.kanadi/manoj/speech to text/Speech-to-text/recording.wav")
    # audio_file.save(path)

    path = f"C:/Users/manoj.kanadi/manoj/speech to text/Speech-to-text/{filename}"
    audio_file.save(path,buffer_size=16384)
    # audio_file = "C:/Users/manoj.kanadi/manoj/speech to text/Speech-to-text/recording.wav"


    # to store wav file into mp3 format.
    # mp3_audio_file = "C:/Users/manoj.kanadi/manoj/speech to text/recording2.mp3"
    # audio = AudioSegment.from_wav(audio_file)
    # audio.export(mp3_audio_file, format='mp3')


    if "audio" not in request.files:
            return redirect(request.url)
    
    # audio_file = "C:/Users/manoj.kanadi/manoj/speech to text/Speech-to-text/OSR_us_000_0011_8k.wav"

# the function is able to generate transcript of file stored locally but is 
# when accessing file sent from html page its not able to access those files
    if audio_file:
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile(audio_file)
        with audioFile as source:
            data = recognizer.record(source)
        transcript = recognizer.recognize_google(data, key=None)
        # print(transcript)

    # tried to open file with different modes while saved in different extension i.e. wav
    # recognizer = sr.Recognizer()
    # with wave.open(audio_file, 'rb') as wav_file:
    #     frames = wav_file.readframes(wav_file.getnframes())

    # transcript = recognizer.recognize_google(frames)


    print('transcript', transcript)


    return render_template('audio.html')



@app.route('/main/' , methods = ['GET','POST'])
def main():
    """endpoint for accepting user input as voice and print transcript of the audio
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