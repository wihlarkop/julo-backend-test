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

```commandline
python manage.py migrate
```

```commandline
python manage.py createsuperuser
```

```commandline
python manage.py runserver 0.0.0.0:8000
```

then go to 
```djangourlpath
http://localhost:8000/api/v1/init
```