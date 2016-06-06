
This is a chat server app built using channels in django

## Installation

This is a standard Django project. Please refer to Django [documentation](https://docs.djangoproject.com/en/1.9/intro/overview/#install-it) for more details.

* Install requirements in the virtualenv

```
virtualenv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

* Postgres setup

```
create database dev_db;
create user chatuser with password 'password';
grant all privileges on database dev_db to chatuser;
```

* Run the inital migrations

```
python manage.py migrate
```


## Run Server

```./manage.py runserver```

### API
Login : POST `/accounts/login/`
Register: POST `/accounts/register/`
Load Room Chat: GET `/room/<room_name>` (Requires Auth)
Realtime updates demo: `/room/render/<room_name>` (Requires Auth)

Allowed `room_name`: `public`, `room1`, `room2`
