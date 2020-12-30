#!/bin/bash

rm -rf cycleshareapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations cycleshareapi
python manage.py migrate cycleshareapi
python manage.py loaddata users.json
python manage.py loaddata tokens.json
python manage.py loaddata biketypes.json
python manage.py loaddata bikesizes.json
python manage.py loaddata payments.json
python manage.py loaddata states.json
python manage.py loaddata riders.json
python manage.py loaddata reviews.json
python manage.py loaddata paymentsjoin.json
python manage.py loaddata bikes.json
python manage.py loaddata reservations.json