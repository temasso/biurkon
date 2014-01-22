#-*- coding: utf-8 -*-
from django import forms
from konferencje.models import Zgloszenie


class ZgloszenieForm(forms.ModelForm):

    class Meta:
            model = Zgloszenie
            exclude = ('prelegent',
                       'status',
                       'uzasadnienie_odrzucenia',
                       'konferencja',
                       'wybrana_sesja',
            )

    def clean_tresc_wystapienia(self):
        """
        do poprawki, plik ma atrybut name oraz size()
        """
        plik = self.cleaned_data['tresc_wystapienia']
        rozmiar = len(plik)
        rozmiarmb = rozmiar / 1000000

        if rozmiarmb >= 1:
            raise forms.ValidationError('Rozmiar pliku nie może być większy niż 1MB')

        nazwa = plik.name

        try:
            nazwa = nazwa.split('.')[1]
        except:
            nazwa = 'brak_koncowki'

        allow = ['pdf', 'odt', 'doc', 'docx',]

        if nazwa not in allow:
            raise forms.ValidationError(u"Dozwolony format pliku: 'nazwa.pdf', nazwa.dot, nazwa.doc, nazwa.docx")
        return self.cleaned_data['tresc_wystapienia']



