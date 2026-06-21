FROM manimcommunity/manim:stable

USER root
WORKDIR /app


RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt


COPY. /app


CMD python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT}
