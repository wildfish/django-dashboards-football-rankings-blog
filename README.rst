Football rankings with django-dashboards
========================================

This is the source code for the blog/demo of `django-dashboards <https://github.com/wildfish/django-dashboards>`_

Setup
-----

Create a pyenv environment:

::

    pyenv virtualenv 3.11.0 django-dashboards-football-rankings
    pyenv activate django-dashboards-football-rankings
    pip install -r requirements.txt


Initial setup of DB:

::

    python manage.py migrate

Pull the data from the FiveThirtyEight repo:

::

    python manage.py import

Run dev server:

::

    python manage.py runserver

Visit http://127.0.0.1:8000/dashboard/football/rankingsdashboard/

There are also some examples of tests to run against dashboards at demo/tests, run with:

::

    pytest

