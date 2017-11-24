from functools import wraps
from django.shortcuts import redirect


def esta_logueado(function):
    @wraps(function)
    def decorador(request, *args, **kwargs):
        if request.request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            return redirect('admin:index')
    return decorador
