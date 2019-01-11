import logging

from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.generic import View
from google.appengine.api import search
import requests

from dinela_search.models import Restaurant
from dinela_search.parser import DineLAParser
from dinela_search.vision import VisionClient


class LoadListingView(View):
    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_API_KEY') != settings.ADMIN_API_KEY:
            return HttpResponseForbidden()

        limit = int(request.GET.get('limit', 3))

        parser = DineLAParser(settings.DINELA_INDEX_FILE_PATH)
        result = parser.parse_restaurants(limit)

        return JsonResponse({
            "result": result
        })


class ProcessMenusView(View):
    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_API_KEY') != settings.ADMIN_API_KEY:
            return HttpResponseForbidden()

        limit = int(request.GET.get('limit', 3))

        client = VisionClient()

        qry = Restaurant.query(Restaurant.menus_ocr_done==False)
        
        results = []
        errors = []
        menu_missing = []

        for item in qry.fetch(limit):
            if not item.lunch_menu_gcs and not item.dinner_menu_gcs:
                menu_missing.append(item.name)
                continue

            if item.lunch_menu_gcs:
                image_uri = item.lunch_menu_gcs
                text = client.get_text(image_uri)
                item.lunch_menu_text = text

            if item.dinner_menu_gcs:
                image_uri = item.dinner_menu_gcs
                text = client.get_text(image_uri)
                item.dinner_menu_text = text

            if ((item.lunch_menu_gcs and not item.lunch_menu_text) or
                (item.dinner_menu_gcs and not item.dinner_menu_text)):
                logging.error('Failed to parse a menu for: %s' % item.name)
                errors.append(item.name)
            else:
                item.menus_ocr_done = True
                item.put()

                results.append({
                    "name": item.name,
                    "lunch": item.lunch_menu_text and len(item.lunch_menu_text),
                    "dinner": item.dinner_menu_text and len(item.dinner_menu_text),
                })

        return JsonResponse({
            "results": results,
            "errors": errors,
            "menu_missing": menu_missing,
        })


class UpdateSearchIndexView(View):
    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_API_KEY') != settings.ADMIN_API_KEY:
            return HttpResponseForbidden()

        limit = int(request.GET.get('limit', 3))

        qry = Restaurant.query(Restaurant.search_updated==None)
        
        indexed = []
        errors = []

        index = search.Index(name=settings.SEARCH_INDEX)

        for item in qry.fetch(limit):
            fields = [
                search.TextField(name='name', value=item.name),
                search.AtomField(name='cuisine', value=item.cuisine),
                search.AtomField(name='neighborhood', value=item.neighborhood),
                search.NumberField(name='lunch_price', value=item.lunch_price or 0),
                search.TextField(name='lunch_menu', value=item.lunch_menu_text),
                search.NumberField(name='dinner_price', value=item.dinner_price or 0),
                search.TextField(name='dinner_menu', value=item.dinner_menu_text),
            ]

            d = search.Document(doc_id=item.key.id(), fields=fields)

            try:
                index.put(d)
                item.search_updated = datetime.now()
                item.put()
            except search.Error:
                logging.exception("Error indexing: %s" % item.name)
                errors.append(item.name)
            else:
                indexed.append(item.name)

        return JsonResponse({
            "indexed": indexed,
            "num_indexed": len(indexed),
            "errors": errors,
            "num_errors": len(errors),
        })
