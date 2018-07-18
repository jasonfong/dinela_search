import json
import logging

from django.conf import settings
import requests


class VisionClient(object):
    def __init__(self):
        pass

    def do_call(self, image_url):
        payload = {
            "requests": [{
                "image": {"source": {"imageUri": image_url}},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
            }]
        }

        resp = requests.post(
            url="https://vision.googleapis.com/v1/images:annotate",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            params={"key": settings.GOOGLE_CLOUD_VISION_API_KEY},
            data=json.dumps(payload),
        )

        try:
            text = resp.json()['responses'][0]['fullTextAnnotation']['text']
        except Exception as err:
            logging.exception('Error while parsing: %s' % resp.text)
            raise err

        return text

    def get_text(self, image_url):
        # Retry call once if it fails
        try:
            text = self.do_call(image_url)
        except Exception as err:
            logging.warning("Failed once on: %s" % image_url)
            text = self.do_call(image_url)
            raise err

        return text
