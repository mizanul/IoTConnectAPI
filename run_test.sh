#!/bin/bash

cd api
export PYTHONPATH=.
export SECRET_KEY=my-secret-key
pytest -s ../test/app_test.py