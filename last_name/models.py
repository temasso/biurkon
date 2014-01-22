#-*- coding: utf-8 -*-
from django.db import models


from django.dispatch import receiver
from registration.signals import user_registered
from konferencje.models import Prelegent

@receiver(user_registered)
def user_registered_handler(sender, user, request, **kwargs):

    prel = Prelegent(user=user,
                     imie = request.POST.get('first_name'),
                     nazwisko = request.POST.get('last_name'),
                     tytul_naukowy = request.POST.get('tytul_naukowy'),
                     jednostka_naukowa = request.POST.get('jednostka_naukowa'),
                     nr_telefonu = request.POST.get('nr_telefonu'),
                     )
    prel.save()

    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.save()



"""
Prelegent obejmuje:

user = AutoOneToOneField(User, primary_key=True)

    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    tytul_naukowy = models.CharField("Stopień naukowy",
                                     max_length=15,
                                     choices=STOPIEN,
                                     default=BRAK)
    jednostka_naukowa = models.CharField(max_length=120)
    #korespondencja = models.CharField("Adres korespondencyjny",
    #                                  max_length=150,
     #                                 blank=True,
     #                                 null=True)
    nr_telefonu = models.CharField("Nr telefonu",
                                   max_length=14)

"""