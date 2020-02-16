#!/bin/bash

if [ "$TRAVIS_PYTHON_VERSION" == "2.7" ]; then
  echo "Python 2 detected, installing dependencies with pip"
  pip install -r requirements-python2.txt
else
  echo "Installing dependencies with pipenv"
  pip install pipenv --upgrade
  pipenv install --deploy --dev
fi
