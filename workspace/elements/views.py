from django.shortcuts import render

from elements.models import Element, Peix, Decoracio
import json
from model_utils.managers import InheritanceManager
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from usuaris.models import Perfil, Posesio
from datetime import datetime
from django.utils.timezone import utc
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
# Create your views here.

@login_required
def getElements(request):
    #tots_els_elements = request.user.elements_que_poseeix.select_subclasses()
    totes_les_posessions = request.user.posesio_set.all()
    llista_peixos = []
    llista_deco = []
    #for element in tots_els_elements:
    for posesio in totes_les_posessions:
        for _ in range(0,posesio.quantitat):
            element = Element.objects.filter( pk = posesio.elements.id ).select_subclasses().get()
            if isinstance( element, Peix ):
                nou_element = { 'nom': element.nom, 'monedes_per_hora': element.monedes_per_hora }
                llista_peixos.append(nou_element)
            else:
                nou_element = { 'nom': element.nom, 'preu': element.preu }
                llista_deco.append(nou_element)
    
    
    tot = { 'peixos': llista_peixos, 'deco': llista_deco }
    
    json_a_retornar = json.dumps(
            {
                'elements': tot
            }
        )
    return HttpResponse(json_a_retornar, content_type='application/json')


#BOTIGA
def getTotsElements(request):
    tots_els_elements = Element.objects.select_subclasses().all()
    llista_peixos = []
    llista_deco = []
    for element in tots_els_elements:
        if isinstance( element, Peix ):
            nou_element = { 'nom': element.nom, 'preu': element.preu, 'thubmnail':element.thumbnail.url, 'monedes_hora': element.monedes_per_hora }
            llista_peixos.append(nou_element)
        else:
            nou_element = { 'id': element.id,'nom': element.nom, 'preu': element.preu, 'imatge':element.imatge }
            llista_deco.append(nou_element)
    
    tot = { 'peixos': llista_peixos, 'deco': llista_deco }
    
    json_a_retornar = json.dumps(
            {
                'elements': tot
            }
        )
    return HttpResponse(json_a_retornar, content_type='application/json')



def getCofre(request):
    #tots_els_elements = request.user.elements_que_poseeix.select_subclasses()
    totes_les_posessions = request.user.posesio_set.all()
    llista_peixos = []
    llista_deco = []
    #for element in tots_els_elements:
    for posesio in totes_les_posessions:
        element = Element.objects.filter( pk = posesio.elements.id ).select_subclasses().get()
        if isinstance( element, Peix ):
            nou_element = {'id': posesio.id, 'quantitat': posesio.quantitat, 'quantitatpeixera': posesio.quantitat_piscina, 'nom_peix': element.nom, 'imatge': element.imatge.url ,  'monedes_per_hora': element.monedes_per_hora, 'velocitat':int(element.velocitat), }
            llista_peixos.append(nou_element)
        else:
            nou_element = { 'nom': element.nom, 'preu': element.preu }
            llista_deco.append(nou_element)
    
    
    tot = { 'peixos': llista_peixos, 'deco': llista_deco }
    
    json_a_retornar = json.dumps(
            {
                'posesions': tot
            }
        )
    return HttpResponse(json_a_retornar, content_type='application/json')


def compraPeix(request):
    info = "Res"
    if request.method == 'POST':
        info = json.loads(request.body)
        peix_seleccionat = Peix.objects.get(nom = info['idPeix'])
        perfil_usuari = Perfil.objects.get(usuari = request.user)
        if perfil_usuari.monedes >= peix_seleccionat.preu:
            try:
                posesio = request.user.posesio_set.get(elements__nom = peix_seleccionat.nom)
                perfil_usuari.monedes = perfil_usuari.monedes - peix_seleccionat.preu
                posesio.quantitat = posesio.quantitat + 1
                posesio.save()
                resposta = json.dumps({
                    'resposta':'Ja te el peix'
                })
            except Posesio.DoesNotExist:
                perfil_usuari.monedes = perfil_usuari.monedes - peix_seleccionat.preu
                nova_posesio = Posesio()
                nova_posesio.usuari = request.user
                nova_posesio.quantitat = 1
                nova_posesio.elements = peix_seleccionat
                nova_posesio.save()
                resposta = json.dumps({
                    'resposta':'No te el peix'
                })
            perfil_usuari.save()
        else:
            resposta = json.dumps({
                'resposta':'No te diners!'
                })
            
    return HttpResponse(resposta, content_type='application/json');
    
def treurePeix(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        peix_seleccionat = Peix.objects.get(nom = info['idPeix'])
        perfil_usuari = Perfil.objects.get(usuari = request.user)
        try:
            posesio = request.user.posesio_set.get(elements__nom = peix_seleccionat.nom)
            p1 = Posesio.objects.filter(quantitat_piscina__gt = 0)
            p2 = Posesio.objects.filter(usuari = request.user, quantitat_piscina__gt = 0)
            total_en_peixera = 0
            for tot in p2:
                total_en_peixera += tot.quantitat_piscina
                print tot.elements.nom
                print tot.quantitat_piscina
            
            if total_en_peixera < 15:
                if posesio.quantitat_piscina<posesio.quantitat:
                    posesio.quantitat_piscina = posesio.quantitat_piscina + 1
                    resposta = json.dumps({
                        'resposta':'true'
                    })
                else:
                    posesio.quantitat_piscina = posesio.quantitat
                    resposta = json.dumps({
                        'resposta':'false'
                    })
                posesio.save()
            else:
                resposta = json.dumps({
                        'resposta':'No pots treure mes peixos'
                    })
        except Posesio.DoesNotExist:
                resposta = json.dumps({
                    'resposta':'Error, aquest peix no el tens en posesio'
                })
    else:
        resposta = json.dumps({
                    'resposta':'Peticio denegada'
                })
    return HttpResponse(resposta, content_type='application/json');

def guardarPeix(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        peix_seleccionat = Peix.objects.get(nom = info['idPeix'])
        perfil_usuari = Perfil.objects.get(usuari = request.user)
        try:
            posesio = request.user.posesio_set.get(elements__nom = peix_seleccionat.nom)
            
            if posesio.quantitat_piscina != 0:
                posesio.quantitat_piscina = posesio.quantitat_piscina - 1
                resposta = json.dumps({
                    'resposta':'Peix guardat!'
                })
            else:
                resposta = json.dumps({
                    'resposta':'Ja tens tots els peixos guardats!'
                })
            posesio.save()
        except Posesio.DoesNotExist:
                resposta = json.dumps({
                    'resposta':'Error, aquest peix no el tens en posesio'
                })
    else:
        resposta = json.dumps({
                    'resposta':'Peticio denegada'
                })
    return HttpResponse(resposta, content_type='application/json');
    
    
def info_usuari(request):
    perfil_usuari = Perfil.objects.get(usuari = request.user)
    totes_les_posessions = request.user.posesio_set.all()
    total_peixos_comprats = 0
    for posesio in totes_les_posessions:
        element = Element.objects.filter( pk = posesio.elements.id ).select_subclasses().get()
        if isinstance( element, Peix ):
            total_peixos_comprats += posesio.quantitat
    info_perfil = {
                    'nom':request.user.username,
                    'monedes':perfil_usuari.monedes,
                    'fons':perfil_usuari.fons,
                    'imatgePerfil': perfil_usuari.imatge.url,
                    'peixosComprats': total_peixos_comprats,
                }
    resposta = json.dumps({
        'resposta': info_perfil
        });
    return HttpResponse(resposta, content_type='application/json');

 

def tiraMonedes(request):
    data_actual = datetime.utcnow().replace(tzinfo=utc)
    perfil_usuari = Perfil.objects.get(usuari = request.user)
    totes_les_posessions = request.user.posesio_set.all()
    monedes_per_hora = 0
    for a in totes_les_posessions:
        if a.quantitat_piscina > 0:
            element = Element.objects.filter( pk = a.elements.id ).select_subclasses().get()
            if isinstance( element, Peix ):
                for _ in range(0,a.quantitat_piscina):
                    monedes_per_hora += element.monedes_per_hora
    dif = data_actual - perfil_usuari.ultima_peticio
    total_segons = dif.total_seconds()/60
    perfil_usuari.monedes_pendents += Decimal(monedes_per_hora*total_segons/60)
    perfil_usuari.ultima_peticio = datetime.now().today()
    perfil_usuari.save()
    resposta = json.dumps({
        'resposta': int(perfil_usuari.monedes_pendents)
        });
    return HttpResponse(resposta, content_type='application/json');
    
def recollirMoneda(request):
    if request.method == 'POST':
        perfil_usuari = Perfil.objects.get(usuari = request.user)
        if (perfil_usuari.monedes_pendents - Decimal(1))>=Decimal(0):
            perfil_usuari.monedes_pendents -= Decimal(1)
            perfil_usuari.monedes += Decimal(1)
            perfil_usuari.save()
        resposta = json.dumps({
            'resposta': perfil_usuari.monedes
            }, cls=DjangoJSONEncoder);
    else:
        resposta = json.dumps({
            'resposta': "Peticio denegada!"
            });
    return HttpResponse(resposta, content_type='application/json');
    
def getEstadistiques(request):
    total_usuaris = User.objects.count()
    total_peixos_comprats = 0
    total_monedes = 0
    total_monedes_pendents = 0
    totes_les_posesions = Posesio.objects.all()
    for posesio in totes_les_posesions:
        total_peixos_comprats += posesio.quantitat
    
    tots_els_perfils = Perfil.objects.all()
    for perfil in tots_els_perfils:
        total_monedes += perfil.monedes
        total_monedes_pendents += perfil.monedes_pendents
    resposta = json.dumps({
            'dades': {
                'total_usuaris': total_usuaris,
                'total_peixos': total_peixos_comprats,
                'total_monedes': total_monedes,
                'total_monedes_pendents': int(total_monedes_pendents),
            }
            }, cls=DjangoJSONEncoder);
    return HttpResponse(resposta, content_type='application/json');
    