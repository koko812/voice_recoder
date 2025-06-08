from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ← 追加
import shutil, os
from faster_whisper import WhisperModel


model = WhisperModel("base")  # "tiny" でもOK


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

    # ↓ 実際の文字起こし処理
    segments, _ = model.transcribe(filepath)
    transcription = "".join([seg.text for seg in segments])
    score = 87.3

    return JSONResponse({
        "filename": file.filename,
        "transcription": transcription,
        "score": score
    })

# これを追加！
app.mount("/temp_audio", StaticFiles(directory="temp_audio"), name="temp_audio")
