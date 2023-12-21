# twitter-space-rover-bot

[Twitter Space Rover Bot 🤖](https://x.com/SpaceRoverBot)

[Twitter Developers Dashboard](https://developer.twitter.com/en/portal/projects-and-apps)

[API da Nasa](https://api.nasa.gov)

A API da NASA permite no máximo 1000 requests por hora.

Exemplo de consulta na API:

APOD (Astronomy Picture of the Day):

<https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY>

Exemplo de consulta do dia 08 de Dezembro de 2023 até 12 de Dezembro de 2023:

<https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=2023-12-08&end_date=2023-12-12>

## venv

Python 3.10: `sudo apt install python3.10`

Criar a venv: `virtualenv venv --python=python3.10`

Ativar venv: `source venv/bin/activate`

Desativar venv: `deactivate`

Salvar as dependências do projeto: `pip freeze > requirements.txt`

Instalar as dependências: `pip install -r requirements.txt`

## Translator

O texto é traduzido utilizando a biblioteca python [deep-translator](https://github.com/nidhaloff/deep-translator).

## Image generator

As imagens são geradas utilizando a biblioteca python [html2image](https://github.com/vgalin/html2image)
