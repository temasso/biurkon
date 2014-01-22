#-*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from reportlab.pdfgen import canvas
from django.http import Http404
from konferencje.models import Konferencja, Sesja, Zgloszenie, Prelegent, PunktProgramu
from konferencje.forms import ZgloszenieForm


@login_required(login_url='/konta/login/')
def index(request):
    """
    test
    """
    return HttpResponse("Test")


@login_required(login_url='/konta/login/')
def TwojeZgloszenia(request):
    if request.user.is_staff:
        zgloszenia = None
        warning = "Jako pracownik musisz mieć uwtorzone konto Prelegenta celem dodawania własnych zgłoszeń."
        return render_to_response('konferencje/zgloszenia.html',
                                  {'zgloszenia': zgloszenia,
                                   'user': request.user,
                                   'warning': warning})
    else:
        prel = Prelegent.objects.get(user=request.user.pk)
        zgloszenia = Zgloszenie.objects.filter(prelegent=prel.pk)
        return render_to_response('konferencje/zgloszenia.html',
                                  {'zgloszenia': zgloszenia,
                                   'user': request.user})


class KonferencjeListView(ListView):
    model = Konferencja
    template_name = 'konferencje/konf_list.html'
    context_object_name = 'konferencje'


class KonferencjaDetailView(DetailView):
    """
    Widok konretnej konferencji z linkami do sesji
    """
    model = Konferencja
    template_name = 'konferencje/detail.html'
    context_object_name = 'konferencja'

    def get_context_data(self, **kwargs):
        context = super(KonferencjaDetailView, self).get_context_data(**kwargs)
        klucz = self.kwargs.get("pk")
        sessions = Sesja.objects.filter(konferencja=klucz)
        context['sesje'] = sessions
        context['klucz'] = klucz

        return context


@login_required(login_url='/konta/login/')
def zgloszenie_add(request, konferencja_pk):
    """
    Na poczatku trzeba sprawdzic, czy ktos juz nie wyslal zgloszenia
    na te konferencje
    """
    zglosz = Zgloszenie.objects.filter(konferencja=konferencja_pk)
    context = RequestContext(request)

    try:
        konferencja = Konferencja.objects.get(pk=konferencja_pk)
    except:
        raise Http404

    #sprawdzenie, czy już się ktoś zgłosił na te konferencje
    try:
        prel = Prelegent.objects.get(user=request.user.pk)
    except:
        return render_to_response('konferencje/already_sent.html',
                                  {'user': request.user, 'konferencja': konferencja,
                                   'staff': request.user.is_staff},
                                  context,)

    czy = zglosz.filter(prelegent=prel.pk).count()
    if czy == 1 or not konferencja.otwarte_zapisy() or request.user.is_staff:
        return render_to_response('konferencje/already_sent.html',
                                  {'user': request.user, 'konferencja': konferencja,
                                   'staff': request.user.is_staff},
                                  context,)
    else:
        if request.method == 'POST':
            print("jestem w POST")
            form = ZgloszenieForm(request.POST, request.FILES)

            if form.is_valid():
                nowe = form.save(commit=False)
                nowe.prelegent = prel
                nowe.konferencja = konferencja
                nowe.save()

                return HttpResponseRedirect('/konferencje/zgloszenia')
        else:
            form = ZgloszenieForm()

        return render_to_response('konferencje/zgloszenie_add.html',
                                  {'form': form, 'user': request.user, 'konferencja': konferencja},
                                  context,
        )


class SesjaDetailView(DetailView):
    """
    Widok dla konkretnej sesji
    """

    model = Sesja
    template_name = 'konferencje/sesja.html'
    context_object_name = 'sesja'

    def get_context_data(self, **kwargs):
        context = super(SesjaDetailView, self).get_context_data(**kwargs)
        klucz = self.kwargs.get("pk")
        punkty = PunktProgramu.objects.filter(sesja=klucz)
        context['punkty'] = punkty

        return context


def sesja_pdf(request, sesja_pk):
    """
    W toku, wynikiem będzie program sesji .pdf
    """
    sesja = Sesja.objects.get(pk=sesja_pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="program.pdf"'

    pdf = canvas.Canvas(response)
    pdf.drawString(100, 100, sesja.temat)

    pdf.showPage()
    pdf.save()

    return response





