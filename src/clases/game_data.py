import json
import os

class FileManager:
    """Class to handle file operations for game data."""
    
    @staticmethod
    def read_json(path: str):
        try:
            with open(path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    @staticmethod
    def write_json(path: str, data: dict):
        try:
            with open(path, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            raise Exception(f"Error saving game data: {e}")

class GameDataManager:
    """
    Singleton class for managing game data from a JSON file.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameDataManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the GameDataManager object.
        """
        self.path = os.path.expanduser("~\\Documents\\Geneacity\\game_history.json")
        self.__data = None

        # Create the folder if it doesn't exist
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w") as file:
                json.dump([], file)

    def load(self) -> dict:
        """
        Loads the game data from the JSON file.

        Returns:
            dict: The game data loaded from the file.
        """
        return FileManager.read_json(self.path)

    def save(self):
        """
        Saves the game data to the JSON file.
        """
        current_data = self.load()

        if current_data == []:
            current_data.append(self.data)
        else:
            for i in range(len(current_data)):
                if current_data[i]["id"] == self.data["id"]:
                    current_data[i] = self.data
                    break
            else:
                current_data.append(self.data)

        FileManager.write_json(self.path, current_data)

    def update(self):
        """
        Updates the game data in the JSON file.
        """
        current_data = self.load()
        current_data[-1] = self.data
        FileManager.write_json(self.path, current_data)

    def load_last_game(self) -> dict:
        """
        Loads the last game data from the JSON file.

        Returns:
            dict: The last game data loaded from the file.
        """
        all_games = self.load()
        if not all_games:
            return None
        return all_games[-1]

    @property
    def data(self) -> dict:
        """Gets the game data."""
        return self.__data

    @data.setter
    def data(self, new_data: dict):
        """Sets the game data."""
        self.__data = new_data

    @data.deleter
    def data(self):
        """Deletes the game data."""
        self.__data = None
