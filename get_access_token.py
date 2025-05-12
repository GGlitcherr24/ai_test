import requests
import urllib3

urllib3.disable_warnings()

def get_access_token():

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
      'scope': 'GIGACHAT_API_PERS'
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json',
      'RqUID': 'dc540414-f6e6-4971-8d20-c1a136e90bc9',
      'Authorization': 'Basic ...'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    access_token = response.json()
    return access_token['access_token']

if __name__ == "__main__":
    print(get_access_token())
