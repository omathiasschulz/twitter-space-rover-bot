import os
import uuid
import requests
import tweepy


class Twitter:
    """Realiza a comunicação com a API do Twitter utilizando a biblioteca Tweepy"""

    def __init__(self) -> None:
        """Construtor da classe Twitter"""
        self.client_v1: tweepy.API = self.__twitter_client_v1()
        self.client_v2: tweepy.Client = self.__twitter_client_v2()

    def __twitter_client_v1(self) -> tweepy.API:
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

    def __twitter_client_v2(self) -> tweepy.Client:
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

    def create_tweet(
        self,
        message: str = "",
        in_reply_to: str = None,
        file_url: str = None,
        filename: str = None,
    ) -> str:
        """Realiza a criação de um novo tweet
        Full doc: https://docs.tweepy.org/en/latest/client.html#tweepy.Client.create_tweet

        Args:
            message (str, optional): Mensagem do tweet (No máximo 280 caracteres). Defaults to "".
            in_reply_to (str, optional): ID Tweet pai/Tweet que será respondido. Defaults to None.
            file_url (str, optional): Url da WEB da imagem para adicionar no tweet
            filename (str, optional): Nome da imagem na tmp/ para adicionar no tweet

        Returns:
            str: ID do tweet criado
        """
        media_ids = []

        if file_url:
            file_url_filename = f"tmp/{uuid.uuid4()}.jpg"
            request = requests.get(file_url, stream=True, timeout=5)

            with open(file_url_filename, "wb") as image:
                for chunk in request:
                    image.write(chunk)

            # Full doc: https://docs.tweepy.org/en/latest/api.html#tweepy.API.media_upload
            response_file = self.client_v1.media_upload(filename=file_url_filename)
            media_ids.append(response_file.media_id)

            os.remove(file_url_filename)

        if filename:
            # Full doc: https://docs.tweepy.org/en/latest/api.html#tweepy.API.media_upload
            response_file = self.client_v1.media_upload(filename=f"tmp/{filename}")
            media_ids.append(response_file.media_id)

        response = self.client_v2.create_tweet(
            text=message,
            in_reply_to_tweet_id=in_reply_to,
            media_ids=media_ids,
        )

        return response.data["id"]
