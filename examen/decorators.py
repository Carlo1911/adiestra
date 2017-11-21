from django.core.exceptions import PermissionDenied
from functools import wraps


def user_is_authenticated(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):
        return function(request, *args, **kwargs)
    return decorator
