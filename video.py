import logging
from pytube import YouTube


apod_info = {
    "copyright": "\nDavid Duarte\n",
    "date": "2024-04-14",
    "explanation": "How does a total solar eclipse end? Yes, the Moon moves out from fully blocking the Sun, but in the first few seconds of transition, interesting things appear. The first is called a diamond ring. Light might stream between mountains or through relative lowlands around the Moon's edge, as seen from your location, making this sudden first light, when combined with the corona that surrounds the Moon, look like a diamond ring. Within seconds other light streams appear that are called, collectively, Bailey's beads. In the featured video, it may seem that the pink triangular prominence on the Sun is somehow related to where the Sun begins to reappear, but it is not. Observers from other locations saw Bailey's beads emerge from different places around the Moon, away from the iconic triangular solar prominence visible to all. The video was captured with specialized equipment from New Boston, Texas, USA on April 8, 2024.   Solar Eclipse Imagery: Notable Submissions to APOD",
    "media_type": "video",
    "service_version": "v1",
    "title": "How a Total Solar Eclipse Ended",
    "url": "https://www.youtube.com/embed/w5uUcq__vMo?rel=0",
}


def download(link):
    """Download

    Args:
        link (_type_): _description_
    """
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        youtubeObject.download(
            output_path="tmp", filename="video.mp4", skip_existing=False
        )
    except Exception as error:
        logging.error(error)


download(apod_info["url"])
