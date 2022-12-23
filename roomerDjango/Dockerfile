FROM python:3.8-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ADD requirements.txt /requirements.txt
RUN pip3.8 install -r /requirements.txt && rm -f /requirements.txt
ADD code /code
WORKDIR /code