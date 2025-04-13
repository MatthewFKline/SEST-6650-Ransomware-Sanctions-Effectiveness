import json
import time

import requests

BASE_URL = "https://blockchain.info/rawaddr/"

# content = results.content
# text = results.text
# data = results.json()

with open("data/ransomware_data.json", "r") as f:
    ransom_addresses = json.load(f)

ransom_addresses = [item["address"] for item in ransom_addresses]

with open("null_addresses.txt", "x") as f:
    for item in ransom_addresses:
        response = requests.get(BASE_URL + item)
        response.raise_for_status()
        data = response.json()
        if data["n_tx"] == 0:
            print(f"No transactions observed for {item}")
            f.write(f"No transactions observed for {item}\n")
        else:
            print(f"Observed > 0 transactions for {item}")
        time.sleep(10.5)
