#!/bin/bash

cd workflow

../manage.py makemessages -e haml -e py -a
../manage.py compilemessages
