import os

from google.cloud import storage
import requests

from google.appengine.ext import ndb


class Restaurant(ndb.Model):
    CUISINE_CHOICES = [
        'American', 'American (new)', 'Argentinian', 'Asian Fusion',
        'Barbecue', 'Brazilian', 'British', 'Burgers', 'Cajun',
        'Californian', 'Chinese', 'Euro-Asian', 'Filipino', 'French',
        'Gastropub', 'Hawaiian', 'Indian', 'Indonesian', 'International',
        'Italian', 'Japanese', 'Latin', 'Latin Fusion', 'Mediterranean',
        'Mexican', 'Moroccan', 'Seafood', 'Soul Food', 'Southern', 'Spanish',
        'Steakhouse', 'Sushi', 'Thai', 'Unknown', 'Vegan', 'Vegetarian',
        'Vietnamese',
    ]

    NEIGHBORHOOD_CHOICES = [
        'Agoura Hills', 'Alhambra', 'Arcadia', 'Arts District',
        'Atwater Village', 'Bel-Air', 'Beverly', 'Beverly Hills', 'Brentwood',
        'Burbank', 'Calabasas', 'Canoga Park', 'Century City', 'Cerritos',
        'Chinatown', 'Culver City', 'Downey', 'Downtown', 'Eagle Rock',
        'Echo Park', 'El Segundo', 'Encino', 'Fairfax',
        'Fashion/Jewelry District', 'Glendale', 'Granada Hills',
        'Hermosa Beach', 'Highland Park', 'Hollywood', 'Koreatown', 'La Brea',
        'Larchmont', 'Long Beach', 'Los Feliz', 'Malibu', 'Manhattan Beach',
        'Mar Vista', 'Marina del Rey', 'Monterey Park', 'Pacific Palisades',
        'Pasadena', 'Pico Rivera', 'Pico-Robertson', 'Playa del Rey',
        'Pomona', 'Rancho Palos Verdes', 'Redondo Beach', 'San Gabriel',
        'Santa Monica', 'Sawtelle Japantown', 'Sherman Oaks', 'Silver Lake',
        'South Pasadena', 'Studio City', 'Tarzana', 'Toluca Lake', 'Torrance',
        'Valencia', 'Valley Village', 'Van Nuys', 'Venice', 'West Hollywood',
        'West Los Angeles', 'Westchester', 'Westlake Village', 'Westwood',
        'Woodland Hills',
    ]

    name = ndb.StringProperty(required=True)
    cuisine = ndb.StringProperty(required=True, choices=CUISINE_CHOICES)
    neighborhood = ndb.StringProperty(required=True,
                                      choices=NEIGHBORHOOD_CHOICES)
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
