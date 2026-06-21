FROM manimcommunity/manim:stable

USER root
WORKDIR /app

# 1. pip upgrade kar - Manim image me purana hota hai
RUN python3 -m pip install --upgrade pip

# 2. requirements copy karke install
COPY requirements.txt.
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# 3. App code copy
COPY. /app

# 4. Shell CMD taaki $PORT expand ho
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
