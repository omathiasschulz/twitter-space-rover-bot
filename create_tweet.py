import logging
import os
import uuid
import datetime
import locale
import coloredlogs
import requests
import tweepy
from dotenv import load_dotenv
from deep_translator import GoogleTranslator

load_dotenv()

# add colored logs to script
coloredlogs.install()

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

NASA_API_URL = "https://api.nasa.gov"


def __twitter_client() -> tweepy.Client:
    """Inicia um client para comunicação com Twitter API v2.0

    Returns:
        tweepy.Client: Retorna o client
    """
    return tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_KEY_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )


def __twitter_client_v1() -> tweepy.API:
    """Inicia um client para comunicação com Twitter API v1.1

    Returns:
        tweepy.API: Retorna o client
    """
    auth = tweepy.OAuth1UserHandler(
        os.getenv("TWITTER_API_KEY"), os.getenv("TWITTER_API_KEY_SECRET")
    )
    auth.set_access_token(
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )
    return tweepy.API(auth)


def __create_tweet(
    message: str, in_reply_to_tweet_id: str = None, file_url: str = None
) -> str:
    """Realiza a criação de um novo tweet
    Full doc: https://docs.tweepy.org/en/latest/client.html#tweepy.Client.create_tweet

    Args:
        message (str): Mensagem do tweet (No máximo 280 caracteres)
        in_reply_to_tweet_id (str, optional): Tweet pai/Tweet que será respondido. Defaults to None.
        file_url (str, optional): Url da imagem para adicionar no tweet

    Returns:
        str: ID do tweet criado
    """
    client = __twitter_client()

    media_ids = None
    if file_url:
        filename = f"tmp/{uuid.uuid4()}.jpg"
        request = requests.get(file_url, stream=True, timeout=5)

        with open(filename, "wb") as image:
            for chunk in request:
                image.write(chunk)

        # Full doc: https://docs.tweepy.org/en/latest/api.html#tweepy.API.media_upload
        client_v1 = __twitter_client_v1()
        response_file = client_v1.media_upload(filename=filename)
        media_ids = [response_file.media_id]

        os.remove(filename)

    response = client.create_tweet(
        text=message,
        in_reply_to_tweet_id=in_reply_to_tweet_id,
        media_ids=media_ids,
    )
    logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{response.data['id']}")

    return response.data["id"]


def __nasa_apod() -> dict:
    """Realiza a consulta do APOD (Astronomy Picture of the Day)

    Returns:
        dict: Resposta da consulta
    """
    api_key = os.getenv("NASA_API_KEY")

    response = requests.get(
        f"{NASA_API_URL}/planetary/apod?api_key={api_key}", timeout=5
    )

    data = response.json()
    logging.info(f"APOD [{response.status_code}] > {data}")

    return data


def __translator(text: str) -> str:
    """Traduz o texto informado em inglês para português

    Args:
        text (str): Texto em inglês

    Returns:
        str: Texto em português
    """
    return GoogleTranslator(source="en", target="pt").translate(text)


def __bold(text: str) -> str:
    """Transforma o texto informado em negrito para adicionar no tweet

    Args:
        text (str): Texto base

    Returns:
        str: Texto em negrito
    """
    output = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold_chars = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"

    for character in text:
        if character in chars:
            output += bold_chars[chars.index(character)]
        else:
            output += character
    return output


def __main():
    """Criação de um novo tweet"""

    try:
        logging.info("Starting script to create a new tweet...")
        apod_info = __nasa_apod()

        # criação do tweet principal
        translated_title = __translator(apod_info["title"])

        build_message = []
        build_message.append(f"{__bold(translated_title)} ({apod_info['title']}) 🌌")

        formatted_date = datetime.datetime.strptime(
            apod_info["date"], "%Y-%m-%d"
        ).strftime("%d de %B de %Y")

        build_message.append(
            "\nFoto Astronômica do Dia (Astronomy Picture of the Day - APOD)"
        )
        build_message.append(f"Referente ao dia {__bold(formatted_date)}")

        if apod_info.get("copyright"):
            copyright_to = apod_info["copyright"].replace("\n", "")
            build_message.append(f"Copyright: {copyright_to}")

        build_message.append("#nasa #apod #astronomy #space #science")
        message = "\n".join(build_message)

        tweet_id = __create_tweet(message=message, file_url=apod_info["hdurl"])

        # criação do tweet com explicação em inglês
        explanation = f"Explanation [🇺🇸 Original text]: {apod_info['explanation']}"
        if len(explanation) > 240:
            explanation = f"{explanation[:240]}..."

        __create_tweet(message=explanation, in_reply_to_tweet_id=tweet_id)

        # criação do tweet com explicação em português
        translated_explanation = __translator(apod_info["explanation"])

        translated_explanation = (
            f"Explicação [🇧🇷 Não oficial]: {translated_explanation}"
        )
        if len(translated_explanation) > 240:
            translated_explanation = f"{translated_explanation[:240]}..."

        __create_tweet(message=translated_explanation, in_reply_to_tweet_id=tweet_id)

        logging.info("Tweet posted with success!")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    __main()
