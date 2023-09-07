FROM python:3.10-slim-buster
LABEL org.opencontainers.image.source="https://github.com/TimeSurgeLabe/htmxgpt"
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# run app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
