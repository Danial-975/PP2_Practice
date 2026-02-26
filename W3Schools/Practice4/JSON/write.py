import json

person = {
    "name": "Jack Robertson",
    "age": 30,
    "city": "New York",
    "is_student": False,
    "hobbies": ["football", "books", "traveling"]
}

with open('c:/Users/dania/PP2_Practice/W3Schools/Practice4/JSON/person.json', 'w') as file:
    json.dump(person, file, indent=2)

print("File person.json created!")