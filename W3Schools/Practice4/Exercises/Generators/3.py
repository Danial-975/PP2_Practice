def divisble_3_4(n):
  for i in range(1,n):
    if i%3==0 and i%4==0:
        yield i

n = int(input())
gen = divisble_3_4(n)
result = list(gen)
print(*result, sep=", ")