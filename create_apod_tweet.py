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


def __apod_explanation_image(title: str, date: str, explanation: str):
    """Realiza a geração da imagem com a explicação completa do APOD do dia

    Args:
        title (str): Título da explicação
        date (str): Data do APOD já formatada
        explanation (str): Explicação
    """
    with open("apod_card.html", encoding="UTF-8") as file:
        card_html = file.read()

        explanation = explanation.replace("  ", "<br>")
        explanation = explanation.replace(
            "<br><br>", '<div style="margin: 4px;"></div>'
        )
        translated_explanation = text_translator(explanation)

        card_html = card_html.replace("var_title", title)
        card_html = card_html.replace("var_explanation", translated_explanation)
        card_html = card_html.replace("var_date", date)

        with open("tmp/apod.html", "w", encoding="utf-8") as html_file:
            html_file.write(card_html)
            html_file.close()

        html_to_image("apod.html", "apod")
        file.close()


def __create_main_tweet(
    twitter_api: Twitter, translated_title: str, formatted_date: str, apod_info: dict
) -> str:
    """Realiza a criação do tweet principal do APOD

    Args:
        twitter_api (Twitter): Comunicação com API do twitter
        translated_title (str): Título do APOD traduzido
        formatted_date (str): Data do APOD traduzido
        apod_info (dict): Informações do APOD

    Returns:
        str: Retorna o ID do tweet
    """
    message = __apod_message(apod_info, translated_title, formatted_date)

    if is_debug:
        logging.info("### Message")
        logging.info(message)
        return None

    media_ids = []
    # valida se é imagem ou vídeo
    if apod_info["media_type"] != "video":
        logging.info("APOD is image")

        # valida se o link HD da imagem está funcionando
        if apod_info.get("hdurl") and __check_link_is_valid(apod_info["hdurl"]):
            media_ids.append(twitter_api.upload_image_from_url(apod_info["hdurl"]))
        else:
            logging.warning(
                f"Link HD da imagem não está funcionando... {apod_info['hdurl']}"
            )
            media_ids.append(twitter_api.upload_image_from_url(apod_info["url"]))
    else:
        logging.info("APOD is video")
        media_ids.append(twitter_api.upload_video_from_url(apod_info["url"]))

    tweet_id = twitter_api.create_tweet(message=message, media_ids=media_ids)
    logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")
    return tweet_id


def __create_secondary_tweet(
    twitter_api: Twitter,
    translated_title: str,
    formatted_date: str,
    apod_info: dict,
    tweet_id: str,
):
    """Realiza a criação do tweet secundário do APOD

    Args:
        twitter_api (Twitter): Comunicação com API do twitter
        translated_title (str): Título do APOD traduzido
        formatted_date (str): Data do APOD traduzido
        apod_info (dict): Informações do APOD
        tweet_id (str): ID do tweet principal
    """
    __apod_explanation_image(translated_title, formatted_date, apod_info["explanation"])

    apod_explanation_message = ""
    if apod_info.get("copyright"):
        copyright_to = apod_info["copyright"].replace("\n", "")
        apod_explanation_message = f"Copyright: {copyright_to}"
    apod_explanation_message += "\n\nExplicação detalhada ⤵️"

    if is_debug:
        logging.info("### Apod Explanation Message")
        logging.info(apod_explanation_message)
        return

    media_ids = [twitter_api.upload_image_from_tmp("apod.png")]

    tweet_id = twitter_api.create_tweet(
        in_reply_to=tweet_id,
        message=apod_explanation_message,
        media_ids=media_ids,
    )

    logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")


def __main():
    """Criação do tweet sobre o APOD"""
    start = datetime.now()
    logging.warning(f"##### APOD SCRIPT - STARTED [{start}] #####")
    if is_debug:
        logging.warning("[DEVELOPMENT MODE]")

    try:
        twitter_api = Twitter()
        nasa_api = Nasa()
        apod_info = nasa_api.apod("2024-04-14")
        # apod_info = nasa_api.apod()
        logging.info(f"APOD > {apod_info}")

        translated_title = text_translator(apod_info["title"])
        formatted_date = date_describe(apod_info["date"])

        tweet_id = __create_main_tweet(
            twitter_api, translated_title, formatted_date, apod_info
        )

        __create_secondary_tweet(
            twitter_api, translated_title, formatted_date, apod_info, tweet_id
        )

        logging.info("Tweet posted with success!")
    except Exception as error:
        logging.error(error)

    end = datetime.now()
    logging.info(f"Runtime: {(end - start).total_seconds()} seconds")
    logging.warning(f"##### APOD SCRIPT - FINISHED [{end}] #####")


if __name__ == "__main__":
    __main()
