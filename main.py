import os
import subprocess
import shutil
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Manim Video Generation API")

# Folder setup
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/render")
async def render_video(
    code: str = Form(...),
    script: str = Form(...),
    audio_url: str = Form(...)
):
    try:
        # 1. Manim Code ko file mein save karein
        manim_file = "scene.py"
        with open(manim_file, "w") as f:
            f.write(code)

        # 2. Manim se video render karein (command execute karein)
        # Note: Render server par Manim installed hona chahiye
        cmd = ["manim", "-pql", manim_file, "MyScene"] 
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=result.stderr)

        # 3. Yahan logic add karein jo audio_url download karke video ke sath merge kare (moviepy use karein)
        # Filhal ke liye hum seedha response bhej rahe hain
        
        return {"status": "success", "message": "Video rendered successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "API is running"}
