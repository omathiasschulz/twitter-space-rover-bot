import logging
import datetime
import locale
import coloredlogs
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from html2image import Html2Image
from src.nasa import Nasa
from src.twitter import Twitter

# load envs from .env file
load_dotenv()

# add colored logs to script
coloredlogs.install()

# brazilian format date
locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")


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
    Site para base: https://yaytext.com/pt/negrito-it%C3%A1lico/
    Obs: Caracteres especiais não são mostrados corretamente no Twitter/X mobile

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


def __apod_message(apod_info: dict, translated_title: str, formatted_date: str):
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
    build_message.append(__bold(formatted_date))

    if apod_info.get("copyright"):
        copyright_to = apod_info["copyright"].replace("\n", "")
        build_message.append(f"Copyright: {copyright_to}")

    build_message.append("\n#nasa #apod #astronomy #space #science")
    message = "\n".join(build_message)

    # diminui o tamanho do tweet caso tenha passado de 280 caracteres
    if len(message) > 280:
        message = message.replace("Astronomy Picture of the Day - ", "")
    if len(message) > 280:
        message = message.replace("\n#nasa #apod #astronomy #space #science", "")

    return message


def __main():
    """Criação do tweet sobre o APOD"""

    try:
        logging.info("Starting script to create the APOD tweet...")

        nasa_api = Nasa()
        apod_info = nasa_api.apod()
        logging.info(f"APOD > {apod_info}")

        # criação do tweet principal
        translated_title = __translator(apod_info["title"])
        formatted_date = datetime.datetime.strptime(
            apod_info["date"], "%Y-%m-%d"
        ).strftime("%d de %B de %Y")

        message = __apod_message(apod_info, translated_title, formatted_date)

        twitter_api = Twitter()
        tweet_id = twitter_api.create_tweet(
            message=message, file_url=apod_info["hdurl"]
        )
        logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        # criação do tweet com a imagem da explicação em português
        width = 600
        height = 700
        hti = Html2Image(temp_path="tmp", output_path="tmp", size=(width, height))

        with open("apod_card.html", encoding="UTF-8") as f:
            card_html = f.read()

            card_html = card_html.replace("{{title}}", translated_title)
            translated_explanation = __translator(apod_info["explanation"])
            card_html = card_html.replace("{{explanation}}", translated_explanation)
            card_html = card_html.replace("{{date}}", formatted_date)

            hti.screenshot(html_str=card_html, save_as="apod.png")
            f.close()

            tweet_id = twitter_api.create_tweet(
                in_reply_to=tweet_id, filename="apod.png"
            )
            logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")
            logging.info("Tweet posted with success!")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    __main()
