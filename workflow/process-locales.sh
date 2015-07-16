#!/bin/sh

../manage.py makemessages -e haml -e html -l fr
../manage.py makemessages -e js -d djangojs -l fr
../manage.py compilemessages -l fr
