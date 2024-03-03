#!/bin/bash

# Activate the virtual environment
source ./venv/bin/activate

# Run the DCA bot
python3 ./src/DcaBot.py config_binance12.json
