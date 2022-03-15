# pull official base image
FROM python:3.10-alpine

WORKDIR /code

COPY ./requirements.txt /code


RUN pip3 install -r requirements.txt

EXPOSE 8000

COPY . /code


# install dependencies