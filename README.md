# twitter-space-rover-bot

O Twitter Space Rover Bot 🚀✨ é um bot automatizado que compartilha imagens astronômicas da NASA no Twitter. O Bot utiliza a [API da Nasa](https://api.nasa.gov) 🔭 para obter diariamente a Foto Astronômica do Dia (APOD - Astronomy Picture of the Day) e compartilha no Twitter.

Além publicar a imagem do dia, o bot também realiza uma publicação da explicação da imagem já traduzido em Português.

[Link para o Bot 🤖](https://x.com/SpaceRoverBot)

Este projeto foi desenvolvido para entusiastas da astronomia que desejam explorar diariamente imagens e informações sobre o universo 🪐.

## Executar o projeto

Antes de começar, certifique-se de ter os seguintes acessos:

- Conta no Twitter para construção do Bot
- Chave de acesso a [API do Twitter](https://developer.twitter.com/en/docs/twitter-api) e ao [Twitter Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps)
- Chave de acesso a [API da Nasa](https://api.nasa.gov)

Após obter os acessos é necessário criar o arquivo  `.env` e configurar as variáveis de ambiente de acordo com o descrito no arquivo `.env.example` para a correta execução da aplicação.

A aplicação pode ser executada de duas maneiras, que são explicadas abaixo.

### Executar o projeto com Docker

O **Docker** é uma plataforma projetada para facilitar a criação, implantação e execução de aplicativos, garantindo consistência entre diferentes ambientes, desde o desenvolvimento até a produção. Com o Docker é possível encapsular um aplicativo e suas dependências em um contêiner, que inclui tudo o que é necessário para a execução do aplicativo.

Com o docker apenas é necessário rodar o seguinte comando para executar a aplicação:

```bash
docker-compose up
```

### Executar o projeto com Virtual Environment

Uma **Virtual Environment** (`Python venv`) permite isolar as dependências do projeto, o que permite que diferentes projetos tenham suas próprias versões específicas de bibliotecas e evitando conflitos entre eles.

A **venv** utilizada neste projeto foi baseada no Python na versão 3.10.

#### Instalar o Python 3.10

Caso vocês não possua o Python na versão 3.10 instalado você pode rodar os seguintes comandos para instalar:

```bash
sudo add-apt-repository universe
sudo apt-get update
sudo apt install python3.10 python3.10-dev python3.10-venv
```

#### Criar uma venv

Rode o seguinte comando na pasta principal do projeto para criar a **venv** com o **Python 3.10**:

```bash
virtualenv venv --python=python3.10
```

Após criar a **venv** apenas é necessário ativa-lá:

```bash
source venv/bin/activate
```

Em seguida instale as dependências do projeto na **venv** e a **venv** estará pronta para uso:

```bash
pip install -r requirements.txt
```

#### Ativar a venv

Lembresse que sempre que um **novo terminal** for aberto para executar o projeto é necessário **ativar** a **venv** com o seguinte comando:

```bash
source venv/bin/activate
```

## Nova dependência

Para salvar uma nova dependências do projeto utilize o sequinte comando e o `requirements.txt` será atualizado:

```bash
pip freeze > requirements.txt
```

## Bibliotecas utilizadas

Algumas bibliotecas instaladas para construção do projeto.

### Tradução do texto

O texto é traduzido utilizando a biblioteca python [deep-translator](https://github.com/nidhaloff/deep-translator).

### Geração de imagem

As imagens da explicação são geradas utilizando a biblioteca python [html2image](https://github.com/vgalin/html2image).

## Exemplos de Consulta na API da NASA

Exemplo de request GET para consulta do APOD (Astronomy Picture of the Day) do dia de hoje:

> <https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY>

Exemplo de request GET para consulta do APOD (Astronomy Picture of the Day) dos dias de 01 de Janeiro de 2024 até 12 de Janeiro de 2024:

> <https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=2024-01-01&end_date=2024-01-12>

## Ambiente de Produção

A aplicação está rodando em produção com uma máquina **t2.micro** da **EC2** (Amazon Elastic Compute Cloud) **AWS** (Amazon Web Services), utilizando como base os arquivos `docker-compose.prod.yml` e `Dockerfile.prod`.

O principal motivo para escolha do serviço EC2 foi para aprender a utilizar uma poderosa ferramenta disponibilizada pela AWS.

No Dockerfile foi configurado uma **Cron job** para execução do script `create_apod_tweet.py`, no qual será executada todo dia às 6 horas da manhã e, com isso, será criado dois posts no Twitter, um post da imagem do dia e outro post com a explicação da imagem.

### Cron jobs

**Cron** é um serviço de agendamento de tarefas em sistemas operacionais baseados em Unix.

**Cron job** é uma tarefa definida para ser executada em um intervalo ou período específico.

**Cron tab** é o arquivo que contém a lista de tarefas a serem executadas.

## Licença

Este projeto está sob a licença MIT, que pode ser encontrada no arquivo LICENSE.

## Contribuições

Contribuições são bem-vindas! Se você quiser contribuir para este projeto, por favor, abra uma issue ou envie uma solicitação de pull request.
