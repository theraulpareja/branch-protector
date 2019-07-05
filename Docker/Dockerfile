# Image for the flask application

FROM python:3.7-alpine
MAINTAINER raul.pareja@gmail.com

COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN mkdir -p /opt/local

COPY app-branch-protector /opt/local/app-branch-protector
COPY conf /opt/local/conf
COPY payloads /opt/local/payloads

WORKDIR /opt/local/app-branch-protector

CMD ["flask", "run", "--host=0.0.0.0"]