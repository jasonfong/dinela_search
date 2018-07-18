from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from google.appengine.api import search
from google.appengine.ext import ndb

from dinela_search.models import Restaurant


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        index = search.Index(settings.SEARCH_INDEX)
        search_results = index.search(query)

        resto_ids = [d.doc_id for d in search_results]

        restaurants = ndb.get_multi([ndb.Key(Restaurant, k) for k in resto_ids])

        return render(
            request,
            'dinela_search/index.html',
            {
                'results': restaurants,
                'dinela_baseurl': settings.DINELA_BASEURL,
            }
        )
