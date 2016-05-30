from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager

class Element(models.Model):
    nom = models.CharField(max_length=200)
    usuaris_que_tenen_aquest_element = models.ManyToManyField( User , through="usuaris.Posesio", related_name="elements_que_poseeix" )
    preu = models.IntegerField()
    objects = InheritanceManager()

class Peix(Element):
    vida = models.IntegerField()
    atac = models.IntegerField()
    velocitat = models.IntegerField()
    imatge = models.ImageField(max_length=500, upload_to= "peixos_imatges", default="/peixos_imatges/default.png")
    thumbnail = models.ImageField(max_length=500, upload_to= "peixos_thubnails", default="/peixos_thubnails/default.png")
    monedes_per_hora = models.IntegerField()
    

class Decoracio(Element):
    imatge = models.ImageField(max_length=500, upload_to= "decoracio_imatges", default="/decoracio_imatges/default.png")
    posicioX = models.IntegerField()
    posicioY = models.IntegerField()