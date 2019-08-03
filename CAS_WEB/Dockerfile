# Pull base image
FROM python:3.7-alpine

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Open port 8000 for serving the webservice
EXPOSE 8000

# Copy project
COPY . /code/

# Start the utils
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
