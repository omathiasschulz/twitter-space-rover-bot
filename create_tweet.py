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
        apod_info = nasa_api.apod("2024-01-05")
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

        # html = (
        #     '<script src="https://kit.fontawesome.com/4163205221.js" crossorigin="anonymous">'
        #     "</script>"
        #     '<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,400i&display=swap"'
        #     ' rel="stylesheet" />'
        #     f'<div class="topo">{translated_title}</div>'
        #     f'<div class="centro">{translated_explanation}</div>'
        #     '<div class="final">'
        #     '<span class="traducao">🇧🇷 Tradução não oficial</span>'
        #     '<span class="tag"><i class="fa-brands fa-x-twitter"></i> SpaceRoverBot</span>'
        #     f'<span class="tag"><i class="fa-regular fa-clock"></i> {formatted_date}</span>'
        #     "</div>"
        # )

        with open("apod_card.html", encoding="UTF-8") as f:
            card_html = f.read()

            card_html = card_html.replace("{{title}}", translated_title)
            card_html = card_html.replace("{{explanation}}", translated_explanation)
            card_html = card_html.replace("{{date}}", formatted_date)

            hti.screenshot(html_str=card_html, save_as="apod.png")
            f.close()

            # hti.screenshot(html_str=html, css_file="apod.css", save_as="apod.png")
            # hti.screenshot(html_file="card_v30.html", save_as="apod.png")
            tweet_id = twitter_api.create_tweet(
                in_reply_to=tweet_id, filename="apod.png"
            )
            logging.warning(f"TWEET > https://x.com/SpaceRoverBot/status/{tweet_id}")
            logging.info("Tweet posted with success!")
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    __main()
