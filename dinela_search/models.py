import os

from google.cloud import storage
import requests

from google.appengine.ext import ndb


class Restaurant(ndb.Model):
    name = ndb.StringProperty(required=True)
    cuisine = ndb.StringProperty(required=True)
    neighborhood = ndb.StringProperty(required=True)
    tags = ndb.StringProperty(repeated=True)

    address_lines = ndb.StringProperty(repeated=True)
    location = ndb.GeoPtProperty()

    lunch_price = ndb.IntegerProperty()
    lunch_menu_url = ndb.StringProperty()
    lunch_menu_gcs = ndb.StringProperty()
    lunch_menu_text = ndb.TextProperty()

    dinner_price = ndb.IntegerProperty()
    dinner_menu_url = ndb.StringProperty()
    dinner_menu_gcs = ndb.StringProperty()
    dinner_menu_text = ndb.TextProperty()

    menus_ocr_done = ndb.BooleanProperty(default=False)

    updated = ndb.DateTimeProperty(auto_now=True)
    search_updated = ndb.DateTimeProperty()

    def _save_menu(self, gcs_bucket, meal_type, file_ext, data):
        blob = storage.Blob(
            name='menus/%s_%s%s' % (self.key.id(), meal_type, file_ext),
            bucket=gcs_bucket,
        )
        blob.upload_from_string(data)
        blob.make_public()
        if meal_type == 'lunch':
            self.lunch_menu_gcs = blob.public_url
        else:
            self.dinner_menu_gcs = blob.public_url

    def load_menus_to_gcs(self, gcs_bucket):
        if self.lunch_menu_url:
            _ , ext = os.path.splitext(self.lunch_menu_url)
            resp = requests.get(self.lunch_menu_url)
            self._save_menu(gcs_bucket, 'lunch', ext, resp.content)

        if self.dinner_menu_url:
            _ , ext = os.path.splitext(self.dinner_menu_url)
            resp = requests.get(self.dinner_menu_url)
            self._save_menu(gcs_bucket, 'dinner', ext, resp.content)


class Account(ndb.Model):
    email = ndb.StringProperty(required=True)
