# pull official base image
FROM python:3.10-slim-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy requirements file
COPY ./Pipfile .
COPY ./Pipfile.lock .

# install dependencies
RUN python3 -m pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

# copy project
COPY . .