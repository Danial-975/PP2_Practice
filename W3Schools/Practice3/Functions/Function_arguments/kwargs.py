def my_function(name, **details):
  print("Username:", name)
  print("Additional details:")
  for key, value in details.items():
    print("  ", key + ":", value)

my_function("userbaev23", age = 23, city = "Almaty", hobby = "playing the guitar")
