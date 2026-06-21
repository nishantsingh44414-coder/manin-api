import os
import subprocess
import uuid
import requests
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse
from moviepy.editor import VideoFileClip, AudioFileClip

app = FastAPI(title="Manim Video API")

OUTPUT_DIR = "/tmp/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/render")
async def render_video(
    code: str = Form(...),
    script: str = Form(...),
    audio_url: str = Form(...)
):
    job_id = str(uuid.uuid4())
    manim_file = f"/tmp/{job_id}.py"
    audio_path = f"/tmp/{job_id}_audio.mp3"
    final_path = f"{OUTPUT_DIR}/{job_id}_final.mp4"

    try:
        # 1. Manim code save - Class naam GeneratedScene hona chahiye
        with open(manim_file, "w") as f:
            f.write(code)

        # 2. Audio download 11labs se
        audio_resp = requests.get(audio_url, timeout=30)
        audio_resp.raise_for_status()
        with open(audio_path, 'wb') as f:
            f.write(audio_resp.content)

        # 3. Manim render -ql = low quality, fast render
        cmd = ["manim", "-ql", "--media_dir", "/tmp/media", manim_file, "GeneratedScene"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

        if result.returncode!= 0:
            return JSONResponse(status_code=500, content={"error": "Manim failed", "log": result.stderr})

        # 4. Video file ka path
        rendered_video = f"/tmp/media/videos/{job_id}/480p15/GeneratedScene.mp4"
        if not os.path.exists(rendered_video):
            return JSONResponse(status_code=500, content={"error": "Video not found after render"})

        # 5. Audio + Video merge
        video_clip = VideoFileClip(rendered_video)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile(final_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        return FileResponse(final_path, media_type="video/mp4", filename="video.mp4")

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def read_root():
    return {"status": "API running"}
