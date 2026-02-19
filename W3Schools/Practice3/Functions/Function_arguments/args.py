def my_function(*numbers):
  total = 1
  for num in numbers:
    total *= num
  return total

print(my_function(4, 7, 11))
print(my_function(12, 4, 2, 3))
print(my_function(4))