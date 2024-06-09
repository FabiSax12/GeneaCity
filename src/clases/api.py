import requests
import threading
from typing import Literal, Tuple, Callable, List
from interfaces.api_interface import ApiInterface
from type.house import House
from type.inhabitant import AvailableInhabitant, Inhabitant
from type.resident import Resident

class Api(ApiInterface):
    def __init__(self, url: str) -> None:
        self.__url = url
        
        self.__houses_result: List[House] = None
        self.__inhabitants_result: List[Inhabitant] = None

        self.__houses_event = threading.Event()
        self.__inhabitants_event = threading.Event()

    def get_houses(self, pos: Tuple[float, float], callback: Callable) -> List[House]:
        """Get the houses in a specific position.

        Args:
            pos (tuple[float, float]): position to get the houses

        Returns:
            list[House]: list of houses in the position area
        """
        pos = (int(pos[0]), int(pos[1]))
        thread = threading.Thread(target=self.__get_houses, args=(pos, callback), daemon=True, name="getHouses")
        thread.start()
        self.__houses_event.wait()
        return self.__houses_result

    def __get_houses(self, pos: Tuple[float, float], callback: Callable):
        endpoint = f"{self.__url}/getHouses/?x={pos[0]}&y={pos[1]}"
        try:
            response = requests.get(endpoint).json()
            if response["status"] == 1:
                self.__houses_result = response["houses"]
            else:
                self.__houses_result = []
        except Exception as e:
            self.__houses_result = []
        finally:
            self.__houses_event.set()
            callback(self.__houses_result)

    def get_house_residents(self, house_id: int) -> List[Resident]:
        """Get the residents of a house.

        Args:
            house_id (int): house id to get the residents

        Returns:
            list[Resident]: list of residents in the house
        """
        try:
            response = requests.get(f"{self.__url}/getHousesResidents/?houseId={house_id}", timeout=4).json()

            if not "residents" in response:
                return []

            for i, resident in enumerate(response["residents"]):
                resident_info = self.get_inhabitant_information(resident["id"])

                response["residents"][i]["id"] = int(resident["id"])
                response["residents"][i]["age"] = int(resident_info["age"])
                response["residents"][i]["father"] = int(resident["father"])
                response["residents"][i]["mother"] = int(resident["mother"])

            if response["status"] == 1:
                return response["residents"]
            else:
                return []
        except requests.Timeout:
            print("Timeout")
            return self.get_house_residents(house_id)

    def get_available_inhabitants(self, pos: Tuple[int, int], callback: Callable) -> List[AvailableInhabitant]:
        """Get the available inhabitants in a specific position.

        Args:
            pos (tuple[int, int]): position to get the available inhabitants

        Returns:
            list[AvailableInhabitant]: list of available inhabitants in the position area
        """
        thread = threading.Thread(target=self.__get_available_inhabitants, args=(pos, callback), daemon=True, name="getAvailableInhabitants")
        thread.start()
        self.__inhabitants_event.wait()
        return self.__inhabitants_result

    def __get_available_inhabitants(self, pos: Tuple[float, float], callback: Callable):
        pos = (int(pos[0]), int(pos[1]))
        try:
            response = requests.get(f"{self.__url}/getAvailableInhabitants/?x={pos[0]}&y={pos[1]}").json()
            for inhabitant in response["inhabitants"]:
                inhabitant["id"] = int(inhabitant["id"])
                inhabitant["age"] = int(inhabitant["age"])

            if response["status"] == 1:
                self.__inhabitants_result = response["inhabitants"]
            else:
                self.__inhabitants_result = []
        except Exception as e:
            self.__inhabitants_result = []
        finally:
            self.__inhabitants_event.set()
            callback(self.__inhabitants_result)

    def select_available_inhabitant(self, inhabitant_id: int) -> bool:
        """Select an available inhabitant to play with.

        Args:
            inhabitant_id (int): inhabitant id to select

        Returns:
            dict: selected inhabitant
        """
        response = requests.get(f"{self.__url}/selectAvailableInhabitant/?id={inhabitant_id}").json()
        return response["status"] == 1

    def get_inhabitant_information(self, inhabitant_id: int) -> Inhabitant:
        """Get the information of an inhabitant.

        Args:
            inhabitant_id (int): inhabitant id to get the information

        Returns:
            Inhabitant: inhabitant information
        """
        try:
            response = requests.get(f"{self.__url}/getInhabitantInformation/?id={inhabitant_id}").json()

            if response["status"] == 1:
                data = response["inhabitant"]
                data["id"] = int(data["id"])
                data["age"] = int(data["age"])
                data["mother"] = int(data["mother"]) if data["mother"] else None
                data["father"] = int(data["father"]) if data["father"] else None
                data["house"] = {
                    "id": int(data["house"]),
                    "x": 250,
                    "y": 250
                } if data["house"] else None
                data["position"] = {
                    "x": 250,
                    "y": 250
                } if data["alive"] else None
                if data["marital_status"] == "Single":
                    data["partner"] = None
                return data
            elif response["status"] == 0:
                raise ValueError(response["error"])
            
            return {}
        except Exception as e:
            raise ValueError("An error occurred while getting inhabitant information.")
        
    def marry_inhabitants(self, inhabitant1_id: int, inhabitant2_id: int, newHouseXPostition: int, newHouseYPostition: int) -> bool:
        """Marry two inhabitants.

        Args:
            inhabitant1_id (int): inhabitant 1 id
            inhabitant2_id (int): inhabitant 2 id

        Returns:
            bool: True if the inhabitants were married, False otherwise
        """
        response = requests.get(f"{self.__url}/createInhabitantUnion/?idInhabitant1={inhabitant1_id}&idInhabitant2={inhabitant2_id}&newHouseXPostition={newHouseXPostition}&newHouseYPostition={newHouseYPostition}").json()

        if response["status"] == 0 and response["error"]:
            raise ValueError(response["error"])

        return response["status"] == 1
    
    def create_children(self, name: str, parent_id: int, gender: Literal['Male'] | Literal['Female'], age: int = None) -> bool:
        """Create children for a married couple.

        Args:
            name (str): child name
            parent_id (int): parent id
            gender (str): gender of the child
            age (int): age of the child
        """
        if age is None:
            age = 0

        response = requests.get(f"{self.__url}/createChildren/?name={name}&idInhabitant={parent_id}&gender={gender}&age={age}").json()

        if response["status"] == 0 and response["error"]:
            raise ValueError(response["error"])

        return response

    # Properties

    @property
    def url(self) -> str:
        return self.__url