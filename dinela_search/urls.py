from django.conf.urls import url
from django.contrib import admin

from dinela_search import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^data/load_listing$', views.LoadListingView.as_view(), name='load_listing'),
    url(r'^data/process_menus$', views.ProcessMenusView.as_view(), name='process_menus'),
    url(r'^data/update_search$', views.UpdateSearchIndexView.as_view(), name='update_search'),
]
