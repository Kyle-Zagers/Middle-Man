import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

api_integration_code = os.getenv('CODE')
username = os.getenv('USER')
secret = os.getenv('SECRET')

# The base URL for the Autotask API
base_url = 'https://webservices22.autotask.net/ATServicesRest'

headers = {
    'accept': 'application/json',
    'ApiIntegrationCode': api_integration_code,
    'UserName': username,
    'Secret': secret
}
    
def serialActive(serial):
    body = {
        # 'MaxRecords' : 10,
        'IncludeFields': ["isactive"],
        'Filter': [
            {
                'op': 'eq',
                'field': 'serialNumber',
                'value': serial
            }
        ]
    }

    # The endpoint for querying configuration items
    endpoint = '/V1.0/ConfigurationItems/query'

    url = f"{base_url}{endpoint}"

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, secret), json=body)

    if response.status_code == 200:
        data = response.json()
    else:
        return response

    result = False

    for var in data["items"]:
        if var['isActive'] == True:
            result = True
            break

    return result

def createAsset(company, name, serial, product, expiration):
    company = getClient(company)
    product = getProduct(product)

    if not isinstance(company, int) or company == -1:
        return f"Company does not exist. Details: {company}."
    
    if not isinstance(product, int) or product == -1:
        return f"Product does not exist. Details: {product}."

    body = {
        "companyID": company,
        "isActive": True,
        "referenceTitle": name,
        "serialNumber": serial,
        "productID": product,
        "installDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "warrantyExpirationDate": expiration
    }

    endpoint = '/V1.0/ConfigurationItems'

    url = f"{base_url}{endpoint}"

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, secret), json=body)

    if response.status_code == 200:
        return f"Success. {serial}"
    
    return response.json()

def getClient(name):
    if not name:
        return -1
    
    body = {
        # 'IncludeFields': [],
        'Filter': [
            {
                'op': 'eq',
                'field': 'companyName',
                'value': name
            }
        ]
    }

    endpoint = '/V1.0/Companies/query'

    url = f"{base_url}{endpoint}"

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, secret), json=body)

    if response.status_code == 200:
        data = response.json()
    else:
        return response
    
    if len(data['items']) == 1:
        return data['items'][0]['id']
        
    return -1
    
def getProduct(product):
    if not product:
        return -1

    body = {
        "Filter": [
            {
                "op": "eq",
                "field": "manufacturerProductName",
                "value": product
            }
        ]
    }

    endpoint = '/V1.0/Products/query'

    url = f"{base_url}{endpoint}"

    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, secret), json=body)

    if response.status_code == 200:
        data = response.json()
    else:
        return response
    
    if len(data['items']) == 1:
        return data['items'][0]['id']
    else:
        print(data['items'])
    
    return -1