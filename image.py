# pip install html2image
from html2image import Html2Image


WIDTH = 400
HEIGHT = 500

hti = Html2Image(temp_path="tmp", output_path="tmp", size=(WIDTH, HEIGHT))

apod = {
    "title": "Three Galaxies and a Comet",
    "explanation": "Distant galaxies abound in this one degree wide field of view toward the southern constellation Grus (The Crane). But the three spiral galaxies at the lower right are quite striking. In fact, all three galaxies are grouped about 70 million light years away and sometimes known as the Grus Triplet. They share the pretty telescopic frame, recorded on December 13, with the comet designated C/2020 V2 ZTF. Now outbound from the inner Solar System and swinging below the ecliptic plane in a hyperbolic orbit, the comet was about 29 light-minutes from our fair planet in this image. And though comet ZTF was brighter when it was closest to the Sun last May and closest to Earth in September of 2023, it still shines in telescopes pointed toward southern night skies, remaining almost as bright as the Grus Triplet galaxies.",
}

html = f'<link href="http://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css" /><h3>{apod["title"]}</h3><hr /><div>{apod["explanation"]}</div>'
css = 'body {padding: 10px; margin: auto; width: 380px; background-color: #dddddd; font-family: "Roboto", sans-serif;}'

hti.screenshot(html_str=html, css_str=css, save_as="apod.png")
# hti.screenshot(html_file="apod.html", css_str=css, save_as="apod.png")
