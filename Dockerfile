FROM python:3.10.12-alpine
LABEL maintainer="Mathias Artur Schulz <mathias@schulz.net.br>"

# Garante que a saída do Python seja enviada diretamente para o terminal (por exemplo, seu log de contêiner) sem ser
# primeiro armazenado em buffer e que você possa ver a saída de seu aplicativo em tempo real
# Isso também garante que nenhuma saída parcial seja mantida em um buffer em algum lugar e nunca seja gravada no caso de o aplicativo Python travar
ENV PYTHONUNBUFFERED 1

WORKDIR /services/schulz/twitter-bot

COPY . /services/schulz/twitter-bot

RUN pip install -r requirements.txt

# instala o chromium para funcionar a lib python html2image
RUN apk add chromium

# comando que roda toda vez que o container for iniciar
CMD python3 create_apod_tweet.py
