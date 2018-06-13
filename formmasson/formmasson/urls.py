"""formmasson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from main.views import CustomFormView,HomePageView,FormResponseListView,CreateEditFormView

urlpatterns = [
    url(r'^$',HomePageView.as_view(),name='home'),
    url(r'^form/(?P<form_pk>\d+)/$',CustomFormView.as_view(),name='custom-form'),
    url(r'^form/(?P<form_pk>\d+)/responses/$',FormResponseListView.as_view(),name='form-responses'),
    url(r'form/(?P<form_pk>\d+)/edit/$', CreateEditFormView.as_view(), name='edit-form'),
    url(r'form/new/$', CreateEditFormView.as_view(), name='create-form'),
    url(r'^admin/', admin.site.urls),
    

]
