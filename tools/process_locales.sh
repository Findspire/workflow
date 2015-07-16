#!/usr/bin/env bash

cd workflow/

/usr/bin/env python ../manage.py makemessages -e html -e haml -a
/usr/bin/env python ../manage.py makemessages -d djangojs -e js -a

/usr/bin/env python ../manage.py compilemessages

