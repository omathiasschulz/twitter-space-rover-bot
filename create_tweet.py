"""Criação de um novo tweet"""
import logging
import os
from dotenv import load_dotenv
from tweepy import Client

load_dotenv()


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


def __main():
    """Criação de um novo tweet"""

    try:
        __create_tweet("Novo tweet!\nTeste com quebra de linha")

        print("Tweet postado com sucesso!")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    __main()
