#!/bin/bash

nohup anvil -a 1 --balance 10000000000 --mnemonic-random &

exec python3 app.py