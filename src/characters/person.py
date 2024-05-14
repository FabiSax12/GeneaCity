class Person():
    def __init__(self, person_info: dict):
        self.id = person_info["id"]
        self.name = person_info["name"]
        self.age = person_info["age"]
        self.house = person_info["house"]
        self.is_married = False

    def __str__(self):
        return f"{self.name} is {self.age} years old."
    
    def birthday(self):
        self.age += 1

    def get_info(self):
        return {"id": self.id, "name": self.name, "age": self.age}