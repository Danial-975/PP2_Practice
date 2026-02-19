class Person:
  lastname = ""

  def __init__(self, name):
    self.name = name

p1 = Person("Liam")
p2 = Person("Andrew")

Person.lastname = "Robertson"

print(p1.lastname)
print(p2.lastname)
