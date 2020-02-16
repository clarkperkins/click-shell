#!/bin/bash

# Code linting
pycodestyle click_shell
pylint click_shell --reports=n --exit-zero --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > reports/pylint.txt

# Type checking
if [ "$TRAVIS_PYTHON_VERSION" != "2.7" ]; then
  mypy click_shell
fi

mkdir -p reports

# Unit tests
pytest --cov=click_shell --cov-report=xml

sonar-scanner
