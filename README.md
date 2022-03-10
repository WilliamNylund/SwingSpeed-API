# **Velofore API**

## Installation guide
clone repository and navigate to root folder:
```
cd SwingSpeed-API
```
Create an virtual environment
```
python3 -m venv env
```
Activate environment
```
source env/bin/activate
```
Install libraries and packages
```
pip install -r requirements.txt
```
```
cd velofore
```
Create your dev environment
```
cp template.env .env
```
Migrate
```
python manage.py migrate
```
```
python manage.py runserver
```
```
migrate: docker-compose run django python /code/manage.py migrate --noinput
```
```
makemigrations: docker-compose run django python /code/manage.py makemigrations
```
```
collectstatic: docker-compose run django python /code/manage.py collectstatic
```
```
stop: docker-compose down
```
```
start: docker-compose up
```
```
create-superuser: docker-compose run django python /code/manage.py createsuperuser
```
```
test: docker-compose run django python /code/manage.py test
```