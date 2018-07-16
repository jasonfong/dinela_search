import logging
import os
import sys

from django.conf import settings
import lxml.html
from google.cloud import storage
import requests

from dinela_search.models import Restaurant


class DineLAParser(object):

    def __init__(self, index_path):
        self.gcs_client = storage.Client()
        self.gcs_bucket = self.gcs_client.get_bucket(settings.GCS_BUCKET)
        self.index_doc = lxml.html.parse(settings.DINELA_INDEX_FILE_PATH)

    def put_restaurant(self, row):
        detail_url = row.xpath(r'td[1]/a/@href')[0]
        restaurant_id = detail_url.split('/')[0]
            
        resto = Restaurant.get_by_id(restaurant_id)

        if resto:
            return False

        name = row.xpath(r'td[1]/a/text()')[0]
        lunch_price = next(iter(row.xpath(r'td[2]/a/text()')), None)
        dinner_price = next(iter(row.xpath(r'td[3]/a/text()')), None)
        cuisine = next(iter(row.xpath(r'td[4]/text()')), None)
        neighborhood = next(iter(row.xpath(r'td[5]/text()')), None)

        name = name.encode('ascii', 'ignore')
        if cuisine is None:
            cuisine = "Unknown"

        if lunch_price:
            lunch_price = int(float(lunch_price.lstrip('$').rstrip('+')))
        if dinner_price:
            dinner_price = int(float(dinner_price.lstrip('$').rstrip('+')))

        resp = requests.get(
            "%s/%s" % (settings.DINELA_BASEURL, detail_url))

        doc = lxml.html.fromstring(resp.text)

        address_lines = doc.xpath(
            r'//*[@id="dinela-menu-wrapper"]/div[3]/div/div[1]/div[2]'
            r'/div[1]/a/span/text()')

        lunch_menu_url = next(iter(
            doc.xpath(r'//*[@id="lunch"]/img/@src')), None)
        
        dinner_menu_url = next(iter(
            doc.xpath(r'//*[@id="dinner"]/img/@src')), None)

        logging.debug(" | ".join(map(str, [
            restaurant_id, name, lunch_price, dinner_price,
            cuisine, neighborhood,
            lunch_menu_url, dinner_menu_url,
        ])))
        
        resto = Restaurant(
            id=restaurant_id,
            name=name,
            cuisine=cuisine,
            neighborhood=neighborhood,
            lunch_price=lunch_price,
            dinner_price=dinner_price,
            address_lines=address_lines,
            lunch_menu_url=lunch_menu_url,
            dinner_menu_url=dinner_menu_url,
        )

        resto.load_menus_to_gcs(self.gcs_bucket)
        resto.put()
        return True

    def parse_restaurants(self, limit=0):
        rows = self.index_doc.xpath(
            r'//*[@id="datatable_restaurants"]/tbody/tr')

        parsed = 0
        ads = 0
        existing = 0

        for row in rows:
            if next(iter(row.xpath('@class')), None) == 'ad_dfp':
                logging.debug('Skipping ad block')
                ads += 1
                continue

            if self.put_restaurant(row):
                parsed += 1
            else:
                existing += 1

            if limit and parsed >= limit:
                break

        return {
            "parsed": parsed,
            "ads": ads,
            "existing": existing,
        }
