import json
import os

class GameDataManager:
    """
    Class for managing game data from a JSON file.
    """

    def __init__(self):
        """
        Initializes the GameDataManager object.
        """
        self.path = os.path.expanduser("~\\Documents\\Geneacity\\game_history.json")
        self.__data = None

        # Crear la carpeta si no existe
        if not os.path.exists(self.path):
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w") as file:
                json.dump([], file)

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
            return []
        except json.JSONDecodeError:
            # Handles JSON decoding errors
            return []

    def save(self):
        """
        Saves the game data to the JSON file.
        """

        current_data = self.load()

        # Add new data
        if current_data == []:
            print("New game data added")
            current_data.append(self.data)
        else:
            for i in range(len(current_data)):
                if current_data[i]["id"] == self.data["id"]:
                    current_data[i] = self.data
                    break
                elif i == len(current_data) - 1:
                    current_data.append(self.data)

        try:
            with open(self.path, "w") as file:
                json.dump(current_data, file, indent=4)
        except Exception as e:
            raise Exception(f"Error saving game data: {e}")

    def update(self):
        """
        Updates the game data in the JSON file.
        """
        current_data = self.load()

        # Find and update the data
        current_data[-1] = self.data

        try:
            with open(self.path, "w") as file:
                json.dump(current_data, file, indent=4)
        except Exception as e:
            raise Exception(f"Error updating game data: {e}")

    def load_last_game(self):
        """
        Loads the last game data from the JSON file.

        Returns:
            dict: The last game data loaded from the file.
        """
        try:
            with open(self.path, "r") as file:
                all_games = json.load(file)
                if not all_games:
                    return None
                return all_games[-1]
        except FileNotFoundError:
            # Handles file not found errors
            return []
        except json.JSONDecodeError:
            # Handles JSON decoding errors
            print("Error decoding JSON file")
            return []

    @property
    def data(self):
        """
        dict: The game data loaded from the file.
        """
        return self.__data
    
    @data.setter
    def data(self, new_data: dict):
        """
        Saves the game data to the JSON file.
        """
        self.__data = new_data


    @data.deleter
    def data(self):
        """
        Deletes the game data from the JSON file.
        """
        self.__data = None
