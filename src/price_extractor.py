
import requests

"""
    Function to use when price is into a single number
"""
def extract_price_number(web_element, config):
    try:
        price_element = web_element.find(config["tag"], class_=config["class"])

        if not price_element:
            raise ValueError(f"Could not find element wih tag={config['tag']} y class={config['class']}")

        price_text = price_element.get_text(strip=True)
        price_text = price_text.split("€")[0]
        price = float(price_text.replace(",", "."))
        
        return price

    except Exception as e:
        print(f"[ERROR] [extract_price_number]: {e}")
        return None


""" 
    Function to use when prices are spplited into whole/decimal parts
"""
def extract_price_parts(web_element, config):
    try:
        whole = web_element.find(config['tag'], class_=config['integer_class'])
        decimal = web_element.find(config['tag'], class_=config['decimal_class'])
        
        if not whole:
            raise ValueError(f"Could not find element wih tag={config['tag']} y class={config['integer_class']}")
        elif not decimal:
            raise ValueError(f"Could not find element wih tag={config['tag']} y class={config['decimal_class']}")

        whole_text = whole.get_text(strip=True).replace(".", "").replace(",","")
        decimal_text = decimal.get_text(strip=True)

        price = float(f"{whole_text}.{decimal_text}")

        return price
    except Exception as e:
        print(f"[ERROR] [extract_price_parts]: {e}")
        return None
    
    
def json_request_extract_price(web_element, config):

    # with open(f'{config["name"]}_log.html', 'w+') as file:
    #     file.write(str(web_element))

    url = config['json_request']
    url = url.replace("&amp;", "&")
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Error in request. Response.status_code is: {response.status_code}")

    # with open(f'{config["name"]}_response.json', 'w+') as file:
    #     file.write(str(response.text))

    price_value = response.json()
    for key in config['json_path']:
        price_value = price_value.get(key, {})

    price = float(price_value)
        
    return price