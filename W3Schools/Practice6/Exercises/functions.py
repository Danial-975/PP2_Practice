from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# 1.
squared = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Map: {squared}, Filter: {evens}")

# 2.
total_sum = reduce(lambda x, y: x + y, numbers)
print(f"Sum by reduce: {total_sum}")

# 3. 
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("Iteration in zip:")
for name, score in zip(names, scores):
    print(f"{name}: {score} points")

print("Iteration by enumerate:")
for index, name in enumerate(names, start=1):
    print(f"{index}. {name}")

# 4.
val = "100"
if isinstance(val, str):
    num = int(val) 
    print(f"Convert from {type(val)} to {type(num)}")