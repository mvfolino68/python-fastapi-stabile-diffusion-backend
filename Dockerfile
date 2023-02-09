FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
# Image from dockerhub


ENV PYTHONUNBUFFERED 1 
# Expose the port 8000 in which our application runs

WORKDIR /app
# Make /app as a working directory in the container

COPY ./image ./image
COPY ./.env . 
# Copy everything from ./src directory to /app in the container

COPY ./requirements.txt .
RUN pip install -r requirements.txt 
# Install the dependencies

EXPOSE 8000
# Expose the required port

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "image.main:app"]
# Run the application in the port 8000
