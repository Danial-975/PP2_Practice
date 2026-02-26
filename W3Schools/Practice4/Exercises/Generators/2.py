def even(n):
  for i in range(n):
    if i%2==0:
        yield i

n = int(input())
gen = even(n)
result = list(gen)
print(*result, sep=", ")