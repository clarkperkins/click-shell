#!/bin/bash

set -e

mkdir -p reports

# Code linting
echo "Running pycodestyle..."
pycodestyle click_shell

echo "Running pylint..."
pylint click_shell --reports=n --exit-zero --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt

# Type checking
if [ "$TRAVIS_PYTHON_VERSION" != "2.7" ]; then
  echo "Running mypy..."
  mypy click_shell
fi

# Unit tests
pytest -vv --cov=click_shell --cov-report=xml

if [ "$TRAVIS_PYTHON_VERSION" == "3.5" ] && [ "$TRAVIS_TAG" == "" ]; then
  echo "Python 3.5 detected, running sonar-scanner"
  sonar-scanner -Dsonar.projectVersion=$(python setup.py --version)
fi
