"""Criação de um novo tweet"""
import logging
import os
import requests
from dotenv import load_dotenv
from tweepy import Client

load_dotenv()


NASA_API_URL = "https://api.nasa.gov"


def __twitter_client() -> Client:
    """Inicia um client para comunicação com Twitter

    Returns:
        Client: Retorna o client
    """
    return Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_KEY_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )


def __create_tweet(message: str):
    """Realiza a criação de um novo tweet usando o client
    Full doc: https://docs.tweepy.org/en/latest/client.html#tweepy.Client.create_tweet

    Args:
        message (str): Mensagem do tweet
    """
    client = __twitter_client()

    response = client.create_tweet(text=message)

    print("response")
    print(response)


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
    print("status_code", response.status_code)
    print("data", data)
    return data


def __main():
    """Criação de um novo tweet"""

    try:
        apod_info = __nasa_apod()

        copyright_to = apod_info["copyright"].replace("\n", "")

        message = (
            f"{apod_info['title']}"
            # f"\n\n{apod_info['explanation']}"
            f"\n\nImage Link: {apod_info['hdurl']}"
            f"\n\nCopyright to: {copyright_to}"
        )

        __create_tweet(message)

        print("Tweet postado com sucesso!")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    __main()
