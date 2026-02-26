import json

person = {
    "name": "Jack Robertson",
    "age": 30,
    "city": "New York",
    "is_student": False,
    "hobbies": ["football", "books", "traveling"]
}

json_string = json.dumps(person, indent=2)
print("JSON строка:")
print(json_string)