from functools import wraps
from django.shortcuts import redirect


def user_is_authenticated(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        if request.request.user.is_authenticated():
            return function(request, *args, **kwargs)
        else:
            return redirect('admin:index')
    return decorator
