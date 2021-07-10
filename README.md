[TOC]



# Directory

```shell
.#project direcotry
├── backend									
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py									#global url
│   └── wsgi.py
├── dashboard								#application directory (put your .py file in here)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── Common_Functions.py						#file for shared funtions in application
│   ├── completeness_class.py
│   ├── Consistency.py
│   ├── Datevalide.py
│   ├── IntegrateFunction.py
│   ├── TBG_Function.py
│   ├── forms.py								#form class
│   ├── models.py
│   ├── outlier.py
│   ├── tests.py
│   ├── Uniqueness.py	
│   ├── urls.py									#urls within the application
│   ├── Validity.py	
│   └── views.py
#core file for render templates
├── db.sqlite3									#not used
├── manage.py
├── media
│   └── csvs									#directory for uploaded files
│       ├── Pokemon.csv
│       └── heart.csv
├─static
│   └─dashboard
│      ├─css
│      ├─img
│      └─js
└── templates									#HTML templates
│   ├── TBGeneral.html
│   ├── accueil.html
│   ├── boxes.html
│   ├── choose_type.html
│	├── contribution.html
│   ├── form.html
│   ├── inspection.html
│   ├── showtype.html
│   ├── statistics.html
│   └── uploadplus.html
├── mysqlclient-1.4.6-cp37-cp37m-win_amd64.whl	#file for installing interface between Python and MySQL
└── README.md

10 directories, 45 files
```

# Required environment

- Python 3.6+
- Django 2+
- MySQL 5.7
- Pandas
- NumPy
- SciPy

# How to run

> In current directory, execute `python manage.py runserver`

