class Father:
  def skills(self):
    print("Gardening and Programming")

class Mother:
  def skills(self):
    print("Cooking and Art")

class Child(Father, Mother):
  pass

c = Child()
c.skills()
