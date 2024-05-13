import requests as http

class Api():
    def __init__(self, url) -> None:
        self.url = url

    def get_houses(self, pos: tuple[int, int]) -> list[dict]:
        response = http.get(f"{self.url}/getHouses/?x={pos[0]}&y={pos[1]}").json()
        if response["status"] == 1:
            return response["houses"]
        else:
            return []
        
    def get_players(self) -> list[dict]:
        response = http.get(f"{self.url}/getPlayers").json()
        if response["status"] == 1:
            return response["players"]
        else:
            return []