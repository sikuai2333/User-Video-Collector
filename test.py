# import requests

# url = "https://api.bbmang.me/users/phones/"

# headers = {
#    'User-Agent': 'Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)'
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

for i in range(111111,999999):
    phone1 = "13696"+str(i)
    with open ("phone.txt","a")as f:
        f.write(phone1+"\n")