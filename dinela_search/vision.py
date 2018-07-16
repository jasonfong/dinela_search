import json
import logging
import requests


class VisionClient(object):
    def __init__(self, auth):
        self.auth = auth

    def do_call(self, image_url):
        payload = {
            "requests": [{
                "image": {"source": {"imageUri": image_url}},
                "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]
            }]
        }

        resp = requests.post(
            url='https://vision.googleapis.com/v1/images:annotate',
            headers={
                'Authorization': self.auth,
                'Content-Type': 'application/json; charset=utf-8',
            },
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
