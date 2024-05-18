from type.house import House
from typing import Literal, TypedDict

class AvailableInhabitant(TypedDict):
    id: int
    name: str
    age: int
    gender: Literal["Male", "Female"]

class Inhabitant(AvailableInhabitant):
    marital_status: Literal["Single", "Married"]
    father: int
    mother: int
    house: House
    