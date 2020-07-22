#!/usr/bin/env sh

echo "WAITING 2 SEC FOR DB TO RUN..."
sleep 2
echo "LAUNCHING CRUD SERVER..."
#screen -dmS python3 run_crud_server.py  # for future tests
cd src
python3 -u run_crud_server.py
#echo "START TESTS"
