class PlayerInterface:
    def draw(self, map_surface):
        raise NotImplementedError

    def move(self, dx: int, dy: int):
        raise NotImplementedError
    
    def increase_score(self, points: int):
        raise NotImplementedError
    
    def decrease_score(self, points: int):
        raise NotImplementedError

    def interact(self, houses: list):
        raise NotImplementedError

    def __save_position(self):
        raise NotImplementedError

    @property
    def pos(self) -> tuple[float, float]:
        raise NotImplementedError

    @property
    def score(self) -> int:
        raise NotImplementedError

    @score.setter
    def score(self, score: int):
        raise NotImplementedError
    