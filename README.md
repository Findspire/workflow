
# todo

* renommer en anglais (wip)
* imports relatif (wip)
* vue user : login, logout, ... (wip)
* permissions
* more doc
* more tests

# Doc

Run tests :

    ./manage.py test

Run coverage :

    coverage erase
    coverage run ./manage.py test
    coverage html

Dump db to json :

    ./manage.py dumpdata APP --format=json --indent=4 > workflow/apps/APP/fixtures/APP.json

Reset db :

    ./scripts/resetdb.py

Fill db with fake data :

    ./scripts/fake_data.py

---------------------------------------------------------

python manage.py migrate
python manage.py createsuperuser

via the django admin create:
    * a Group "manager" and add yourself
    * a Person instance

create
    persons
    competences
    items
    project

start a workflow
