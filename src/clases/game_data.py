import json
import os

class GameData:
    """
    Base class for managing game data from a JSON file.
    """

    def __init__(self, path):
        """
        Initializes the GameData object.

        Args:
            path (str): The path to the JSON file.
        """
        self.path = path

    def load(self):
        """
        Loads the game data from the JSON file.

        Returns:
            dict: The game data loaded from the file.
        """
        try:
            with open(self.path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            # Handles file not found errors
            return {}
        except json.JSONDecodeError:
            # Handles JSON decoding errors
            print("Error decoding JSON file")
            return {}

    def save(self, data):
        """
        Saves the game data to the JSON file.

        Args:
            data (dict): The game data to save to the file.
        """
        try:
            with open(self.path, "w") as file:
                json.dump(data, file, indent=4)
        except json.JSONDecodeError:
            print("Error decoding JSON file")
        except Exception as e:
            print(f"Error saving game data: {e}")

class GameDataManager(GameData):
    """
    Class for managing game data from a JSON file.
    """

    def __init__(self):
        """
        Initializes the GameDataManager object.
        """
        self.os = self._detect_os()
        self.path = self._detect_path()

    def _detect_os(self):
        """
        Detects the operating system.

        Returns:
            str: The operating system name.
        """
        if os.name == "posix":
            return "Linux"
        elif os.name == "nt":
            return "Windows"
        else:
            return None

    def _detect_path(self):
        """
        Detects the path to the game data file.

        Returns:
            str: The path to the game data file.
        """
        if self.os:
            return os.path.expanduser("~/Documents/Geneacity/game_history.json")
        else:
            return None 
        
    
