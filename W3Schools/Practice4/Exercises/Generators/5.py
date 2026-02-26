def numbers(n):
  for i in range(n,0,-1):
    yield i

n = int(input())
gen = numbers(n)
for _ in range(n,0,-1):
  print(next(gen))