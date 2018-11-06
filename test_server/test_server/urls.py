"""test_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
import sys
import os

#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from addressapp.api import AddressesList
from addressapp.views import main, get_contacts, addressesbook, delete_person, notfound, PageCounts

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='API name')
urlpatterns = [
    url(r'^docs/', schema_view)
]
print('test')
urlpatterns += [
    #url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$',main, name='home'),
    url(r'^book/',addressesbook,name='addressesbook'),
    url(r'^delete/(?P<name>.*)/',delete_person, name='delete_person'),
    url(r'^book-search/',PageCounts.as_view(), name='get_contacts'),
    url(r'^addresses-list/', AddressesList.as_view(), name='addresses-list'),
    url(r'^notfound/',notfound, name='notfound'),
    url(r'^admin/',admin.site.urls),
]
