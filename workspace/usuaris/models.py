from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Perfil(models.Model):
    monedes = models.IntegerField(default=0)
    monedes_pendents = models.DecimalField(max_digits=10, decimal_places=4, default = 50) #float
    ultima_peticio = models.DateTimeField(auto_now=False, auto_now_add=True)
    fons = models.CharField(max_length=100, blank=True, default="")
    punts = models.IntegerField(default=0)
    usuari = models.OneToOneField(User)
    imatge = models.ImageField(max_length=500, upload_to= "usuaris_imatges", default="/usuaris_imatges/defaultUser.png")
    
    def __unicode__(self):
        return self.usuari.username
        
# signals.py
from django.db.models import signals
from django.dispatch import receiver

@receiver(signals.post_save, sender=User)
def assigna_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create( usuari = instance )
        
class Posesio(models.Model):
    usuari = models.ForeignKey(User)
    elements = models.ForeignKey("elements.Element")
    quantitat = models.IntegerField()
    quantitat_piscina = models.IntegerField(default=0)