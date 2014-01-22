#-*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from models import Konferencja, Zgloszenie, Prelegent
from django.contrib.auth.models import User
from django.core.mail import send_mail
import datetime
from django.utils import timezone


"""
@receiver(post_save, sender=Konferencja)
def druk(sender, instance,**kwargs):
   
   # Dodaje dni do konferencji wg ilosci zadeklarowanej w polu
   # czas_trwania_dni.
    
    print("Utworzono konfe")
    print(instance.tytul)
    print(instance.id)
    
    init_date = instance.inauguracja
    ile_przed = datetime.timedelta(days=-7)
    
    #Trzeba wprowadzić zabezpieczenie
    #przed pomnażaniem przy każdym zapisie na zasadzie 
    #czy data utworzenia jest w okolicach minuty
    #data_wprowadzenia
    
    
    #if datetime.datetime.now()  < instance.data_wprowadzenia + datetime.timedelta(seconds=20):
    t = timezone.now()
    t = t.astimezone(timezone.utc).replace(tzinfo=None)
    
    wpro = instance.data_wprowadzenia
    wpro = wpro.astimezone(timezone.utc).replace(tzinfo=None)

    
    if t  <  wpro + datetime.timedelta(seconds=20):
        for d in range(instance.czas_trwania_dni):
            nastepny = datetime.timedelta(days=d)
            data_kol = init_date + nastepny
            ko = data_kol + ile_przed
            day = Dzien.objects.create(konferencja=instance,
                                       nr_poz=d+1,
                                       data=data_kol,
                                       koniec_rekrutacji=ko,
                                       )
            day.save()
    else:
        pass
"""    
    
#----
    
"""
: do admina http://stackoverflow.com/questions/4721771/get-current-user-log-in-signal-in-django
@receiver(pre_save, sender=Zgloszenie)
def accept_notification_status(sender, instance,**kwargs):
    
    print("Nowe zgloszenie")
    
    prel = Prelegent.objects.get(pk=instance.prelegent)
    uname= User.objects.get(pk=prel.user)
    
    if instance.is_accept:
        send_mail('Twoje zgłoszenie zostało zaakceptowane', \
                  'Zgłoszenie ' + instance.__unicode__ + \
                  'zakceptowane', 'biurkon@gmail.com', \
                  [str(uname.email),], fail_silently=False)  
    else:
        send_mail('Twoje zgłoszenie zostało niezaakceptowane', \
                  'Zgłoszenie ' + instance.__unicode__ + \
                  'niezakceptowane', 'biurkon@gmail.com', \
                  [str(uname.email),], fail_silently=False)     
          
  """  


