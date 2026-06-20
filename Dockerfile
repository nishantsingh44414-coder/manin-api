FROM manimcommunity/manim:stable
WORKDIR /app
COPY main.py .
RUN pip install fastapi uvicorn moviepy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
