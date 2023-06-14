import speech_recognition as sr
from flask import Flask ,request, render_template ,redirect
# from google.cloud import speech
from pydub import AudioSegment
# import subprocess


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('audio.html')



@app.route('/audio/',methods = ['POST']) 
def audio():
    
    print("Inside audio")

    # tried another ways to store the file so that it wont get corrupted
    # file_path = request.files['audio'].read()

    # mp3_file_path = "C:/Users/manoj.kanadi/manoj/speech to text/recording3.mp3"


    # with open(mp3_file_path, 'wb') as f:
    #     f.write(file_path)


    file_path = request.files['audio']
    if file_path.filename == "":
        return "no file available"
    filetype = file_path.content_type
    print("type of file ", filetype)

    # while storing file sent from UI its getting corrupted and thats why not getting transcripted
    file_path.save("C:/Users/manoj.kanadi/manoj/speech to text/recording.wav")
    file_path = "C:/Users/manoj.kanadi/manoj/speech to text/recording.mp3"


    mp3_file_path = "C:/Users/manoj.kanadi/manoj/speech to text/recording2.mp3"
    audio = AudioSegment.from_wav(file_path)
    audio.export(mp3_file_path, format='mp3')


    if "audio" not in request.files:
            return redirect(request.url)
    
    file_path = "C:/Users/manoj.kanadi/manoj/speech to text/OSR_us_000_0011_8k.wav"

# the function is able to generate transcript of file stored locally but is 
# when accessing file sent from html page its not able to access those files
    if file_path:
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile(file_path)
        with audioFile as source:
            data = recognizer.record(source)
        transcript = recognizer.recognize_google(data, key=None)
        print(transcript)

    # tried to open file with different modes while saved in different extension i.e. wav
    # recognizer = sr.Recognizer()
    # with wave.open(file_path, 'rb') as wav_file:
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