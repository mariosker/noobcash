FROM python:3.10-slim-buster

WORKDIR /noobcash

COPY ./backend/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ./


CMD [ "python3", "backend/app.py"]