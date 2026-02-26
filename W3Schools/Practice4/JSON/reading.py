import json


with open('c:/Users/dania/PP2_Practice/W3Schools/Practice4/JSON/person.json', 'r') as file:
    data = json.load(file)

print(data)
print(f"Name: {data['name']}")
print(f"Age: {data['age']}")
print(f"City: {data['city']}")