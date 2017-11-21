from django.shortcuts import render
from random import randint
from django.conf import settings
from django.views.generic.base import TemplateView


class Index(TemplateView):
    template_name = 'jugadas.html'

    def get_context_data(self, **kwargs):
        jugadas = []
        for i in range(settings.NUMERO_JUGADAS):
            jugadas.append(generar_jugada())
        context = {'jugadas': jugadas}
        return context


def generar_jugada():
    numeros = []
    while(len(numeros) < 6):
        numero = str(randint(0, 45)).zfill(2)
        if numero not in numeros:
            numeros.append(numero)

    jugada = '-'.join(sorted(numeros))
    return jugada
