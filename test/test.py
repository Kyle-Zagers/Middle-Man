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
endpoint = '/V1.0/ConfigurationItems/'

# Set up headers for the request
headers = {
    'accept': 'application/json',
    'ApiIntegrationCode': api_integration_code,
    'UserName': username,
    'Secret': secret
}

device = 1

url = f"{base_url}{endpoint}{device}"

response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, secret))

while response.status_code == 200:
    # Construct the full URL
    url = f"{base_url}{endpoint}{device}"

    # Make the GET request with basic authentication
    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(username, secret))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print('Query successful. Response data:')
        # print(data)
        if data['item']:
            print(data['item']['referenceTitle'])
    else:
        print(f'Failed to make the query. Status code: {response.status_code}')
    device+=1
