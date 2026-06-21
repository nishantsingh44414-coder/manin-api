FROM manimcommunity/manim:stable

USER root
WORKDIR /app


RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*


RUN python3 -m pip install --upgrade pip --no-cache-dir \
    && python3 -m pip install --no-cache-dir fastapi uvicorn[standard] pydantic python-multipart moviepy requests
COPY. /app

EXPOSE 10000

CMD echo "PORT is: $PORT" && python3 -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000} --log-level debug
