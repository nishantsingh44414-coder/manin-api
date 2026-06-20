import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from moviepy.editor import VideoFileClip, AudioFileClip

app = FastAPI()

class VideoRequest(BaseModel):
    python_code: str
    audio_url: str

@app.post("/generate-video")
async def generate_video(request: VideoRequest):
    # Purane files delete karne ke liye
    for f in ["MainScene.mp4", "input_code.py", "final_output.mp4"]:
        if os.path.exists(f): os.remove(f)

    # Code save karne ke liye
    with open("input_code.py", "w") as f:
        f.write(request.python_code)

    # Video banane ke liye command
    manim_command = ["manim", "-ql", "input_code.py", "MainScene", "--media_dir", ".", "--custom_folders"]
    
    try:
        subprocess.run(manim_command, check=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Manim render failed")

    return {"status": "success", "message": "Video Ready!"}
