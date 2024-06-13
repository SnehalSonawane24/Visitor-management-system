#!/bin/env bash

# echo Downgrade Python3.12 to 3.10.12 using 
# yum install python3.10 
# alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
# alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 2

# echo "Creating virtualenv"
# pip3 install virtualenv
# virtualenv env

# echo "Activating virtualenv"
# source env/bin/activate

echo "Building project packages..."
pip3 install -r requirements.txt

echo "Migrating Database..."
python3 manage.py migrate --noinput

echo "Collecting static files..."
python3 manage.py collectstatic --noinput
