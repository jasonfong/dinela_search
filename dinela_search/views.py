import logging

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.generic import View

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

        for item in qry.fetch(limit):
            if item.lunch_menu_gcs:
                image_uri = item.lunch_menu_gcs
                text = client.get_text(image_uri)
                item.lunch_menu_text = text

            if item.dinner_menu_gcs:
                image_uri = item.dinner_menu_gcs
                text = client.get_text(image_uri)
                item.dinner_menu_text = text

            if not item.lunch_menu_text and not item.dinner_menu_text:
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
            "errors": errors
        })
