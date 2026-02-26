def square(n):
  for i in range(n+1):
    yield i**2

n = int(input())
gen = square(n)
for _ in range(n+1):
  print(next(gen))