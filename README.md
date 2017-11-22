# Proyecto de clase

Luego de crear un entorno virtual
```
mkdir env
virtualenv --no-site-package --distribute --python=python3 env
```
Para activar el entorno virtual
```
source env/bin/activate
```
Para instalar django
```
pip install django
```
Para crear un usuario (dentro del proyecto)
```
python manage.py createsuperuser
```