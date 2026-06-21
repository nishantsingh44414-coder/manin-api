import os
import uuid
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Manim API Live on Render $7 plan 🚀", "port": os.environ.get("PORT")}

@app.post("/render")
def render_video(text: str = "Hello Bhai"):
    try:
        # Unique naam taaki file clash na ho
        scene_name = f"Scene_{uuid.uuid4().hex[:8]}"
        py_file = f"/tmp/{scene_name}.py"

        # Manim scene code
        scene_code = f'''
from manim import *

class {scene_name}(Scene):
    def construct(self):
        t = Text("{text}", font_size=60, color=WHITE)
        self.play(Write(t), run_time=2)
        self.wait(1)
        self.play(FadeOut(t), run_time=1)
'''

        # File bana de /tmp me - RAM me likhega, fast hoga
        with open(py_file, "w") as f:
            f.write(scene_code)

        # Manim render - quality low rakhi hai 2GB RAM ke liye
        cmd = f"manim -ql --media_dir /tmp {py_file} {scene_name}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)

        if result.returncode != 0:
            raise Exception(f"Manim Error: {result.stderr}")

        # Video ka path
        video_path = f"/tmp/videos/{scene_name}/ql/{scene_name}.mp4"

        if not os.path.exists(video_path):
            raise Exception("Video file ban hi nahi")

        return FileResponse(video_path, media_type="video/mp4", filename=f"{scene_name}.mp4")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, workers=1)
