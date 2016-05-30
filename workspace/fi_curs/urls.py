"""fi_curs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from usuaris import views as vista_usuaris
from elements import views as vista_elements
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = ([
    url(r'^$', vista_usuaris.p_inicial, name='inicial'),
    url(r'^elements/', include('elements.urls', namespace="elements")),
    url(r'^login/', vista_usuaris.vista_login, name="login"),
    url(r'^registre/', vista_usuaris.vista_signup, name="registre"),
    url(r'^sortir/', vista_usuaris.vista_logout, name="sortir"  ),
    url(r'^getEstadistiques/', vista_elements.getEstadistiques, name="getEstadistiques"),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
      + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
               )
