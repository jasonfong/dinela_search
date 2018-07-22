import logging
import os

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.utils.http import urlencode
from django.views.generic import View
from google.appengine.api import memcache, search, users
from google.appengine.ext import ndb

from dinela_search.models import Restaurant, Account


class SearchView(View):
    def get(self, request, *args, **kwargs):
        memcache_client = memcache.Client()
        user_ip = request.META['REMOTE_ADDR']
        call_count = memcache_client.get(user_ip)
        if call_count and call_count >= settings.RATE_LIMIT:
            return HttpResponse("Rate Limit Exceeded", status=429)

        if call_count:
            call_count += 1
        else:
            call_count = 1
        memcache_client.set(user_ip, call_count, time=settings.RATE_LIMIT_WINDOW)

        if not int(os.getenv('PUBLIC_MODE', 0)):
            google_user = users.get_current_user()
            authorized = False

            if google_user:
                account = Account.query(Account.email==google_user.email()).get()
                if account:
                    authorized = True

            if not authorized:
                return HttpResponseForbidden()

        query_clauses = []

        query = request.GET.get('q', '').strip()
        cuisine = request.GET.get('cuisine', '').strip()
        neighborhood = request.GET.get('neighborhood', '').strip()
        limit = int(request.GET.get('limit', settings.DEFAULT_SEARCH_LIMIT))

        if limit > settings.HARD_SEARCH_LIMIT:
            limit = settings.HARD_SEARCH_LIMIT

        if query:
            query_clauses.append(query)

        if cuisine:
            query_clauses.append('cuisine:"%s"' % cuisine)
        if neighborhood:
            query_clauses.append('neighborhood:"%s"' % neighborhood)

        combined_query = ' AND '.join(query_clauses)

        logging.debug('combined query: %s' % combined_query)

        index = search.Index(settings.SEARCH_INDEX)
        search_query = search.Query(
            query_string=combined_query,
            options=search.QueryOptions(limit=limit)
        )
        search_results = index.search(search_query)

        resto_ids = [d.doc_id for d in search_results]

        restaurants = ndb.get_multi([ndb.Key(Restaurant, k) for k in resto_ids])
        restaurants.sort(key=lambda x: x.name)

        return render(
            request,
            'dinela_search/index.html',
            {
                'results': restaurants,
                'dinelaBaseurl': settings.DINELA_BASEURL,
                'query': query,
                'selectedCuisine': cuisine,
                'selectedNeighborhood': neighborhood,
                'cuisines': Restaurant.CUISINE_CHOICES,
                'neighborhoods': Restaurant.NEIGHBORHOOD_CHOICES,
                'limit': limit,
            }
        )
