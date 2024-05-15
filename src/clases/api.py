import threading
import requests

class Api:
    def __init__(self, url) -> None:
        self.url = url
        
        self.houses_result = None
        self.players_result = None
        self.inhabitants_result = None
        self.selected_inhabitant_result = None
        self.inhabitant_info_result = None

        self.houses_event = threading.Event()
        self.players_event = threading.Event()
        self.inhabitants_event = threading.Event()
        self.selected_inhabitant_event = threading.Event()
        self.inhabitant_info_event = threading.Event()

    def get_houses(self, pos: tuple[int, int]) -> list[dict]:
        """Get the houses in a specific position.

        Args:
            pos (tuple[int, int]): position to get the houses

        Returns:
            list[dict]: list of houses in the position area
        """
        print("getting houses...")
        thread = threading.Thread(target=self.__get_houses, args=(pos,), daemon=True, name="getHouses")
        thread.start()
        self.houses_event.wait()
        return self.houses_result

    def __get_houses(self, pos: tuple[int, int]):
        try:
            response = requests.get(f"{self.url}/getHouses/?x={pos[0]}&y={pos[1]}").json()
            if response["status"] == 1:
                self.houses_result = response["houses"]
            else:
                self.houses_result = []
        except Exception as e:
            self.houses_result = []
        finally:
            self.houses_event.set()

    def get_players(self) -> list[dict]:
        """Get the players in the game.

        Returns:
            list[dict]: list of players in the game
        """
        thread = threading.Thread(target=self.__get_players, daemon=True, name="getPlayers")
        thread.start()
        self.players_event.wait()
        return self.players_result

    def __get_players(self):
        try:
            response = requests.get(f"{self.url}/getPlayers").json()
            if response["status"] == 1:
                self.players_result = response["players"]
            else:
                self.players_result = []
        except Exception as e:
            self.players_result = []
        finally:
            self.players_event.set()

    def get_house_residents(self, house_id: int) -> list[dict]:
        """Get the residents of a house.

        Args:
            house_id (int): house id to get the residents

        Returns:
            list[dict]: list of residents in the house
        """
        response = requests.get(f"{self.url}/getHousesResidents/?houseId={house_id}").json()
        if response["status"] == 1:
            return response["residents"]
        else:
            return []

    def get_available_inhabitants(self, pos: tuple[int, int]) -> list[dict]:
        """Get the available inhabitants in a specific position.

        Args:
            pos (tuple[int, int]): position to get the available inhabitants

        Returns:
            list[dict]: list of available inhabitants in the position area
        """
        print("getting available inhabitants...")
        thread = threading.Thread(target=self.__get_available_inhabitants, args=(pos,), daemon=True, name="getAvailableInhabitants")
        thread.start()
        self.inhabitants_event.wait()
        return self.inhabitants_result

    def __get_available_inhabitants(self, pos: tuple[int, int]):
        try:
            response = requests.get(f"{self.url}/getAvailableInhabitants/?x={pos[0]}&y={pos[1]}").json()
            if response["status"] == 1:
                self.inhabitants_result = response["inhabitants"]
            else:
                self.inhabitants_result = []
        except Exception as e:
            self.inhabitants_result = []
        finally:
            self.inhabitants_event.set()

    def select_available_inhabitant(self, inhabitant_id: int) -> dict:
        """Select an available inhabitant to play with.

        Args:
            inhabitant_id (int): inhabitant id to select

        Returns:
            dict: selected inhabitant
        """
        response = requests.get(f"{self.url}/selectAvailableInhabitant/?id={inhabitant_id}").json()
        return response

    def get_inhabitant_information(self, inhabitant_id: int) -> dict:
        """Get the information of an inhabitant.

        Args:
            inhabitant_id (int): inhabitant id to get the information

        Returns:
            dict: inhabitant information
        """
        response = requests.get(f"{self.url}/getInhabitantInformation/?id={inhabitant_id}").json()
        return response