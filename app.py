import json, uvicorn
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, Request

from core.utils import *
from core.secret import Encrypt
from core.compare import find_closest


PATH = "local/db.json"

app = FastAPI()
enc = Encrypt()

@app.post("/upload/data")
async def upload_data(request: Request):
    """
    NOTE: payload body.
    {
        "keyword" : [..., ...]
    }
    """
    
    # load database keyword.
    DATABASE = json.load(open(PATH, "r"))

    # get payload
    result = await request.json()

    if "keyword" in result.keys(): 
        DATABASE[0]["keyword"] += result["keyword"]
        
        # update database.
        json.dump(DATABASE, open(PATH, "w"))

        return {"status_code" : 200, "message" : "Success."}

    else: 
        return {"status_code" : 404, "message" : "Failed! keyword not exist in object data."}

@app.post("/upload/audio")
async def upload_file(file: UploadFile):
    
    # load database keyword.
    DATABASE = json.load(open(PATH, "r"))[0]["keyword"]   

    # save file into temporary folder.
    file_location = save_data_to_temp(file, file.filename)

    # get text based on temporary audio file.
    speech_text = convert_wav_to_text(file_location)
    speech_text = speech_text.lower()

    # get nearest similar word.
    result_similar = find_closest(speech_text, DATABASE)
    if len(result_similar) == 0:
        result_similar = [speech_text]

    # convert result_similar into file object of audio.
    filename = convert_text_to_audio(result_similar[0])

    return {"status_code" : 200, "message" : "Success.", "data" : {"token" : enc.encode(filename)}}

@app.get("/audio/{token}")
async def get_audio_file(token: str): 

    filename = enc.decode(token)
    filepath = Path(filename)

    return FileResponse(filepath.as_posix(), filename = filename)


if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host = "0.0.0.0", 
        port = 8080, 
        reload = True, 
        debug = True
    )