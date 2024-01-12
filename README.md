# twitter-space-rover-bot

O Twitter Space Rover Bot é um bot automatizado que compartilha imagens astronômicas da NASA no Twitter. O Bot utiliza a [API da Nasa](https://api.nasa.gov) para obter diariamente o Astronomy Picture of the Day (APOD) e compartilha no Twitter.

[Link para o Bot 🤖](https://x.com/SpaceRoverBot)

Este projeto foi desenvolvido para entusiastas da astronomia que desejam explorar diariamente imagens e informações sobre o universo.

## Exemplos de Consulta na API da NASA

APOD (Astronomy Picture of the Day) do dia de hoje:

<https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY>

APOD (Astronomy Picture of the Day) dos dias de 01 de Janeiro de 2024 até 12 de Janeiro de 2024:

<https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=2024-01-01&end_date=2024-01-12>

## Rodar o projeto

Antes de começar, certifique-se de ter as seguintes ferramentas e acessos:

- Python 3.10
- Conta no Twitter para construção do Bot
- Chave de acesso a [API do Twitter](https://developer.twitter.com/en/docs/twitter-api) e ao [Twitter Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps)
- Chave de acesso a [API da Nasa](https://api.nasa.gov)

### Instalar o Python 3.10

Caso vocês não possua o Python na versão 3.10 instalado você pode rodar os seguintes comandos para instalar:

```bash
sudo add-apt-repository universe
sudo apt-get update
sudo apt install python3.10 python3.10-dev python3.10-venv
```

### Virtual Environment

O projeto foi construído utilizando **Virtual Environment** (`Python venv`) para isolar as dependências do projeto, o que permite que diferentes projetos tenham suas próprias versões específicas de bibliotecas e evitando conflitos entre eles.

#### Criar uma venv

Rode o seguinte comando na pasta principal do projeto para criar a **venv** com o **Python 3.10**:

```bash
virtualenv venv --python=python3.10
```

Após criar a **venv** apenas é necessário ativa-lá:

```bash
source venv/bin/activate
```

Em seguida instale as dependências do projeto na **venv** e a venv estará pronta para uso:

```bash
pip install -r requirements.txt
```

#### Ativar a venv

Lembresse que sempre que um **novo terminal** for aberto para executar o projeto é necessário **ativar** a **venv** com o seguinte comando:

```bash
source venv/bin/activate
```

#### Nova dependência

Para salvar uma nova dependências do projeto utilize o sequinte comando e o `requirements.txt` será atualizado:

```bash
pip freeze > requirements.txt
```

### Bibliotecas utilizadas

Algumas bibliotecas instaladas para construção do projeto.

#### Tradução do texto

O texto é traduzido utilizando a biblioteca python [deep-translator](https://github.com/nidhaloff/deep-translator).

#### Geração de imagem

As imagens são geradas utilizando a biblioteca python [html2image](https://github.com/vgalin/html2image).

## Licença

Este projeto está sob a licença MIT, que pode ser encontrada em LICENSE.

## Contribuições

Contribuições são bem-vindas! Se você quiser contribuir para este projeto, por favor, abra uma issue ou envie uma solicitação de pull request.
