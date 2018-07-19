from django.conf.urls import url
from django.contrib import admin

from dinela_search import views, views_data

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^data/load_listing$', views_data.LoadListingView.as_view(), name='load_listing'),
    url(r'^data/process_menus$', views_data.ProcessMenusView.as_view(), name='process_menus'),
    url(r'^data/update_search$', views_data.UpdateSearchIndexView.as_view(), name='update_search'),

    url(r'^test$', views.TestView.as_view(), name='test'),
    url(r'^search$', views.SearchView.as_view(), name='search'),
    url(r'^$', views.SearchView.as_view(), name='index'),
]
