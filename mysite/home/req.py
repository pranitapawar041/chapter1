import requests
r = requests.get('https://images.app.goo.gl/gWEx1jLczSxwdqcm7')
print(r.text)
print(r.status_code)

url = 'https://images.app.goo.gl/gWEx1jLczSxwdqcm7'
data = {
    "sam" : 4,
    "rahul": 5
}
r2 = requests.post(url=url, data=data)