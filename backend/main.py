from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil, os

app = FastAPI()

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

    transcription = "This is a dummy transcription."
    score = 87.3

    return JSONResponse({
        "filename": file.filename,
        "transcription": transcription,
        "score": score
    })
