import os, pyttsx3
from pathlib import Path
from speech_recognition import AudioFile, Recognizer


RECOGN  = Recognizer()
BASEDIR = "temp" 


def convert_wav_to_text(file: str):
    
    with AudioFile(file) as source:
        audio = RECOGN.record(source)
        text  = RECOGN.recognize_google(audio)

    return text

def convert_text_to_audio(text: str):

    filename = text + ".wav"
    filename = os.path.join(BASEDIR, filename)
    filepath = Path(filename)

    engine = pyttsx3.init()
    engine.save_to_file(text, filepath.as_posix())
    engine.runAndWait()
    engine.stop()

    return filename

def save_data_to_temp(file_binary, filename):

    file_location = os.path.join("temp", filename)
    with open(file_location, "wb+") as file_obj:
        file_obj.write(file_binary.file.read())

    return file_location