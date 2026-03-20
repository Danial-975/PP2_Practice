f = open("demofile.txt", "r")

print(f.read())
f.close()

f = open("demofile.txt", "r")

print(f.readline())
print(f.readline())
f.close()

with open("demofile.txt") as f:
  for x in f:
    print(x.strip())

with open('demofile.txt', 'r', encoding='utf-8') as f:
    print(f.readlines()[:3])