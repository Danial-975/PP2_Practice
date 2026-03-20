from functools import reduce

def even(x):
    return x % 2 == 0

a = "Hello"
b = [1, 3, 4, 6, 2, 5]
c = ['a', 'b', 'c', 'd', 'e', 'f']
d = 2
e = complex(d)
print(len(a))
print(sum(b))
print(min(b))
print(max(b))
print(list(zip(b,c)))
print(sorted(b))
print(list(filter(even, b)))

sum_all = reduce(lambda a, x: a + x, b) 
print(sum_all)

fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")