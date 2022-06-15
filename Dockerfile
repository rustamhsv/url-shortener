# Pull base image
FROM python:3.8-slim-buster

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# install psycopg2
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy project
COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]