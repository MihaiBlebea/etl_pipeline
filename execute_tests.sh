#!/bin/bash

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="${PYTHONPATH}:${PWD}"
eval "./env/bin/python3 setup.py pytest"