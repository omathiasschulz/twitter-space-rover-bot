from dotenv import load_dotenv
from html2image import Html2Image
from src.twitter import Twitter


# load envs from .env file
load_dotenv()


WIDTH = 600
HEIGHT = 700

hti = Html2Image(temp_path="tmp", output_path="tmp", size=(WIDTH, HEIGHT))

apod = {
    "title": "Halos de gelo sobre a Baviera",
    "explanation": "O que está causando esses arcos incomuns no céu? Cristais de gelo. Ao cruzar um campo de neve fresca perto de Füssen, Baviera, Alemanha, no início deste mês, o fotógrafo percebeu que havia entrado em uma névoa gelada. Para que a água suspensa congele formando uma névoa gelada são necessárias temperaturas bastante baixas e, de fato, a temperatura do ar neste dia foi medida bem abaixo de zero. A névoa gelada refletia a luz do pôr do sol atrás da Igreja de St. Coleman. O resultado foi um dos maiores espetáculos que o fotógrafo já viu. Primeiro, os pontos na imagem em destaque não são estrelas de fundo, mas sim gelo e neve suspensos. A seguir, dois halos de gelo proeminentes são visíveis: o halo de 22 graus e o halo de 46 graus. Vários arcos também são visíveis, incluindo, de cima para baixo, antisolar (subsolar), circunzenital, Parry, tangente e parélico (horizontal). Finalmente, a curva em forma de balão que liga o arco superior ao Sol é a mais rara de todas: é o arco helíaco, criado pela reflexão nas laterais de cristais de gelo de formato hexagonal suspensos numa orientação horizontal.",
}

html = f'<h3>{apod["title"]}</h3><p>{apod["explanation"]}</p>'
css = "body { margin: auto; width: 580px; height: 700px; padding: 10px; font-family: 'Lato', sans-serif; font-weight: 300; font-size: 20px; line-height: 1.5; background-image: linear-gradient(to bottom right, #1b4468, #1e4c74); color: white; } h3 { text-transform: uppercase; margin-bottom: 10px; }"

hti.screenshot(html_str=html, css_str=css, save_as="apod.png")

twitter_api = Twitter()
tweet_id = twitter_api.create_tweet(filename="apod.png")
print("tweet_id", tweet_id)
