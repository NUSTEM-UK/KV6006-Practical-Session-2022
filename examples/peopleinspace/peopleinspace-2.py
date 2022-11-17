# examples/peopleinspace/peopleinspace-2.py
import requests

r = requests.get('http://api.open-notify.org/astros.json')
data = r.json()

print("Total people in space: ", data['number'])
print("-----")

for person in data['people']:
    print(person['name'])
