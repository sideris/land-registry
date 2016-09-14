# Plentific land registry app

This is a sample application for Plentific by Petros G. Sideris

We use d3.js to provide the graphs and Django with Postgres 9.5 for the 
backend

If you haven't setup the Postgres service one needs python-devel and the
username and password should be `postgres:test` at port `5432` and host
 `localhost`.

There wasn't any templating tool used, SCSS or any JS dependency management tool
due to the limited scope and lifecycle of this application.

To run the server just run `python manage.py runserver`, which will 
run a Django instance in a production environment

To load the data one needs to do `python manage.py load_data --large --clear`
but be warned it takes a long time. 

An online version can be found at `http://138.68.134.157` with a 
prepopulated database of 10m properties and 18m transactions
(could be down due to updates being pushed)