class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
        print("Woof Woof")

class Duck(Animal):
    def speak(self):
        print("Quack Quack")

animal = Animal()
animal.speak()
dog = Dog()
dog.speak()
duck = Duck()
duck.speak()