#-*- coding: utf-8 -*-
import datetime
from django.utils import timezone
from django.db import models
from annoying.fields import AutoOneToOneField
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django import forms


class Konferencja(models.Model):
    tytul = models.CharField("Tytuł konferencji",
                             max_length=80,
    )
    opis = models.CharField(max_length=250, )
    data_zamkniecia_zgloszen = models.DateTimeField("Zgłoszenia otwarte do:")
    data_wprowadzenia = models.DateTimeField("Data utworzenia wpisu",
                                             auto_now_add=True,
    )
    inauguracja = models.DateField("Data rozpoczęcia")

    def __unicode__(self):
        return "'%s'" % (self.tytul,)

    def otwarte_zapisy(self):
        """
        Sprawdza, czy w danym dniu zapisy są jeszcze otwarte.
        """
        #tnow = timezone.now()
        #tnow = tnow.astimezone(timezone.utc).replace(tzinfo=None)
        tnow = datetime.datetime.now()

        deadline = self.data_zamkniecia_zgloszen
        #deadline = deadline.astimezone(timezone.utc).replace(tzinfo=None)

        if tnow > deadline:
            return False
        else:
            return True

    otwarte_zapisy.Boolean = True

    def konferencja_nadchodzaca(self):
        """
        Zwraca wartosc True, jesli konferencja trwa lub dopiero nastapi,
        w przeciwnym razie zwraca False.
        """
        now_day = datetime.date.today()

        if self.inauguracja >= now_day:
            return "Tak"
        else:
            return "Nie"

    konferencja_nadchodzaca.short_description = "Czy zbliżająca się konferencja?"
    konferencja_nadchodzaca.Boolean = True

    def ilosc_sesji(self):
        """
        Funkcja zwraca ilość sesji powiązanych
        z konferencją
        """
        k = Konferencja.objects.get(pk=self.pk)
        ilosc_sesji = k.sesja_set.count()

        return ilosc_sesji

    ilosc_sesji.short_description = "Ilość sesji"

    def final(self):
        k = Konferencja.objects.get(pk=self.pk)
        ostatnia_sesja = k.sesja_set.latest('start')

        return ostatnia_sesja.start

    final.short_description = "Finał (data ostatniej sesji)"


    def inauguracja_godzina(self):
        """
        Zwraca godzinę pierwszej sesji
        """

        k = Konferencja.objects.get(pk=self.pk)
        pierwsza_sesja = k.sesja_set.order_by('start').latest('start')

        return pierwsza_sesja.start.strftime('%H:%M')

    final.inauguracja_godzina = "Godzina rozpoczęcia (godzina pierwszej sesji)"

    class Meta:
        ordering = ['inauguracja']
        verbose_name_plural = "konferencje"


BRAK = u' '
INZ = u'inż.'
MGRINZ = u'mgr inż.'
DR = u'dr'
DRIZN = u'dr inż.'
DRHAB = u'dr hab.'
PROFDRHAB = u'prof. dr hab.'

STOPIEN = (
    (BRAK, u' '),
    (INZ, u'inż.'),
    (MGRINZ, u'mgr inż.'),
    (DR, u'dr'),
    (DRIZN, u'dr inż.'),
    (DRHAB, u'dr hab.'),
    (PROFDRHAB, u'prof. dr hab.'),
)


class Prelegent(models.Model):
    """
    Wykorzystano https://github.com/skorokithakis/django-annoying#readme
    """
    user = AutoOneToOneField(User, primary_key=True)

    imie = models.CharField(max_length=30)
    nazwisko = models.CharField(max_length=30)
    tytul_naukowy = models.CharField("Stopień naukowy",
                                     max_length=15,
                                     choices=STOPIEN,
                                     default=BRAK,
    )
    jednostka_naukowa = models.CharField(max_length=120)
    nr_telefonu = models.CharField("Nr telefonu",
                                   max_length=14,
    )

    def __unicode__(self):
        return "%s %s %s" % (self.tytul_naukowy, self.imie, self.nazwisko)

    class Meta:
        ordering = ['user']
        verbose_name_plural = "prelegenci"

    def mail(self):
        uzy = User.objects.get(pk=self.user.pk)
        return uzy.email



class Sesja(models.Model):
    """
    Sesja jest w relacji jeden do wielu z Konferencja
    """
    konferencja = models.ForeignKey(Konferencja)
    temat = models.CharField("Temat sesji",
                             max_length=60,
    )
    lokalizacja = models.CharField("Miejsce sesji",
                                   max_length=70,
    )
    start = models.DateTimeField("Godzina i dzień rozpoczęcia")
    ilosc_miejsc_dla_prelegentow = models.PositiveIntegerField("Max. ilość miejsc",
                                                               default=8,
    )

    class Meta(object):
        ordering = ('start',)
        verbose_name_plural = "sesje"

    def ile_wolnych_miejsc_w_sesji(self):
        miejsc = self.ilosc_miejsc_dla_prelegentow
        sesja = Sesja.objects.get(pk=self.pk)
        ilosc_punktow = sesja.punktprogramu_set.count()
        return miejsc - ilosc_punktow

    ile_wolnych_miejsc_w_sesji.short_description = "Wolne miejsca"

    def ile_zajetych_miejsc_w_sesji(self):
        miejsc = self.ilosc_miejsc_dla_prelegentow
        sesja = Sesja.objects.get(pk=self.pk)
        ilosc_punktow = sesja.punktprogramu_set.count()
        return "%d/%d" % (ilosc_punktow, miejsc)

    ile_zajetych_miejsc_w_sesji.short_description = "Obłożenie"


    def __unicode__(self):
        return 'Sesja: "%s" | Konferencja: %s' % (self.temat, self.konferencja,)

    def get_admin_url(self):
        return "/admin/konferencje/sesja/%d/" % self.id

    def koniec_sesji(self):
        pocz = self.start
        miejsc_czas = self.ilosc_miejsc_dla_prelegentow * 15
        delta = datetime.timedelta(minutes=miejsc_czas)
        cz = pocz + delta
        return cz.strftime("%H:%M")

    koniec_sesji.short_description = "Koniec sesji (wg planu)"

    def czas_sesji(self):
        miejsc_czas = self.ilosc_miejsc_dla_prelegentow * 15

        return "%d min" % (miejsc_czas,)

    czas_sesji.short_description = "W minutach"

    def koniec_sesji_oblozenie(self):
        sesja = Sesja.objects.get(pk=self.pk)
        ilosc_punktow = sesja.punktprogramu_set.count()
        czas = abs(ilosc_punktow * 15)
        delta = datetime.timedelta(minutes=czas)
        pocz = self.start
        koniec = pocz + delta

        return koniec.strftime("%H:%M")


    koniec_sesji_oblozenie.short_description = "Koniec sesji(przy obłożeniu)"


ODRZUCONY = 0
NOWY = 1
PRZYPISANY = 2

STATUS = (
    (ODRZUCONY, 'Odrzucony'),
    (NOWY, 'Nowy'),
    (PRZYPISANY, 'Przypisany'),
)


class Zgloszenie(models.Model):
    """
    status: http://stackoverflow.com/questions/1160019/django-send-email-on-model-change
    lub http://stackoverflow.com/questions/1355150/django-when-saving-how-can-you-check-if-a-field-has-changed?lq=1
    """
    prelegent = models.ForeignKey(Prelegent)
    konferencja = models.ForeignKey(Konferencja, primary_key=False)
    tytul_wystapienia = models.CharField(verbose_name="Tytuł wystąpienia",
                                         max_length=100,
    )

    tresc_wystapienia = models.FileField(upload_to='teksty_zgloszenia/%Y/%m/%d/%H/%M')

    data_zgloszenia = models.DateTimeField("Data wpłynięcia zgłoszenia",
                                           auto_now=True)

    status = models.SmallIntegerField("Status",
                                      choices=STATUS,
                                      default=NOWY, )

    wybrana_sesja = models.ForeignKey(Sesja,
                                      blank=True,
                                      null=True, )

    uzasadnienie_odrzucenia = models.CharField("Uzasadnienie odrzucenia",
                                               max_length=300,
                                               blank=True,
                                               null=True,
                                               help_text="Wpisz uzasadnienie odmowy", )


    def status_zgloszenia(self):

        if self.status == 1:
            return "Nowe"
        elif self.status == 0:
            return "Odrzucone: %s" % (self.uzasadnienie_odrzucenia,)
        else:
            return "Przypisany: %s" % (self.wybrana_sesja,)

    status_zgloszenia.short_description = "Status | Opis"

    def __unicode__(self):
        return "%s : %s na %s" % (self.prelegent.__unicode__(),
                                  self.tytul_wystapienia,
                                  self.konferencja, )


    class Meta(object):
        verbose_name_plural = "zgłoszenia"

    def save(self, *args, **kwargs):
        print("save wywolano!!!")

        prel = Prelegent.objects.get(pk=self.prelegent)
        uname = User.objects.get(pk=prel.user.pk)
        email_prelegenta = uname.email

        if self.pk is not None:
            orig = Zgloszenie.objects.get(pk=self.pk)
            print(orig.status)
            if orig.status == self.status:
                print('Status bez zmian')
            elif orig.status == 1 and self.status == 0: #ODRZUCONY
                print('Odrzucam')
                message = 'Przykro nam! Zgloszenie o tytule wystapienia: "%s" zostalo odrzucone. Uzasadnienie: %s' % (
                    self.tytul_wystapienia,
                    self.uzasadnienie_odrzucenia,)

                send_mail('Biurkon: Twoje zgłoszenie zostało odrzucone',
                          message, 'biurkon@gmail.com',
                          [email_prelegenta, ],
                          fail_silently=False
                )
                print('Wyslano odrzucenie')

            elif orig.status == 1 and self.status == 2: #PRZYPISANY

                print("Tworze punkt. Przypisany")

                punkt = PunktProgramu(sesja=self.wybrana_sesja,
                                      tytul_naukowy=self.prelegent.tytul_naukowy,
                                      imie=self.prelegent.imie,
                                      nazwisko=self.prelegent.user.last_name,
                                      tytul_wystapienia=self.tytul_wystapienia,
                                      my_order=0,
                )

                print("Utworzylem punkt")
                punkt.save()

                message = u"Twoje zgłoszenie zostało zaakceptowane. W menu 'Twoje zgłoszenia' sprawdzisz swoją sesję."
                send_mail(u'Gratulujemy! Twoje zgłoszenie zostało zaakceptowane',
                          message, 'biurkon@gmail.com',
                          [email_prelegenta, ],
                          fail_silently=False,
                )

            else:
                message = u'Ważna wiadomość! Zgloszenie o tytule wystapienia: "%s" zostalo zmieniło pierwotny status. Uzasadnienie: %s' % (
                    self.tytul_wystapienia,
                    self.uzasadnienie_odrzucenia,)

                send_mail('Biurkon: Twoje zgłoszenie zmieniło pierwotny status',
                          message, 'biurkon@gmail.com',
                          [email_prelegenta, ],
                          fail_silently=False)

        super(Zgloszenie, self).save(*args, **kwargs)


class PunktProgramu(models.Model):
    """
    Podstsawowa jednostka budująca sesję. Zaakceptowane zgłoszenie jest
    'tranfsormowane' w punkt programu.
    """
    sesja = models.ForeignKey(Sesja)
    tytul_naukowy = models.CharField(max_length=15,
                                     choices=STOPIEN,
                                     default=BRAK,
                                     )
    imie = models.CharField(max_length=25)
    nazwisko = models.CharField(max_length=35)

    tytul_wystapienia = models.CharField(verbose_name="Tytuł wystąpienia",
                                         max_length=100,
                                         )

    my_order = models.PositiveIntegerField(blank=False,
                                           null=False,
                                           )

    class Meta(object):
        ordering = ('my_order',)
        verbose_name_plural = "zgłoszenia"

        #zgloszenie = models.OneToOneField(Zgloszenie,
        #                                 primary_key=False,
        #                                 blank=True,
        #                                 null=True,
        #                                 help_text="Ma zastosowanie tylko, gdy wystąpienie powstało w wyniku zgłoszenia",








  
    
    

    

    
    
    

    
    
    
    

    

    
    
