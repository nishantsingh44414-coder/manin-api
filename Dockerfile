FROM manimcommunity/manim:stable

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.txt .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
