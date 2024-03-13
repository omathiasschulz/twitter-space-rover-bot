import os
import logging
import locale
from datetime import datetime
import coloredlogs
import requests
from dotenv import load_dotenv
from src.api.nasa import Nasa
from src.api.twitter import Twitter
from src.utils.text import text_bold, text_translator
from src.utils.date import date_describe
from src.utils.image import html_to_image


# load envs from .env file
load_dotenv()

# add colored logs to script
coloredlogs.install(isatty=True)

# brazilian format date
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

# is debug
is_debug = os.getenv("DEBUG") != "0"


def __check_link_is_valid(url: str) -> bool:
    """Valida se o link informado é válido retornando o status code 200

    Args:
        url (str): URL para validar

    Returns:
        bool: Retorna se a URL é válida
    """
    response = requests.head(url, timeout=5)
    return response.status_code == 200


def __apod_message(apod_info: dict, translated_title: str, formatted_date: str) -> str:
    """Realiza a construção da mensagem do tweet sobre o APOD do dia

    Args:
        apod_info (dict): Informações retornadas da API do APOD
        translated_title (str): Título do APOD do dia traduzido
        formatted_date (str): Data do APOD do dia formatado

    Returns:
        str: Retorna a mensagem
    """
    build_message = []
    build_message.append(f"{translated_title} ({apod_info['title']}) 🌌")

    if apod_info["media_type"] == "video":
        build_message.append(f"\nAssista ao vídeo: {apod_info['url']}")

    build_message.append(
        "\nFoto Astronômica do Dia (Astronomy Picture of the Day - APOD)"
    )
    build_message.append(text_bold(formatted_date))

    build_message.append("\n#nasa #apod #astronomy #space #science")
    message = "\n".join(build_message)

    # diminui o tamanho do tweet
    # tamanho máximo para mensagem no twitter = 280 caracteres
    # negrito e ícones usam 2 caracteres de espaço no twitter, totalizando +20 caracteres
    if len(message) > 260:
        message = message.replace("Astronomy Picture of the Day - ", "")
    if len(message) > 260:
        message = message.replace("\n#nasa #apod #astronomy #space #science", "")
    if len(message) > 260:
        message = message[:260]

    return message


def __main():
    """Criação do tweet sobre o APOD"""
    start = datetime.now()
    logging.warning(f"##### APOD SCRIPT - STARTED [{start}] #####")
    if is_debug:
        logging.warning("[DEVELOPMENT MODE]")

    try:
        nasa_api = Nasa()
        apod_info = nasa_api.apod()
        logging.info(f"APOD > {apod_info}")

        # criação do tweet principal
        translated_title = text_translator(apod_info["title"])

        formatted_date = date_describe(apod_info["date"])

        message = __apod_message(apod_info, translated_title, formatted_date)

        file_url = None
        # se o apod do dia for vídeo, não possui imagem
        if apod_info["media_type"] != "video":
            # valida se o link HD da imagem está funcionando
            if apod_info.get("hdurl") and __check_link_is_valid(apod_info["hdurl"]):
                file_url = apod_info["hdurl"]
            else:
                logging.warning(
                    f"Link HD da imagem não está funcionando... {apod_info['hdurl']}"
                )
                file_url = apod_info["url"]

        if is_debug:
            logging.info("### Message")
            logging.info(message)
        else:
            twitter_api = Twitter()
            tweet_id = twitter_api.create_tweet(message=message, file_url=file_url)
            logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        # criação do tweet com a imagem da explicação em português
        with open("apod_card.html", encoding="UTF-8") as file:
            card_html = file.read()

            explanation = apod_info["explanation"]
            explanation = explanation.replace("  ", "<br>")
            explanation = explanation.replace(
                "<br><br>", '<div style="margin: 4px;"></div>'
            )
            translated_explanation = text_translator(explanation)

            # ajusta o tamanho da fonte do título de acordo com número de palavras
            default_head_font_size = "38px"
            if len(translated_title) > 33:
                default_head_font_size = "30px"
            if len(translated_title) > 42:
                default_head_font_size = "25px"

            # ajusta o tamanho da fonte de acordo com número de palavras
            default_font_size = "40px"
            if len(translated_explanation) > 600:
                default_font_size = "36px"
            if len(translated_explanation) > 800:
                default_font_size = "34px"
            if len(translated_explanation) > 900:
                default_font_size = "32px"
            if len(translated_explanation) > 1000:
                default_font_size = "30px"
            if len(translated_explanation) > 1100:
                default_font_size = "29px"
            if len(translated_explanation) > 1200:
                default_font_size = "28px"
            if len(translated_explanation) > 1300:
                default_font_size = "27px"
            if len(translated_explanation) > 1400:
                default_font_size = "26px"
            if len(translated_explanation) > 1500:
                default_font_size = "20px"

            logging.info(
                f"Head: {default_head_font_size} | {len(translated_title)} words"
            )
            logging.info(
                f"Body: {default_font_size} | {len(translated_explanation)} words"
            )

            card_html = card_html.replace("var_head_font_size", default_head_font_size)
            card_html = card_html.replace("var_font_size", default_font_size)
            card_html = card_html.replace("var_title", translated_title)
            card_html = card_html.replace("var_explanation", translated_explanation)
            card_html = card_html.replace("var_date", formatted_date)

            html_to_image(card_html, "apod")
            file.close()

            apod_explanation_message = ""
            if apod_info.get("copyright"):
                copyright_to = apod_info["copyright"].replace("\n", "")
                apod_explanation_message = f"Copyright: {copyright_to}"
            apod_explanation_message += "\n\nExplicação detalhada ⤵️"

            if is_debug:
                logging.info("### Apod Explanation Message")
                logging.info(apod_explanation_message)
            else:
                tweet_id = twitter_api.create_tweet(
                    in_reply_to=tweet_id,
                    message=apod_explanation_message,
                    filename="apod.png",
                )
                logging.warning(
                    f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}"
                )

            logging.info("Tweet posted with success!")
    except Exception as error:
        logging.error(error)

    end = datetime.now()
    logging.info(f"Runtime: {(end - start).total_seconds()} seconds")
    logging.warning(f"##### APOD SCRIPT - FINISHED [{end}] #####")


if __name__ == "__main__":
    __main()
