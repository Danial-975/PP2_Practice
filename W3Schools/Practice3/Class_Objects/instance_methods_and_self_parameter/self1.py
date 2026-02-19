class Person:
  def __init__(self, name):
    self.name = name

  def printname(self):
    print(self.name)

p1 = Person("Ben")
p2 = Person("Linus")

p1.printname()
p2.printname()