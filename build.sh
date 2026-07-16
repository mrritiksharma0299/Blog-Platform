#!/usr/bin/env bash

set -o errexit

rm -rf staticfiles

python manage.py collectstatic --noinput

python manage.py migrate

python repair_profile_community.py