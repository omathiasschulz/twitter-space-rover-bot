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


def __main():
    """Criação de um novo tweet"""

    try:
        logging.info("Starting script to create a new tweet...")

        nasa_api = Nasa()
        apod_info = nasa_api.apod()
        logging.info(f"APOD > {apod_info}")

        # criação do tweet principal
        translated_title = __translator(apod_info["title"])

        build_message = []
        build_message.append(f"{translated_title} ({apod_info['title']}) 🌌")

        formatted_date = datetime.datetime.strptime(
            apod_info["date"], "%Y-%m-%d"
        ).strftime("%d de %B de %Y")

        build_message.append(
            "\nFoto Astronômica do Dia (Astronomy Picture of the Day - APOD)"
        )
        build_message.append(__bold(formatted_date))

        if apod_info.get("copyright"):
            copyright_to = apod_info["copyright"].replace("\n", "")
            build_message.append(f"Copyright: {copyright_to}")

        build_message.append("\n#nasa #apod #astronomy #space #science")
        message = "\n".join(build_message)

        twitter_api = Twitter()
        tweet_id = twitter_api.create_tweet(
            message=message, file_url=apod_info["hdurl"]
        )
        logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        # criação do tweet com explicação em português
        translated_explanation = __translator(apod_info["explanation"])
        # translated_explanation_lines = textwrap.wrap(translated_explanation, width=278)
        # for line in translated_explanation_lines:
        #     tweet_id = twitter_api.create_tweet(
        #         message=f"{line} +", in_reply_to=tweet_id
        #     )
        #     logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        # # criação do tweet com explicação em inglês
        # explanation = f"Explanation [🇺🇸 Original text]: {apod_info['explanation']}"
        # explanation_lines = textwrap.wrap(explanation, width=278)
        # for line in explanation_lines:
        #     tweet_id = twitter_api.create_tweet(
        #         message=f"{line} +", in_reply_to=tweet_id
        #     )
        #     logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        # criação do tweet com explicação em português - imagem
        WIDTH = 600
        HEIGHT = 700
        hti = Html2Image(temp_path="tmp", output_path="tmp", size=(WIDTH, HEIGHT))

        # html = f"<h3>{translated_title}</h3><p>{translated_explanation}</p>"
        # css = "body { margin: auto; width: 580px; height: 700px; padding: 10px; font-family: 'Lato', sans-serif; font-weight: 300; font-size: 20px; line-height: 1.5; background-image: linear-gradient(to bottom right, #1b4468, #1e4c74); color: white; } h3 { text-transform: uppercase; margin-bottom: 10px; }"

        html = f'<script src="https://kit.fontawesome.com/4163205221.js" crossorigin="anonymous"></script><link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i&display=swap" rel="stylesheet" /><div class="container"><div class="topo">{translated_title}</div><div class="centro">{translated_explanation}</div><div class="final"><span class="traducao">Tradução não oficial 🇧🇷</span><span class="tag"><i class="fa-brands fa-x-twitter"></i> SpaceRoverBot</span><span class="tag"><i class="fa-regular fa-clock"></i> 05/01/2024</span></div></div>'
        css = "body {font-family: sans-serif;font-size: 17px;line-height: 1.5;color: #fff;}.container {width: 560px;height: 680px;margin: auto;display: flex; /* layout flexível para organizar elementos internos */flex-direction: column; /* seta os elementos internos em coluna */padding: 6px;background-image: linear-gradient(to bottom right, #136a8a, #267871);border-radius: 5px;border: 2px solid #82c1bb;}.topo {font-size: 25px;font-weight: bold;font-family: 'Open Sans', sans-serif;border-bottom: 1px solid #82c1bb;}.centro {flex-grow: 1; /* aumenta a altura para preencher o espaço restante */display: flex; /* layout flexível para organizar elementos internos */flex-direction: column; /* seta os elementos internos em coluna */justify-content: center; /* centraliza o conteúdo interno verticalmente */}.final {text-align: end;}.traducao {color: #e5e5e5;font-size: 14px;margin-top: 4px;float: left;}.tag {padding: 4px;border-radius: 4px;background-color: rgba(0, 0, 0, 0.6);}.tag:nth-child(2) {margin-right: 6px;}"

        hti.screenshot(html_str=html, css_str=css, save_as="apod.png")
        tweet_id = twitter_api.create_tweet(in_reply_to=tweet_id, filename="apod.png")
        logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")

        logging.info("Tweet posted with success!")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    __main()
