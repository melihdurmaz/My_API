import requests

# API anahtarı
api_key = '*******************'
wallet_address=input("Wallet adresinizi giriniz: ")


# API URL'si
url = f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={wallet_address}&address=0x5bEFE2128AFB0762d4fEdc51fD1B613507FeF4a8&tag=latest&apikey={api_key}'

try:
    response = requests.get(url)
    token = 15

    if response.status_code == 200:
        response_json = response.json()
        token_balance =int(response_json.get('result'))
        print(token_balance > token)


    else:
        print(f"İstekte bir hata oluştu. HTTP kodu: {response.status_code}")

except Exception as e:
    print(f"Hata oluştu: {str(e)}")
