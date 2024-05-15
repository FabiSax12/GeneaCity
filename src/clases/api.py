import threading
import requests

class Api:
    def __init__(self, url) -> None:
        self.url = url
        self.houses_result = None
        self.players_result = None
        self.houses_event = threading.Event()
        self.players_event = threading.Event()

    def get_houses(self, pos: tuple[int, int]) -> list[dict]:
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
            print("Error al obtener casas:", e)
            self.houses_result = []
        finally:
            self.houses_event.set()

    def get_players(self) -> list[dict]:
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
            print("Error al obtener jugadores:", e)
            self.players_result = []
        finally:
            self.players_event.set()

    def get_house_residents(self, house_id: int) -> list[dict]:
        response = requests.get(f"{self.url}/getHousesResidents/?houseId={house_id}").json()
        if response["status"] == 1:
            return response["residentes"]
        else:
            return []