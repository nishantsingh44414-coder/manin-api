FROM manimcommunity/manim:stable

# Switch to root to install dependencies and system tools
USER root

# Install FastAPI, Uvicorn for the server, and clean up cache
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Create and set the working directory
WORKDIR /app

# Copy application files into the container
COPY . /app

# Expose the internal port FastAPI will run on
EXPOSE 8080

# Run the Uvicorn server on container startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
