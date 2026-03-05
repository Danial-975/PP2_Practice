import re

txt = "Hello , World!"

x = re.findall("^He..o.*World!$", txt)
if x:
  print("Yes, the string starts with Hello and ends with World!")
else:
  print("No match")