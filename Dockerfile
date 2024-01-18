FROM python:3.10.12-alpine
LABEL maintainer="Mathias Artur Schulz <mathias@schulz.net.br>"

ENV MAIN_DIR="/twitter-bot"
# desabilita o buffering da saída do Python para garantir uma exibição imediata e sem atrasos
ENV PYTHONUNBUFFERED 1

WORKDIR ${MAIN_DIR}

COPY . ${MAIN_DIR}

RUN pip install -r requirements.txt

# instala o chromium para funcionar a lib python html2image
RUN apk add chromium

# roda o script python ao iniciar o container
CMD python create_apod_tweet.py
