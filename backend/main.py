from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from faster_whisper import WhisperModel
import shutil, os

app = FastAPI()
model = WhisperModel("base")  # "tiny" でもOK

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...)):
    os.makedirs("temp_audio", exist_ok=True)
    filepath = f"temp_audio/{file.filename}"

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    return JSONResponse({
        "filename": file.filename
    })

@app.get("/transcribe/{filename}")
async def transcribe_audio(filename: str):
    filepath = f"temp_audio/{filename}"
    if not os.path.exists(filepath):
        return JSONResponse({"error": "File not found"}, status_code=404)

    segments, _ = model.transcribe(filepath)
    transcription = "".join(seg.text for seg in segments)

    return JSONResponse({
        "transcription": transcription
    })

app.mount("/temp_audio", StaticFiles(directory="temp_audio"), name="temp_audio")
