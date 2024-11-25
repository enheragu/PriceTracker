# PriceTracker

Script to track prices on websites and send notification based on a given threshold.

Check `config/track_configuration.yaml` to check an example of the different available options.
If a `ntfy_topic` is provided, notifications will be sent to the provided topic when the threshold is exceeded. Check more about it in https://ntfy.sh/

The script to run is `src/update_prices.py`. A virtual environment is recommended to install the dependencies.


## Installation

It is recommended to install the setup into a virtual environment. Create one and activate it with the following command (or just ignore these an execute without venv):

```sh
    python3 -m venv venv
    source venv/bin/activate
```
>Note: THe second `venv` is just the path in which the virtual env will be located. Change it at will.

The environment can be deactivated as follows:
```sh
    deactivate
```

Clone the repository in a given location and install its requirementes with the following command, executed from the root folder of the repository. You can check the requirements file to check the libraries that will be installed into your system.

```sh
    pip3 install -r requirements
```

## Execution

It is better to configure the script in crontab. To edit the crontab file use in a terminal the command `crontab -e`. Open the file with the desired editor and add the command to execute. In the following example the command is executed twice a day (at 11 and at 23h). The output ot the command is stored in a log file just in case something needs to be checked later.

```sh
    0 11,23 * * * /home/pi/PriceTracker/scripts/check:prices.sh >> /home/pi/PriceTracker/logs/log_crontab_price_tracker.log 2>&1
```