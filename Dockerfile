# DEVELOPMENT
FROM python:3.10.12-alpine as dev
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

# PRODUCTION
FROM python:3.10.12-alpine as prod
LABEL maintainer="Mathias Artur Schulz <mathias@schulz.net.br>"

ENV MAIN_DIR="/twitter-bot"
ENV CRON_DIR="/cron"
# desabilita o buffering da saída do Python para garantir uma exibição imediata e sem atrasos
ENV PYTHONUNBUFFERED 1

# cria pasta separada e arquivo para salvar os logs
RUN mkdir ${CRON_DIR}
RUN touch ${CRON_DIR}/crontab.log

WORKDIR ${MAIN_DIR}

COPY . ${MAIN_DIR}

RUN pip install -r requirements.txt

RUN apk add --no-cache tzdata
ENV TZ=America/Sao_Paulo

# instala o chromium para funcionar a geração de imagem
RUN apk add --no-cache chromium
RUN apk add --no-cache chromium-chromedriver

# cria o arquivo crontab e configura uma cronjob para executar um script python e redireciona a saída para o arquivo de logs
RUN echo "0 9 * * * cd ${MAIN_DIR} && python create_apod_tweet.py >> ${CRON_DIR}/crontab.log 2>&1" > ${CRON_DIR}/crontab

# lê o arquivo crontab e instala as configurações de cron
RUN crontab ${CRON_DIR}/crontab

# inicia o daemon cron e acompanha atualizações no arquivo de logs
CMD printf "Success\nWaiting for cronjobs...\n" && crond && tail -f ${CRON_DIR}/crontab.log
