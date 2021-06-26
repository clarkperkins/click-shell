#!/bin/bash

set -e

mkdir -p reports

# Code linting
echo "Running pycodestyle..."
pycodestyle click_shell

echo "Running pylint..."
pylint click_shell --reports=n --exit-zero --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt

# Type checking
# mypy doesn't work at all on python2, and there's some other issues with pipenv packages on python3 < 3.8
if [ "$TRAVIS_PYTHON_VERSION" == "3.9" ]; then
  echo "Running mypy..."
  mypy click_shell
fi

# Unit tests
pytest -vv --cov=click_shell --cov-report=xml

if [ "$TRAVIS_PYTHON_VERSION" == "3.9" ] && [ "$CLICK_VERSION" == "8.0" ] && [ "$TRAVIS_TAG" == "" ]; then
  echo "Python 3.9 detected, running sonar-scanner"
  sonar-scanner -Dsonar.projectVersion=$(python setup.py --version)
fi
