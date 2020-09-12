FROM python:3.7-slim-buster

RUN useradd -ms /bin/bash  flaskapp
RUN apt-get update -qq
RUN apt-get install -y -qq gcc make
RUN apt-get install nano

WORKDIR /home/flaskapp

COPY requirements.txt requirements.txt
RUN python3 -m venv venv

RUN venv/bin/pip install scipy
RUN venv/bin/pip install cython
RUN venv/bin/pip install gunicorn 
RUN venv/bin/pip install -r requirements.txt

COPY app.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R flaskapp:flaskapp ./
USER flaskapp

EXPOSE 8000
ENTRYPOINT ["./boot.sh"]
