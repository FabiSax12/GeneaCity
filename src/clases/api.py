import requests
import threading
from typing import Tuple, Callable, List, Dict
from interfaces.api_interface import ApiInterface

class Api(ApiInterface):
    def __init__(self, url: str) -> None:
        self.__url = url
        
        self.__houses_result = None
        self.__inhabitants_result = None

        self.__houses_event = threading.Event()
        self.__inhabitants_event = threading.Event()

    def get_houses(self, pos: Tuple[float, float], callback: Callable) -> List[Dict]:
        """Get the houses in a specific position.

        Args:
            pos (tuple[float, float]): position to get the houses

        Returns:
            list[dict]: list of houses in the position area
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

    def get_house_residents(self, house_id: int) -> List[Dict]:
        """Get the residents of a house.

        Args:
            house_id (int): house id to get the residents

        Returns:
            list[dict]: list of residents in the house
        """
        response = requests.get(f"{self.__url}/getHousesResidents/?houseId={house_id}").json()
        if response["status"] == 1:
            return response["residents"]
        else:
            return []

    def get_available_inhabitants(self, pos: Tuple[int, int], callback: Callable) -> List[Dict]:
        """Get the available inhabitants in a specific position.

        Args:
            pos (tuple[int, int]): position to get the available inhabitants

        Returns:
            list[dict]: list of available inhabitants in the position area
        """
        thread = threading.Thread(target=self.__get_available_inhabitants, args=(pos, callback), daemon=True, name="getAvailableInhabitants")
        thread.start()
        self.__inhabitants_event.wait()
        return self.__inhabitants_result

    def __get_available_inhabitants(self, pos: Tuple[float, float], callback: Callable):
        pos = (int(pos[0]), int(pos[1]))
        try:
            response = requests.get(f"{self.__url}/getAvailableInhabitants/?x={pos[0]}&y={pos[1]}").json()
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
        # response = requests.get(f"{self.__url}/selectAvailableInhabitant/?id={inhabitant_id}").json()
        # return response["status"] == 1
        print("Selected inhabitant: ", inhabitant_id)
        return {
            "status": True
        }  # Simulate successful selection

    def get_inhabitant_information(self, inhabitant_id: int) -> Dict:
        """Get the information of an inhabitant.

        Args:
            inhabitant_id (int): inhabitant id to get the information

        Returns:
            dict: inhabitant information
        """
        response = requests.get(f"{self.__url}/getInhabitantInformation/?id={inhabitant_id}").json()
        return response
    
    # Properties

    @property
    def url(self) -> str:
        return self.__url