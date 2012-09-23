#!/bin/bash
command -v mkvirtualenv >/dev/null && virtual_env_installed=true | virtual_env_installed=false

if ! $virtual_env_installed ; then
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
fi

export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUALENV_BASE=$WORKON_HOME
export PIP_RESPECT_VIRTUALENV=true

mkvirtualenv --no-site-packages -p python welog
workon welog
pip install -r requirements.txt
