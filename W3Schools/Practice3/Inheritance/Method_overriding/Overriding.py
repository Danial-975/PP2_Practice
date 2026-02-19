class Animal:
    def speak(self):
        return "Неизвестный звук"

class Dog(Animal):
    def speak(self):
        return "Гав!"

class Cat(Animal):
    def speak(self):
        return "Мяу!"

animal = Animal()
dog = Dog()
cat = Cat()

print(dog.speak())  
print(cat.speak())