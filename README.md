# Task Complete
A task management application.    
[View a demo of the application.](https://fc-taskcomplete.herokuapp.com/) 


## Overview
Task complete is a full web application built with Django that includes user authentication and tests for the models, views and forms. The CSS framework used is Bulma.

[Go to test files](https://github.com/timamero/django-task-complete/tree/main/todo/tests)

## Instructions
* Clone this project
    ```
    https://github.com/timamero/django-task-complete.git
    ```

* Create virtual environment
    ```
    py -m venv venv
    ```

* Install Dependencies
    ```
    pip install -r requirements.txt
    ```
    Note: This project was configured with postgresql. It is required to use the ArrayField type in Models.  [See steps to set up postgresql in Django here](https://github.com/timamero/django-starting-template/blob/main/postgresql/configure-postgresql-database.md)

* Update settings.py Variables
    ```
    SECRET_KEY 
    DATABASES['default']['Name']
    DATABASES['default']['User']
    DATABASES['default']['Password']
    E_USER
    E_HOST
    E_PORT
    E_PASSWORD
    ```
    * To generate a new secret key, enter the following into the command line:
        ```
        python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
        ```

 * Run Database Migrations 
    ```
    py manage.py makemigrations
    py manage.py migrate
    ```

* Create Superuser
    ```
    py manage.py createsuperuser
    ```

* Run server
    ```
    py manage.py runserver
    ```
