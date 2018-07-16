from google.appengine.ext import vendor
vendor.add('lib')

from google.appengine.api import urlfetch
import requests
import requests_toolbelt.adapters.appengine

requests_toolbelt.adapters.appengine.monkeypatch()
urlfetch.set_default_fetch_deadline(60)
appstats_SHELL_OK = True
