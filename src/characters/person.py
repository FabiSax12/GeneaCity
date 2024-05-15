class Person():
    def __init__(self, person_info: dict):
        self.__id = person_info["id"]
        self.__name = person_info["name"]
        self.__gender = person_info["gender"]
        self.__age = person_info["age"]
        self.__marital_status = person_info["marital_status"]
        self.__alive = person_info["alive"]
        self.__father = person_info["father"]
        self.__mother = person_info["mother"]
        self.__house = person_info["house"]

    def __str__(self):
        return f"{self.__name} is {self.__age} years old."
    
    def birthday(self):
        self.__age += 1

    # Properties

    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def gender(self):
        return self.__gender
    
    @property
    def age(self):
        return self.__age
    
    @property
    def marital_status(self):
        return self.__marital_status
    
    @property
    def alive(self):
        return self.__alive
    
    @property
    def father(self):
        return self.__father
    
    @property
    def mother(self):
        return self.__mother
    
    @property
    def house(self):
        return self.__house
    
    @house.setter
    def house(self, new_house):
        self.__house = new_house
