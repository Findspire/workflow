
# todo

* renommer en anglais (wip)
* vue user : login, logout, ... (wip)
* permissions
* more doc
* more tests

# Basic setup

Don't forget to build the css :

    ./tools/build_css.sh

Syncdb :
If you use the plain django's command `syncdb`, you will need to create a Person instance for the django's superuser. You should use the following script.

    ./scripts/resetdb.py

Fill db with fake data :

    ./scripts/fake_data.py

# Dev tools

Run tests :

    ./manage.py test

Run coverage :

    coverage erase
    coverage run ./manage.py test
    coverage html

Dump db to json :

    ./manage.py dumpdata APP --format=json --indent=4 > workflow/apps/APP/fixtures/APP.json

---------------------------------------------------------

python manage.py migrate
python manage.py createsuperuser
via the django admin create a Person instance

create
    persons
    competences
    items
    project

start a workflow
