FROM python:3.12-slim-bookworm AS base

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
    pip install --user -r requirements.txt

COPY aws.py aws.py

RUN apt-get update \
    && apt-get install -y binutils \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt /var/lib/dpkg /tmp/* /var/tmp/* \
    && python3 -m PyInstaller --onefile --noconfirm --clean --name aps aws.py


FROM ubuntu:24.04 AS final

ARG UID

LABEL author="Ivan Medaev" \
    language="python" \
    tool="aps" \
    version="3.12"

ENV ID=${UID}
ENV USER=ubuntu
ENV GROUP=ubuntu

WORKDIR /app

RUN mkdir -p /home/${USER}/.aws && \
    chown -R ${USER}:${GROUP} /app /home/${USER}/.aws/

COPY --from=base --chown=${USER}:${GROUP} /app/dist/aps .

USER ${USER}
