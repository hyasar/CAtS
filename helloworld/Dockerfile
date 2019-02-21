# Pull base image
FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Open port 8000 for serving the webservice
EXPOSE 8000

# Copy project
COPY . /code/

# Start the service
# CMD ["python3", "manage.py", "runserver 0.0.0.0:8000"]
