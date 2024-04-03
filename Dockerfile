FROM python:3.12-alpine
LABEL authors="danil"

WORKDIR ./tutoring_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements-linux.txt
