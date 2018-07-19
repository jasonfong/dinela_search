from django.conf import settings
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import View
from google.appengine.api import search, users
from google.appengine.ext import ndb

from dinela_search.models import Restaurant, Account


class SearchView(View):
    def get(self, request, *args, **kwargs):
        google_user = users.get_current_user()

        authorized = False

        if google_user:
            account = Account.query(Account.email==google_user.email()).get()
            if account:
                authorized = True

        if not authorized:
            return HttpResponseForbidden()

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
                'query': query,
            }
        )


class TestView(View):
    def get(self, request, *args, **kwargs):
        google_user = users.get_current_user()

        authorized = False

        if google_user:
            account = Account.query(Account.email==google_user.email()).get()
            if account:
                authorized = True

        if not authorized:
            return HttpResponseForbidden()

        query = request.GET.get('q', '')
        index = search.Index(settings.SEARCH_INDEX)
        search_results = index.search(query)

        resto_ids = [d.doc_id for d in search_results]

        restaurants = ndb.get_multi([ndb.Key(Restaurant, k) for k in resto_ids])

        return render(
            request,
            'dinela_search/test.html',
            {
                'results': restaurants,
                'dinela_baseurl': settings.DINELA_BASEURL,
            }
        )
