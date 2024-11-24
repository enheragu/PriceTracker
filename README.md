# PriceTracker

Script to track prices on websites and send notification based on a given threshold.

Check `config/track_configuration.yaml` to check an example of the different available options.
If a `ntfy_topic` is provided, notifications will be sent to the provided topic when the threshold is exceeded. Check more about it in https://ntfy.sh/

The script to run is `src/update_prices.py`. A virtual environment is recommended to install the dependencies.
