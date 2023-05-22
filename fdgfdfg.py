import requests
import json

def check_trc20_balance(address, contract_address):
    tron_api_url = "https://api.trongrid.io"

    headers = {
        'Content-Type': 'application/json',
    }

    function_selector = "70a08231"  # balanceOf function hash
    data_hex = function_selector + address[2:].lower().rjust(64, '0')

    data = {
        "contract_address": contract_address,
        "function_selector": "70a08231",
        "parameter": data_hex,
        "visible": True
    }

    response = requests.post(
        f"{tron_api_url}/wallet/triggersmartcontract",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code != 200:
        print("Failed to get balance.")
        return

    result = response.json()
    if not result["result"]["result"]:
        print("Invalid address or contract address.")
        return

    balance_hex = result["constant_result"][0]
    balance = int(balance_hex, 16) / 10**6

    print(f"Balance for address {address} is: {balance} USDT")


if __name__ == "__main__":
    usdt_contract_address = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT TRC20 contract address
    your_tron_address = "your_tron_address_here"

    check_trc20_balance(your_tron_address, usdt_contract_address)