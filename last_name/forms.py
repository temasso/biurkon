#-*- coding: utf-8 -*-
from django import forms
from registration_email.forms import EmailRegistrationForm

BRAK = ' '
INZ = 'inż.'
MGRINZ = 'mgr inż.'
DR = 'dr'
DRIZN = 'dr inż.'
DRHAB = 'dr hab.'
PROFDRHAB = 'prof. dr hab.'

STOPIEN = (
            (BRAK, ' '),
            (INZ, 'inż.'),
            (MGRINZ, 'mgr inż.'),
            (DR, 'dr'),
            (DRIZN, 'dr inż.'),
            (DRHAB, 'dr hab.'),
            (PROFDRHAB, 'prof. dr hab.'),
         )

class CustomEmailRegistrationForm(EmailRegistrationForm):

    def __init__(self,*args,**kwargs):
        super(EmailRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['nr_telefonu'].widget.attrs['class'] = "number"



    tytul_naukowy = forms.ChoiceField(choices=STOPIEN,
                                      label="Twój stopień",
                                      )
    first_name = forms.CharField(max_length=30,
                                 label="Podaj swoje imię",
                                 )
    last_name = forms.CharField(max_length=30,
                                label="Podaj swoje nazwisko",
                                )
    jednostka_naukowa = forms.CharField(max_length=120,
                                        label="Podaj nazwę swojej jednostki naukowej",
                                        )
    nr_telefonu = forms.CharField(max_length=14,
                                  label="Podaj numer kontaktowy",
                                  )







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

