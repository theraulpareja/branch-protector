# Image for the flask application

FROM python:3.7-alpine
MAINTAINER raul.pareja@gmail.com

# COPY ../../app-branch-protector/ /app
# COPY ../../conf /
# COPY ../../payloads /
# COPY ../../requirements.txt /

COPY requirements.txt /
RUN pip install -r /requirements.txt

# Adding a non root user best practice as principle of least privilege
# RUN addgroup -g 1001 flaskhook && \
#    adduser -D -u 1001 -G flaskhook flaskhook

# USER flaskhook

RUN mkdir -p /usr/local/{app-branch-protector,conf,payloads}

COPY app-branch-protector /usr/local/app-branch-protector
COPY conf /usr/local/conf
COPY payloads /usr/local/payloads

WORKDIR /usr/local/


CMD ["gunicorn", "-w 4", "main:app"]