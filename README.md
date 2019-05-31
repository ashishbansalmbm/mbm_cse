//[![Encarta Logo](http://encartambm.in/static/img/logo_small.png)](http://encartambm.in\)

# MBM ENGINEERING COLLEGE CSE 2018 Website

Website for MBM ENGINEERING COLLEGE 2018


## Getting Started

This is a straight forward Django project. A little profeciency in Python is expected. 
Use Python3.

### Prerequisites

You'll need following software to get started.

```
Python3 
Django 
MySQL 
Sublime Text! 
venv | python3-venv | virtualenvwrapper | (or whatever floats your virtual env boat)
```

### Installing

To set up development environment follow these steps. Of course, it is assumed that you have already complied with the above prerequisites.

```
git clone git@github.com:ashishbansalmbm/mbm_cse.git 
cd into/wherever/you/cloned/this/repo
pip install -r requirements.txt
```

And Django stuff!

```
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

You should see the website running at http://127.0.0.1:8000

## Deployment

Standards Ubuntu server deployment with nginx and gunicorn. 

## Built With

* [Django](https://www.djangoproject.com/) - The web framework used
* [Python](https://www.python.org/) - Programming language for the uninitiated
* [pyCharm](https://www.jetbrains.com/pycharm/) - Yes, someone used that too.
* [chrome] - For designing purpose obviously.

## Contributing

Please be humane and contact the maintainer.

## Versioning

We don't use any versioning whatsoever in this project!
