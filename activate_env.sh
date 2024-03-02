#!/bin/bash

if [ ! -e env/bin/activate ]; then
  python3.10 -m venv env/ || return
  source env/bin/activate
  echo "Activated virtual env"
  python -m pip install --upgrade pip wheel setuptools
  python -m pip install -e .[all]
  git config commit.template .github/.gitmessage
  cp .github/prepare-commit-msg .git/hooks/prepare-commit-msg
  chmod +x .git/hooks/prepare-commit-msg
  pre-commit install
else
  source env/bin/activate
  python -m pip install -e .[all]
  echo "Activated virtual env"
fi
