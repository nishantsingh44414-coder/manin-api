from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import subprocess
import os
import uuid

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Manim API Live on Render $7 plan 🚀"}

@app.post("/render")
def render_video(text: str = "Hello Bhai"):
    try:
        scene_name = f"Scene_{uuid.uuid4().hex[:8]}"
        py_file = f"{scene_name}.py"

        scene_code = f'''
from manim import *

class {scene_name}(Scene):
    def construct(self):
        t = Text("{text}").scale(1.5)
        self.play(Write(t))
        self.wait(1)
        self.play(FadeOut(t))
'''

        with open(py_file, "w") as f:
            f.write(scene_code)

        cmd = f"manim -ql --media_dir /tmp {py_file} {scene_name}"
        subprocess.run(cmd, shell=True, check=True, timeout=120)

        video_path = f"/tmp/videos/{py_file.replace('.py','')}/ql/{scene_name}.mp4"
        return FileResponse(video_path, media_type="video/mp4", filename="video.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
