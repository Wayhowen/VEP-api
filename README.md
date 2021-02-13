# Django API

Django API for VEP


## Running:
### Using docker-compose:
1.) For Internal API  
    `docker-compose up api_internal`  

2.) For External API  
    `docker-compose up api_external`
### Manually:
1.) Install `Python 3.9.0` or higher  
2.) For each API, install all dependencies using:  
    `pip install -r api_[external/internal]/requirements.txt`  
3.) Start Django server using:  
    `python manage.py runserver 0.0.0.0:8000 --settings=api_internal.settings.base`

Important notice: this is only a development, 1 thread server and therefore should not be used in productiony