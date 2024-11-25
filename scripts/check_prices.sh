#!/usr/bin/env bash
## Configure bash as default shell (cron uses /bin/sh)
SHELL=/bin/bash
echo "-------------------------"
date
echo "[chech_prices.sh] start"
EXECUTION_PATH=$(pwd) # Once finished returns to path


## Get path of current file (chech_prices.sh) to get path of the repo and the rest of scripts
SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
export SCRIPT_PATH=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )

# Generate log path in case its not there
mkdir -p $SCRIPT_PATH/../log

## Activate python venv with deps
echo "[chech_prices.sh] Activate venv"
cd $SCRIPT_PATH/../ && source ./venv/bin/activate

## Run checkin with input options
echo "[chech_prices.sh] Run script"
cd $SCRIPT_PATH/../ && ./src/update_prices.py "$@"

cd $EXECUTION_PATH
echo "[chech_prices.sh] end"
date
echo "-------------------------"
