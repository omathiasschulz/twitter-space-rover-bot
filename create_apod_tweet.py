import logging
import locale
from datetime import datetime
import coloredlogs
import requests
from dotenv import load_dotenv
from deep_translator import GoogleTranslator
from html2image import Html2Image
from src.nasa import Nasa
from src.twitter import Twitter


# load envs from .env file
load_dotenv()

# add colored logs to script
coloredlogs.install(isatty=True)

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


def __describe_date(base_date: str) -> str:
    """Formata a data e retorna no padrão: DD de FULL_MM de YYYY

    Args:
        base_date (str): Data para formatar no padrão YYYY-MM-DD

    Returns:
        str: Retorna a data formatada
    """
    full_months = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro",
    }
    date = datetime.strptime(base_date, "%Y-%m-%d")
    month = date.strftime("%m")
    return date.strftime(f"%d de {full_months[month]} de %Y")


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

        formatted_date = __describe_date(apod_info["date"])

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

        twitter_api = Twitter()
        tweet_id = twitter_api.create_tweet(message=message, file_url=file_url)
        logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        # criação do tweet com a imagem da explicação em português
        width = 950
        height = 1000
        hti = Html2Image(
            temp_path="tmp",
            output_path="tmp",
            size=(width, height),
            custom_flags=["--no-sandbox", "--disable-gpu"],
            disable_logging=True,
        )

        with open("apod_card.html", encoding="UTF-8") as f:
            card_html = f.read()

            explanation = apod_info["explanation"]
            explanation = explanation.replace("  ", "<br>")
            explanation = explanation.replace(
                "<br><br>", '<div style="margin: 4px;"></div>'
            )
            translated_explanation = __translator(explanation)

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

            logging.warning(
                f"Head: {default_head_font_size} | {len(translated_title)} words"
            )
            logging.warning(
                f"Body: {default_font_size} | {len(translated_explanation)} words"
            )

            card_html = card_html.replace("var_head_font_size", default_head_font_size)
            card_html = card_html.replace("var_font_size", default_font_size)
            card_html = card_html.replace("var_title", translated_title)
            card_html = card_html.replace("var_explanation", translated_explanation)
            card_html = card_html.replace("var_date", formatted_date)

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
