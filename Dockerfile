FROM python:3.9

# Install dependencies
RUN apt-get update -y && apt-get install -y python3-pip python3-dev build-essential

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy application code
COPY src/ /root/src/
WORKDIR /root/src/flask_website/

# Run the Flask app
CMD ["python", "app.py"]