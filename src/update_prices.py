#!/usr/bin/env python3
# encoding: utf-8

import os
import yaml
import requests
import tabulate
from bs4 import BeautifulSoup
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from price_extractor import extract_price_number, extract_price_parts, json_request_extract_price
# Rutas de los archivos YAML
CONFIG_PATH = "./config/track_configuration.yaml"
PLOTS_DIR = "./plots/"
PRICES_DIR = "./data"

# Leer configuración desde YAML
def load_yaml(file_path, type=dict()):
    try:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file) or type
    except FileNotFoundError:
        print(f"[ERROR] [load_yaml] Could not find {file_path}")
        data = type
    return data

def update_yaml_list(file_path, new_data):
    data = load_yaml(file_path, [])
    data.append(new_data)

    with open(file_path, "w+") as file:
        yaml.dump(data, file, default_flow_style=False)
    
    return data

def fetch_price(site_config):
    try:
        session = requests.Session()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = session.get(site_config["url"], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if 'json_request' in site_config:
            price = json_request_extract_price(web_element=soup, config=site_config)
        else:
            if 'integer_class' in site_config:
                price = extract_price_parts(web_element=soup, config=site_config)
            else:
                price = extract_price_number(web_element=soup, config=site_config)
        
        return price
    except Exception as e:
        print(f"[ERROR] [fetch_price] Error getting price for {site_config['name']}: {e}")
        return None

# Notificar con notify.sh
def notify(topic, site_name, price):
    if topic is None:
        return 
    
    requests.post("https://ntfy.sh/"+str(topic),
            data=str(f"Tracker from {site_name} is below threshold, price is: {price}").encode(encoding='utf-8'),
            headers={
            "Title": "Price tracker"
        })
    


def update_prices():
    config = load_yaml(CONFIG_PATH)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nfty_topic = config['ntfy_topic']
    
    os.makedirs(PRICES_DIR, exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)

    for product in config['products']:
        table_format = [['Site', 'Price Web', 'Price Unit']]

        fig, ax = plt.subplots(figsize=(10, 6))

        for site_config in product["sites"]:
            threshold = product["threshold"]
            product_name = product['name']
            site_name = site_config["name"]
            price = fetch_price(site_config)
            complete_name = f"{product_name.replace(' ', '_')}_{site_name.replace(' ', '_')}"

            if price is None:
                print(f"Failed to fetch price for {product_name} in {site_name}")
                table_format.append([site_name,"Error"])
                continue
            
            # print(f"Fetched price for {product_name} in {site_name}: {price} €")
            price_unit = price
            if 'price_div' in site_config:
                price_unit = price/site_config['price_div']

            table_format.append([site_name,f"{price:.2f} €",f"{price_unit:.2f} €"])

            prices_yaml = os.path.join(PRICES_DIR,f"{complete_name}.yaml")
            prices_data = update_yaml_list(prices_yaml,{current_time: price})

            # Notificar si está por debajo del umbral
            if price <= threshold:
                notify(nfty_topic, product_name, price)

            # Generar gráfico del histórico de precios
            timestamps_str = [list(timestamp.keys())[0] for timestamp in prices_data]
            timestamps = [datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S') for date_str in timestamps_str]
            price_values = [list(price.values())[0] for price in prices_data]
            
            sns.lineplot(x=timestamps, y=price_values, label=site_name)
        plt.title(f"Price History for {product_name}")
        plt.xlabel("Time")
        plt.ylabel("Price")
        
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, f"{product_name}.png"))
        plt.clf()

        print(f"\n\nPrices for {product_name} (price threshold: {threshold} €)")
        print(tabulate.tabulate(table_format, headers="firstrow", tablefmt="fancy_grid"))
if __name__ == "__main__":
    update_prices()
