# api_interface.py
from typing import List, Dict, Tuple, Callable

class ApiInterface:
    def get_houses(self, pos: Tuple[float, float], callback: Callable) -> List[Dict]:
        raise NotImplementedError
    
    def get_house_residents(self, house_id: int) -> List[Dict]:
        raise NotImplementedError
    
    def get_available_inhabitants(self, pos: Tuple[int, int], callback: Callable) -> List[Dict]:
        raise NotImplementedError
    
    def select_available_inhabitant(self, inhabitant_id: int) -> bool:
        raise NotImplementedError
    
    def get_inhabitant_information(self, inhabitant_id: int) -> Dict:
        raise NotImplementedError
