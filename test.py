import requests

url = "http://127.0.0.1:5000/api/454824exec"
headers = {
    "User-Agent":"sqlmap"
}
for i in range(10000):
    res = requests.get(url,headers=headers)
    print(res.text)
