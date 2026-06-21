FROM manimcommunity/manim:stable

USER root
WORKDIR /app

# pip upgrade + packages install
RUN python3 -m pip install --upgrade pip
COPY requirements.txt.
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# App code copy
COPY..

# $PORT Render deta hai, shell format zaruri hai
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
