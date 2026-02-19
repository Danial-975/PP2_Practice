class Person:
  age = 19
  def __init__(self, name, age):
    self.name = name
    self.age = age

  def myfunc(self):
    print("Hello my name is " + self.name)

p1 = Person("Linus", 18)

del p1.age
del Person.age

print(p1.name)
print(p1.age)
