import os
import uuid
import requests
import tweepy
from pytube import YouTube


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

    def upload_image_from_tmp(self, image_name: str) -> str:
        """Realiza o upload para o twitter da imagem informada

        Args:
            image_name (str): Nome da imagem que está na tmp/

        Returns:
            str: Retorna o ID da imagem enviada
        """
        response_file = self.client_v1.media_upload(filename=f"tmp/{image_name}")
        return response_file.media_id

    def upload_image_from_url(self, image_url: str) -> str:
        """Realiza o upload para o twitter da imagem informada

        Args:
            image_url (str): Url da imagem

        Returns:
            str: Retorna o ID da imagem enviada
        """
        file_url_filename = f"tmp/{uuid.uuid4()}.jpg"
        request = requests.get(image_url, stream=True, timeout=10)

        with open(file_url_filename, "wb") as image:
            for chunk in request:
                image.write(chunk)

        response_file = self.client_v1.media_upload(filename=file_url_filename)
        os.remove(file_url_filename)

        return response_file.media_id

    def upload_video_from_url(self, video_url: str) -> str:
        """Realiza o upload para o twitter do vídeo informado

        Args:
            video_url (str): Url do vídeo no youtube

        Returns:
            str: Retorna o ID do vídeo enviado
        """
        youtube_interface = YouTube(video_url)
        youtube_interface = youtube_interface.streams.get_highest_resolution()

        youtube_interface.download(
            output_path="tmp", filename="video.mp4", skip_existing=False
        )

        response_file = self.client_v1.media_upload(
            filename="tmp/video.mp4", chunked=True
        )
        os.remove("tmp/video.mp4")

        return response_file.media_id

    def create_tweet(
        self,
        message: str = "",
        in_reply_to: str = None,
        media_ids: list = None,
    ) -> str:
        """Realiza a criação de um novo tweet
        Full doc: https://docs.tweepy.org/en/latest/client.html#tweepy.Client.create_tweet

        Args:
            message (str, optional): Mensagem do tweet (No máximo 280 caracteres). Defaults to "".
            in_reply_to (str, optional): ID Tweet pai/Tweet que será respondido. Defaults to None.
            media_ids (list, optional): Ids do twitter de imagens/vídeos para vincular ao tweet

        Returns:
            str: ID do tweet criado
        """
        response = self.client_v2.create_tweet(
            text=message,
            in_reply_to_tweet_id=in_reply_to,
            media_ids=media_ids,
        )
        return response.data["id"]
