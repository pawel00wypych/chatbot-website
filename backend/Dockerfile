FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .