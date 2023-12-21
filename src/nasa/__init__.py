import os
import requests


class Nasa:
    """Realiza a comunicação com a API da NASA"""

    NASA_API_URL = "https://api.nasa.gov"

    def __init__(self) -> None:
        """Construtor da classe Nasa"""
        # default timeout 5 seconds
        self.default_timeout = 5
        self.api_key = os.getenv("NASA_API_KEY")

    def apod(self) -> dict:
        """Realiza a consulta do APOD (Astronomy Picture of the Day)

        Returns:
            dict: Resposta da consulta
        """
        response = requests.get(
            f"{self.NASA_API_URL}/planetary/apod?api_key={self.api_key}",
            timeout=self.default_timeout,
        )

        return response.json()
