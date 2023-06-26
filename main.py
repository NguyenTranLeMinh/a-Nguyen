import requests
import configparser
import json
import time

COUNTER = 0

# Create a configparser object
config = configparser.ConfigParser()
# Read the .ini file
config.read('keys.ini')
# Get the value of API_KEY
x_api_key = config.get('KEYS', 'X_API_KEY')

with open('nhanh.csv', 'r') as f:
    dict_products = dict()

    # headers
    a, b = f.readline().strip().split(',')

    for line in f:
        sku, n = line.strip().split(',')
        if sku is None or n is None:
            continue 
        dict_products[sku] = dict() # Ma san pham
        dict_products[sku][b] = n # Ton trong kho
        # dict_products[sku]['inventoryId'] = -1

# print(dict_products)
assert len(dict_products) != 0, "File .csv NULL"

get_url = config.get('URLS', 'GET_URL')
headers = {"x-api-key": x_api_key}

for page_id in range(1, 11):
    params = {"page": page_id}
    response = requests.get(get_url, params=params, headers=headers)

    if response.status_code == 200:
        # Request successful
        data = response.json()
        # Process the response data as needed
        # json_str = json.dumps(data)
        # print(json_str)
        for item in data['data']:
            for variant in item['variants']:
                if dict_products.get(variant['sku']) and dict_products[variant['sku']][b]:
                    # dict_products[variant['sku']]['inventoryId'] = variant['inventoryId']
                    id = variant['inventoryId']
                    put_url = f"https://developers-oaplus.line.biz/myshop/v1/inventory/{id}/adjust"
                    payload = {
                        "amount": int(dict_products[sku][b])
                    }
                    put_response = requests.put(put_url, headers=headers, json=payload)
                    # print(payload)
                    print(f"Status code {put_response.status_code}: sku={variant['sku']}, inventoryID={id}, amount={int(dict_products[sku][b])}")
                    
                    COUNTER += 1
                    if COUNTER == 50:
                        time.sleep(3)
                        COUNTER = 0
    else:
        # Request failed
        print(f"Request failed with status code {response.status_code}")

print("Done!")
