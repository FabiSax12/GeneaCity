from typing import Literal, TypedDict

class Resident(TypedDict):
    id: int
    name: str
    gender: Literal["Male", "Female"]
    marital_status: Literal["Single", "Married"]
    father: int
    mother: int