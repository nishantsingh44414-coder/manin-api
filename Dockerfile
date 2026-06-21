FROM manimcommunity/manim:stable


USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app


COPY requirements.txt .


RUN PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 \
    pip install --no-cache-dir -r requirements.txt


COPY . .


ENV PORT=8000
EXPOSE 8000


CMD uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
