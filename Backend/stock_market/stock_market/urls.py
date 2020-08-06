"""stock_market URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from stock import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^nifty_50$', views.fetch_nifty50_data, name="Top 50 stock"),
    url(r'^all_ticker$', views.get_list_of_ticker, name="Get list of all ticker"),
    url(r'^ticker$', views.map_url, name="Get data from user defined"),

]
