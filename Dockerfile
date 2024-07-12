FROM python:3.11-slim-bookworm

ARG UID

LABEL author="Ivan Medaev" \
      tool="aws" \
      language="python" \
      version="3.11"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV ID=$UID
ENV USER=awstool
ENV GROUP=awstool

WORKDIR /app

COPY aws.py aws.py

RUN groupadd -g $ID $GROUP && \
    useradd -r -m -u $ID -g $GROUP $USER && \
    mkdir -p /home/$USER/.aws && \
    chown -R $USER:$GROUP /app /home/$USER/.aws/

USER $USER

CMD [ "python3" ]
