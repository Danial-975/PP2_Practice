import re

text1 = "Hello, World!"
text2 = "World, Hello!"

# Match "Hello" at the beginning of the string
match1 = re.match(r"Hello", text1) 
match2 = re.match(r"Hello", text2)

if match1:
    print(f"Match found in text1: {match1.group()}") # Output: Match found in text1: Hello
else:
    print("No match in text1")

if match2:
    print(f"Match found in text2: {match2.group()}")
else:
    print("No match in text2") # Output: No match in text2
