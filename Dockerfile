FROM python:3.10.12-alpine
LABEL maintainer="Mathias Artur Schulz <mathias@schulz.net.br>"

ENV MAIN_DIR="/twitter-bot"
# desabilita o buffering da saída do Python para garantir uma exibição imediata e sem atrasos
ENV PYTHONUNBUFFERED 1

WORKDIR ${MAIN_DIR}

COPY . ${MAIN_DIR}

RUN pip install -r requirements.txt

RUN apk add --no-cache tzdata
ENV TZ=America/Sao_Paulo

# instala o chromium para funcionar a geração de imagem
RUN apk add --no-cache chromium
RUN apk add --no-cache chromium-chromedriver

# roda o script python ao iniciar o container
CMD python create_apod_tweet.py
