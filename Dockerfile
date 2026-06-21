FROM manimcommunity/manim:stable

USER root
RUN pip install --no-cache-dir fastapi uvicorn pydantic python-multipart moviepy requests

WORKDIR /app
COPY . /app
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
