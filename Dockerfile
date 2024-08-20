FROM python:3.11-slim-bookworm AS BASE

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


FROM ubuntu:22.04 AS FINAL

ARG UID

LABEL author="Ivan Medaev" \
      language="python" \
      tool="asp" \
      version="3.11"

ENV ID=${UID}
ENV USER=awstool
ENV GROUP=awstool

WORKDIR /app

RUN groupadd -g ${ID} ${GROUP} && \
    useradd -r -m -u ${ID} -g ${GROUP} ${USER} && \
    mkdir -p /home/${USER}/.aws && \
    chown -R ${USER}:${GROUP} /app /home/${USER}/.aws/

COPY --from=base --chown=${USER}:${GROUP} /app/dist/aps .

USER ${USER}
