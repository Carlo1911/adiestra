from django.contrib.auth.models import User
from banco.models import Tarjeta

class MyCustomBackend(object):

    def authenticate(self, numero_tarjeta=None, pin=None):

        try:
            tarjeta = Tarjeta.objects.get(numero_tarjeta=numero_tarjeta,pin=pin)

            if tarjeta:
                return tarjeta.cliente.user
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None