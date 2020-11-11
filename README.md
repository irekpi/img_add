# Image Upload - DRF

App that allows Users to add photos

Users are currently created in Admin panel and can have different plans created by Admin 

Admin is able to create arbitrary plans with configurable thumbnail sizes, presence of the link to the originally uploaded file, ability to generate expiring links

####3 basic plans:

    - basic - User can add photo and get url to 200x200 size
    - premum - User can add photo and get urls for 200x200, 400x400 and original size
    - enterprise - User can add photo and get urls for 200x200, 400x400 and original size and make expiration date in seconds
### Basics

    'Python 3.8'
    'Django 3.1.3'
    'djangorestframework 3.12.2'

### Get the project and install it 
    Git Clone - current repository - https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository

    Virtual Environment - create - https://docs.python.org/3/tutorial/venv.html

    "pip install -r requirements.txt" - https://pip.pypa.io/en/stable/reference/pip_freeze/


The most important thing

When we get all requirements we start our server with lines below


    python manage.py migrate
    python manage.py runserver
