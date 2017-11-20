from random import randint
import datetime

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Cliente (models.Model):
    """
    Clase con datos del cliente
    """

    GENERO_MASCULINO = 'masculino'
    GENERO_FEMENINO = 'femenino'
    GENERO_OTROS = 'otros'
    GENERO_CHOICES = (
        (GENERO_MASCULINO, 'Masculino'),
        (GENERO_FEMENINO, 'Femenino'),
        (GENERO_OTROS, 'Otros')
    )
    DOCUMENTO_DNI = 'dni'
    DOCUMENTO_PASAPORTE = 'pasaporte'
    DOCUMENTO_CHOICES = (
        (DOCUMENTO_DNI, u'DNI'),
        (DOCUMENTO_PASAPORTE, u'PASAPORTE')
    )
    user = models.OneToOneField(User)
    apellido_paterno = models.CharField(u'Apellido paterno', max_length=50, blank=True, null=True)
    apellido_materno = models.CharField(u'Apellido materno', max_length=50, blank=True, null=True)
    nombres = models.CharField(u'Nombres', max_length=100, blank=True, null=True)
    genero = models.CharField(u'Genero', choices=GENERO_CHOICES, max_length=20)
    fecha_nacimiento = models.DateField(u'Fecha de nacimiento')
    direccion = models.CharField(u'Dirección', max_length=100)
    departamento = models.CharField(u'Departamento', max_length=100)
    provincia = models.CharField(u'Provincia', max_length=100)
    distrito = models.CharField(u'Distrito', max_length=100)
    tipo_documento = models.CharField(u'Tipo de documento', choices=DOCUMENTO_CHOICES, max_length=20)
    numero_documento = models.CharField(u'Número de documento', max_length=8, validators=[
        RegexValidator(
            regex=r'\d{8}',
            message='Debe contener 8 dígitos',
            code='invalid_dni'
        ),
    ])
    fecha_afiliacion = models.DateTimeField(u'Fecha de afiliacion', auto_now_add=True)
    firma = models.ImageField(u'Firma', upload_to='fotos/%Y/%m/%d/', blank=True, null=True)

    class Meta:
        unique_together = ('tipo_documento', 'numero_documento')

    @property
    def nombre_completo(self):
        return u'{nombres} {a_paterno} {a_materno}'.format(
            nombres=self.nombres,
            a_paterno=self.apellido_paterno,
            a_materno=self.apellido_materno
        )


class Cuenta (models.Model):
    """
    Clase con datos de la cuenta
    """
    SOLES = 'soles'
    DOLARES = 'dolares'
    MONEDA_CHOICES = (
        (SOLES, u'Soles'),
        (DOLARES, u'Dólares')
    )

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    numero_cuenta = models.CharField(max_length=14, unique=True)
    tipo_moneda = models.CharField(u'Moneda', choices=MONEDA_CHOICES, max_length=20)
    saldo_actual = models.DecimalField(u'Saldo actual', default=0, max_digits=10, decimal_places=2)
    costo_mantenimiento = models.DecimalField(u'Costo de mantenimiento', default=0, max_digits=5, decimal_places=2)
    fecha_anulacion = models.DateField(u'Fecha de anulación', blank=True, null=True)

    def __init__(self, *args, **kwargs):
        self.numero_cuenta = self.generar_numero_cuenta()

    @property
    def generar_numero_cuenta(self):
        return '{}-{}'.format(self.generar_numero(3), self.generar_numero(10))

    def generar_numero(self, longitud):
        return ''.join(["%s" % randint(0, 9) for num in range(0, longitud)])


class Tarjeta (models.Model):

    """
    Clase con datos de la tarjeta
    """
    cuenta = models.OneToOneField(Cuenta, on_delete=models.CASCADE)
    numero = models.CharField(max_length=16, unique=True)
    mes_expiracion = models.CharField(max_length=2)
    anio_expiracion = models.CharField(max_length=4)
    cvv = models.CharField(max_length=3)
    vigencia = models.BooleanField()
    bloqueada = models.BooleanField()
    pin = models.CharField(max_length=4)

    def generar_numero(self, longitud, tarjeta=False, cvv=False):
        if cvv:
            inicial = str(randint(1, 9))
            return inicial.join(["%s" % randint(0, 9) for num in range(0, longitud-1)])
        if tarjeta:
            return '4'.join(["%s" % randint(0, 9) for num in range(0, longitud-1)])
        return ''.join(["%s" % randint(0, 9) for num in range(0, longitud)])

    @property
    def generar_numero_tarjeta(self):
        posible_numero = '{}'.format(self.generar_numero(16, tarjeta=True))
        while (not self.validar_numero(posible_numero)):
            posible_numero = '{}'.format(self.generar_numero(16, tarjeta=True))
        return posible_numero

    @property
    def validar_numero(self, numero):
        # paso 1
        impares = numero[1::2]
        pares = numero[::2]
        impares = [i * 2 for i in impares]
        # paso 2
        impares = [int((i%10 + (i-i%10)/10)) if i/10>=1 else i for i in impares]
        # paso 3 y 4
        suma = 0
        for i in impares:
            suma+=i
        for i in pares:
            suma+=i
        # paso 5
        if (suma%10 == 0):
            return True
        return False

    @property
    def generar_expiracion(self):
        ahora = datetime.datetime.now()
        meses = randint(24, 81)
        ahora = ahora + datetime.timedelta(months=meses)
        self.mes_expiracion = ahora.strftime('%m')
        self.anio_expiracion = ahora.strftime('%y')

    def __init__(self, *args, **kwargs):
        self.numero = self.generar_numero_tarjeta()
        self.generar_expiracion()
        self.cvv = self.generar_numero(3, cvv=True)
        self.pin = self.generar_numero(3)
