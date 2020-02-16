#!/bin/bash

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
pytest --cov=click_shell --cov-report=xml

sonar-scanner
