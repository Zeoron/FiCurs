from django.conf.urls import url, include
from elements import views


urlpatterns = [
    url(r'^elements/', views.getElements, name='getElements'),
    url(r'^totsElements/', views.getTotsElements, name="recullTotsElsElements"),
    url(r'^getCofre/', views.getCofre, name="cofre"),
    url(r'^compraPeix/', views.compraPeix, name="compraPeix"),
    url(r'^treurePeix/', views.treurePeix, name="treurePeix"),
    url(r'^guardarPeix/', views.guardarPeix, name="guardarPeix"),
    url(r'^infoUsuari/', views.info_usuari, name="infoUsuari"),
    url(r'^tiraMonedes/', views.tiraMonedes, name="tiraMonedes"),
    url(r'^recollirMoneda/', views.recollirMoneda, name="recollirMoneda"),
]