FROM manimcommunity/manim:stable

USER root
WORKDIR /app
COPY . /app


CMD uvicorn main:app --host 0.0.0.0 --port $PORT
