import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Initialize environment vectors safely
load_dotenv()

from models.request import OrganizedBrainDump
from services.planner import process_voice_brain_dump, process_text_brain_dump

app = FastAPI(title="AI Hybrid Voice & Text Brain-Dump Engine")

TEMP_DIR = "temp_audio"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.post("/api/process-voice", response_model=OrganizedBrainDump)
async def handle_voice_processing(file: UploadFile = File(...)):
    """Handles incoming raw microphone audio files, processes, and purges the file artifact."""
    suffix = os.path.splitext(file.filename)[1] if file.filename else ".webm"
    temp_file_path = os.path.join(TEMP_DIR, f"upload_{os.getpid()}{suffix}")

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return process_voice_brain_dump(temp_file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/api/process-text", response_model=OrganizedBrainDump)
async def handle_text_processing(payload: dict = Body(...)):
    """Accepts manual text payloads directly from the frontend interface input box."""
    raw_text = payload.get("text", "").strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Text payload cannot be empty.")
    
    try:
        return process_text_brain_dump(raw_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static frontend architecture views
app.mount("/", StaticFiles(directory="static", html=True), name="static")