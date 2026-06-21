FROM manimcommunity/manim:stable

USER root
WORKDIR /app

# ffmpeg + sab python package ek saath install
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install --no-cache-dir fastapi uvicorn[standard] pydantic python-multipart moviepy requests

# App code copy
COPY. /app

# python3 -m uvicorn = direct module chalega
CMD python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT}
