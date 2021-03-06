from random import randint
from django.conf import settings
from django.views.generic.base import TemplateView
from .decorators import esta_logueado


class Index(TemplateView):
    template_name = 'jugadas.html'
    request = None

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        jugadas = []
        for i in range(settings.NUMERO_JUGADAS):
            jugadas.append(genera_jugada())
        context = {'jugadas': jugadas}
        return context

    @esta_logueado
    def get(self, request, *args, **kwargs):
        self.request = request
        return super(Index, self).get(request, *args, **kwargs)


def genera_jugada():
    numeros = []
    while(len(numeros) < 6):
        numero = str(randint(0, 45)).zfill(2)
        if numero not in numeros:
            numeros.append(numero)

    jugada = '-'.join(sorted(numeros))
    return jugada
