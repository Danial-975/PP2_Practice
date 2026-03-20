with open("dfile.txt", "a") as f:
  f.write("Now the file has more content!")

with open("dfile.txt") as f:
  print(f.read())

with open("dfile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")

with open("dfile.txt") as f:
  print(f.read())