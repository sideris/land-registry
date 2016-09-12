#!/bin/bash
echo "Positional Parameters"
echo '$1 = ' $1
echo '$2 = ' $2
echo '$3 = ' $3

#apt-get update
#apt-get install libpq-dev python-dev --yes
#
#pip install virtualenvwrapper
#
#export WORKON_HOME=$HOME/.virtualenvs
#export MSYS_HOME=/c/msys/1.0
#source /usr/local/bin/virtualenvwrapper

if [ "$1" = "setdb" ]; then
    setup_postgres()
else
  echo "Wrong parameter. To setup postgres try `setdb`"
fi

mkvirtualenv plentific
pip install -r requirements.txt

python manage.py migrate
python manage.py load_data --clear --large

function setup_postgres
{
    echo "<p>Setting up postgres</p>"
    apt-get install postgresql postgresql-contrib --yes
    service postgresql start
    sudo -u postgres psql postgres
    \password postgres
    test
    psql
    create database plentific;
    \q

}   # end of system_info