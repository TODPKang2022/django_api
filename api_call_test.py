import requests
import json


url = 'http://127.0.0.1:8080/book-search/'

headers={'Content-Type':'application/json; charset=utf-8'}
params = {
    'term':'data_test'
}

r = requests.get(url=url, headers=headers, params=params)
print(r)
response = r.json()
print(json.dumps(response, indent=2, ensure_ascii=False))