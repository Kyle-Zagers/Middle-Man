from tools import *
from selenium import *
from splinter import Browser
from selenium.webdriver.edge.options import Options
import time
import pandas as pd
from selectolax.parser import HTMLParser
import re
import json
from fake_useragent import UserAgent
import random

def getModel(serial):
    # browser = Browser('edge', headless=True)
    # browser.visit('https://pcsupport.lenovo.com/us/en/warranty-lookup#/')

    # browser.find_by_xpath('//*[@id="app-standalone-warrantylookup"]/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div[1]/input').fill(serial)
    # browser.find_by_xpath('//*[@id="app-standalone-warrantylookup"]/div[1]/div[2]/div/div/div[1]/button').click()

    # time.sleep(0.2)

    # model = browser.find_by_xpath('//*[@id="app-psp-warranty"]/div[2]/div/div/div[1]/div/div[1]/div[1]/div/div/div[2]/ul/li[1]/span').value
    # name = browser.find_by_xpath('/html/body/div[2]/section[2]/div[1]/div[2]/div[2]/div[1]/h4').value
    # expiration = browser.find_by_xpath('//*[@id="app-psp-warranty"]/div[2]/div/div/div[1]/div/div[1]/div[2]/div[2]/div/div/div/div/div[2]/div/div[5]/span[2]').value
    # browser.quit()
    
    # type = ""

    # for i in reversed(name):
    #     if i == ' ':
    #         break
    #     type = i + type

    # date = datetime.strptime(expiration, "%Y-%m-%d")

    # return [f"{type}{model}", f"{date.strftime('%Y-%m-%d')}T{'00:00:00.000'}Z"]

    # file = open("temp.txt", 'w', encoding="utf-8")

    free_us_proxies = [
        {'http': 'http://104.238.111.107:3230', 'https': 'https://104.238.111.107:3230'},
        {'http': 'http://104.225.220.233:80', 'https': 'https://104.225.220.233:80'},
        {'http': 'http://137.184.6.203:8081', 'https': 'https://137.184.6.203:8081'},
        {'http': 'http://12.186.205.123:80', 'https': 'https://12.186.205.123:80'},
        {'http': 'http://100.1.53.24:5678', 'https': 'https://100.1.53.24:5678'},
        {'http': 'http://130.245.128.193:8080', 'https': 'https://130.245.128.193:8080'},
        {'http': 'http://128.199.5.121:21044', 'https': 'https://128.199.5.121:21044'},
        {'http': 'http://154.16.146.45:80', 'https': 'https://154.16.146.45:80'},
        {'http': 'http://12.176.231.147:80', 'https': 'https://12.176.231.147:80'},
        {'http': 'http://142.54.232.6:4145', 'https': 'https://142.54.232.6:4145'},
        {'http': 'http://148.72.140.24:30127', 'https': 'https://148.72.140.24:30127'},
        {'http': 'http://130.58.218.30:80', 'https': 'https://130.58.218.30:80'},
        {'http': 'http://103.170.155.15:3128', 'https': 'https://103.170.155.15:3128'},
        {'http': 'http://104.200.135.46:4145', 'https': 'https://104.200.135.46:4145'},
        {'http': 'http://107.180.90.88:4756', 'https': 'https://107.180.90.88:4756'},
        # ... additional proxies would be listed here
    ]


    ua = UserAgent()

    response = requests.get(f'https://pcsupport.lenovo.com/us/en/api/v4/mse/getproducts?productId={serial}', headers={'User-Agent': ua.random})
    info = response.json()[0]
    response = requests.get(f'https://pcsupport.lenovo.com/us/en/products/{info['Id']}/warranty', headers={'User-Agent': ua.random})

    variable_pattern = re.compile(r'var\s+ds_warranties\s+=\s+(.*?);') # regex
    match = variable_pattern.search(response.text)

    if match:
        info = match.group(1).split('||')[1].strip()
        info = json.loads(info)
    else:
        return -1
    
    date = datetime.strptime(info['BaseWarranties'][0]['End'], "%Y-%m-%d")
    return [f"{info['MachineType']}{info['Mode']}", f"{date.strftime('%Y-%m-%d')}T{'00:00:00.000'}Z"]



from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to process each device
def process_device(row):
    if not row['Serial Number']:
        return -1

    if serialActive(row['Serial Number']):
        return f"Active asset with serial already exists. Details: {row['Serial Number']}."

    try:
        model = getModel(row['Serial Number'])
    except:
        model = getModel(row['Serial Number'])

    return createAsset(row['Client'], row['Reference Name'], row['Serial Number'], model[0], model[1])

if __name__ == "__main__":
    # Read the CSV data from a file
    file_path = r'./Asset Search Results.csv'
    data = pd.read_csv(file_path)

    # Extract the necessary columns
    deviceinfo = data[['Client', 'Reference Name', 'Serial Number']]

    # Use ThreadPoolExecutor to parallelize the processing
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(process_device, row) for index, row in deviceinfo.iterrows()]
        results = []
        for future in as_completed(futures):
            result = future.result()
            print(result)
            results.append(result)

    print(results)








# model = getModel("PF4KPTAC")
# print(createAsset("Bone Construction, LLC", "Kyle Test Device", "282489", model[0], model[1]))
