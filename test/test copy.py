import requests
from requests.auth import HTTPBasicAuth
import json

# Replace these variables with your actual data
api_integration_code = 'BGOMLNT67XY2BP2P4EIIU4DBK6K'
username = 'eaxvwrkfllohdan@virtechsystemsSB060324.com'
secret = '9p@Z#0LxR$g3*2AqyN~46#mGs'

# The base URL for the Autotask API
base_url = 'https://webservices22.autotask.net/ATServicesRest'

# The endpoint for querying configuration items
endpoint = '/V1.0/ConfigurationItems/query'

# Set up headers for the request
headers = {
    'accept': 'application/json',
    'ApiIntegrationCode': api_integration_code,
    'UserName': username,
    'Secret': secret
}

body = {
    'MaxRecords' : 500,
    'Filter': [
        {
            'op': 'gt',
            'field': 'id',
            'value': 0
        }
    ]
}

url = f"{base_url}{endpoint}"

data = {}

response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, secret), json=body)

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the JSON response
#     data = response.json()
#     attributes = list(map(lambda device: device['referenceTitle'], data['items']))
#     print('Query successful. Response data:')
#     # print(data)
#     print(attributes)
# else:
#     print(f'Failed to make the query. Status code: {response.status_code}')

while response.status_code == 200:

    items = response.json()['items']

    if not items:
        break

    if data:
        data['items'] += items
    else:
        data = response.json()

    body['Filter'][0]['value'] = data["items"][len(data["items"])-1]['id']
    response = requests.post(url, headers=headers, auth=HTTPBasicAuth(username, secret), json=body)

attributes = list(map(lambda device: device['serialNumber'], data['items']))
print(attributes)
print(len(attributes))