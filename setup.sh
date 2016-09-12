#!/bin/bash

apt-get update
apt-get install libpq-dev python-dev --yes
apt-get install python-pip --yes

pip install virtualenv virtualenvwrapper
pip install --upgrade pip

cp ~/.bashrc ~/.bashrc-org # backup bashrc
# Be careful with this command
printf '\n%s\n%s\n%s' '# virtualenv' 'export WORKON_HOME=~/virtualenvs' \
'source /usr/local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc
mkdir -p $WORKON_HOME


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
    test
    create database plentific;
    \q

}   # end of system_info