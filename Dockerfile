FROM python:3.6.2

ENV PYTHONUNBUFFERED 1
CMD mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/