import os
import requests


class Nasa:
    """Realiza a comunicação com a API da NASA"""

    NASA_API_URL = "https://api.nasa.gov"

    def __init__(self) -> None:
        """Construtor da classe Nasa"""
        self.api_key = os.getenv("NASA_API_KEY")

    def apod(self, date: str = None) -> dict:
        """Realiza a consulta do APOD (Astronomy Picture of the Day)

        Args:
            date (str, optional): Data para consulta do APOD (YYYY-MM-DD). Defaults to None.

        Returns:
            dict: Resposta da consulta
        """
        extra_filters = ""
        # valida se consulta o APOD de um dia em específico ou com base no dia de hoje
        if date:
            extra_filters = f"&date={date}"

        response = requests.get(
            f"{self.NASA_API_URL}/planetary/apod?api_key={self.api_key}{extra_filters}",
            timeout=10,
        )

        return response.json()
