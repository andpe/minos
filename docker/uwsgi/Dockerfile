FROM debian:latest

ENV HOME /minos
WORKDIR /minos

RUN apt-get update && apt-get install -y uwsgi uwsgi-plugin-python3 python3-pip

ADD ./requirements.txt /

RUN python3 -m pip install -r /requirements.txt

EXPOSE 8005

CMD ["uwsgi", "--plugin", "python3", "--wsgi-file", "minos.py", "--callable", "app", "--processes", "1", "--threads", "8", "--socket", "0.0.0.0:8005", "--py-autoreload=5"]