from abc import ABC, abstractmethod

class Shape(ABC):
  @abstractmethod
  def area(self):
    pass

class Rectangle(Shape):
  def __init__(self, a, b):
    self.a = a
    self.b = b
  def area(self):
    return self.a * self.b

h = Rectangle(4,3)
print(isinstance(h, Shape))
print(h.area())
