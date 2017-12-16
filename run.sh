#!/bin/bash

# start with large response-timeout allowing for large texts to be parsed
gunicorn --bind 0.0.0.0:9000 --timeout 120 server:app
