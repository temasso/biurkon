#-*- coding: utf-8 -*-

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from adminsortable.admin import SortableInlineAdminMixin
from django.forms import TextInput, Textarea
from django.db import models
from konferencje.models import Konferencja, Sesja, Prelegent, Zgloszenie, PunktProgramu

class SesjaModForm(forms.ModelForm):

    class Meta:
        model = Sesja

    def clean_start(self):
        print("WAWA")
        try:
            kid = self.cleaned_data['konferencja']
        except:
            raise forms.ValidationError("Najpierw utwórz i zapisz konferencję, następnie dodaj nową sesję. FIRST")

        print("pzed 2 tra")
        try:
            konferencja = Konferencja.objects.get(pk=kid.id)
        except:
            raise forms.ValidationError("Najpierw utwórz i zapisz konferencję, następnie dodaj nową sesję")


        start_konfa = konferencja.inauguracja
        start_sesja = self.cleaned_data['start']

        if start_sesja.date() < start_konfa:
            mes = "Sesja nie może zaczynać się przed dniem inauguracji konferencji, czyli %s" % (start_konfa,)
            raise forms.ValidationError(mes)

        return self.cleaned_data['start']


class SesjaLinkInline(admin.TabularInline):
    """
    http://stackoverflow.com/questions/2857001/adding-links-to-full-change-forms-for-inline-items-in-django-admin
    """
    model = Sesja
    extra = 0
    form = SesjaModForm

    can_delete = False

    def admin_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,
            instance._meta.module_name),
                      args=[instance.id]
        )
        return mark_safe(u'<strong><a href="{u}">Zarządzaj tą sesją</a></strong>'.format(u=url))

    readonly_fields = ('admin_link',)

class KonferencjaModForm(forms.ModelForm):
    opis = forms.CharField(widget=forms.Textarea,)

    class Meta:
        model = Konferencja

class KonferencjaAdmin(admin.ModelAdmin):

    inlines = [SesjaLinkInline,]

    list_display = ('tytul',
                    'inauguracja',
                    'final',
                    'data_zamkniecia_zgloszen',
                    'otwarte_zapisy',
                    'konferencja_nadchodzaca',
                    'ilosc_sesji'
    )

    list_filter = ['data_zamkniecia_zgloszen','inauguracja']
    search_fields = ['tytul']
    date_hierarchy = 'inauguracja'
    save_on_top = True
    form = KonferencjaModForm

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80',})},

    }


class PunktProgramuInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PunktProgramu
    extra = 0



class SesjaAdmin(admin.ModelAdmin):

    form = SesjaModForm
    inlines = [PunktProgramuInline,]

    list_display = ['__unicode__',
                    'start',
                    'koniec_sesji',
                    'ile_wolnych_miejsc_w_sesji',
                    'ile_zajetych_miejsc_w_sesji',
                    'koniec_sesji_oblozenie',
                    ]

    date_hierarchy = 'start'
    list_filter = ['start']



admin.site.register(Konferencja,KonferencjaAdmin)
admin.site.register(Sesja,SesjaAdmin)

class ZgloszenieAdminForm(forms.ModelForm):
    """
    http://stackoverflow.com/questions/949268/django-accessing-the-model-instance-from-within-modeladmin
    """

    uzasadnienie_odrzucenia = forms.CharField(widget=forms.Textarea,
                                              required=False,
                                              max_length=300,)

    class Meta:
        model = Zgloszenie


    def __init__(self, *args, **kwargs):
        super(ZgloszenieAdminForm, self).__init__(*args, **kwargs)
        print(self.instance.pk)
        self.fields['wybrana_sesja'].queryset = Sesja.objects.filter(konferencja=self.instance.pk)


    def clean_wybrana_sesja(self):

        status = self.cleaned_data['status']

        try:
            sesja = self.cleaned_data['wybrana_sesja']
        except:
            sesja = None


        if sesja != None and status == 2:
            konkretna_sesja = Sesja.objects.get(pk=sesja.pk)
            limit = konkretna_sesja.ile_wolnych_miejsc_w_sesji()
            print("limit:")
            print(limit)

            if limit == 0:
                raise forms.ValidationError("Limit miejsc dla tej sesji wyczerpany! Zwiększ jej limit lub zapisz na inną.")

        if status == 1 and sesja is not None:
            raise forms.ValidationError("Przypisałeś sesję podczas gdy status zgłoszenia jest NOWY."
                                        " Czy jesteś pewien? Jeżeli status pozostaje NOWY, ustaw wybraną sesję na pustą. "
                                        "W przeciwnym razie przypisz zgłoszenie do sesji")

        if status == 2 and sesja is None:
            raise forms.ValidationError("Status PRZYPISANY wymaga wybrania sesji!")
        return self.cleaned_data['wybrana_sesja']



    def clean_uzasadnienie_odrzucenia(self):

        status = self.cleaned_data['status']

        try:
            uzasadnienie = self.cleaned_data['uzasadnienie_odrzucenia']
        except:
            uzasadnienie = "puste"

        if status == 0 and len(uzasadnienie) < 30 :
            raise forms.ValidationError("Odrzucenie zgłoszenia wymaga uzasadnienia! Min. 30 znaków.")
        else:
            return self.cleaned_data['uzasadnienie_odrzucenia']



class ZgloszenieAdmin(admin.ModelAdmin):

    form = ZgloszenieAdminForm

    list_display = ('status',
                    'prelegent',
                    'tytul_wystapienia',
                    'konferencja',
                    'status_zgloszenia',
                    'data_zgloszenia',
    )


admin.site.register(Zgloszenie,ZgloszenieAdmin)


class PrelegentInline(admin.TabularInline):

    model = Prelegent
    extra = 0




class PrelegentAdmin(admin.ModelAdmin):

    list_display = ('tytul_naukowy',
                    'imie',
                    'nazwisko',
                   'mail',
                    'nr_telefonu',
                    'jednostka_naukowa',
                 #   'user.date_joined',
                 #   'user.last_login',
                 #   'user.is_active',

    )

    #list_filter = ('user.is_active', 'user.date_joined','user.last_login')
    #search_fields = ['last_name']


admin.site.register(Prelegent,PrelegentAdmin)



