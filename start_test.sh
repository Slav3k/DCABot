#!/bin/bash

#call ./InstallDeps.sh
./InstallDeps.sh

# Activate the virtual environment
source ./venv/bin/activate

# Run the DCA bot
python3 ./src/DcaBot.py config_template.json
