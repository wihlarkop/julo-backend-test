# Backend Test

## Installation

first create virtual environment python

```commandline
python -m venv env
```

then you need install requirements for running

```commandline
pip install -r requirements.txt
```
then you need migrate the migrations file for create sqlite database
```commandline
python manage.py migrate
```
then you need to createsuperuser for login
```commandline
python manage.py createsuperuser
```
now you can run server python
```commandline
python manage.py runserver 0.0.0.0:8000
```

then go to for get user uuid
```djangourlpath
http://localhost:8000/admin/account/customuser/
```