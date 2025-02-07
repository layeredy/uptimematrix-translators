#!/bin/bash

# NOTICE: You will need to setup the Python venv
# Before running this script for it to function

# Change the 'status' part in the source command
# To whatever you named your venv or this script
# Will not function.

source status/bin/activate
python3 uptimerobot.py
deactivate
