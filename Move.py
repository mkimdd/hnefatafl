class Move:
    def __init__(self, source: tuple, destination: tuple):
        self.source = source
        self.destination = destination
    def get_source(self) -> tuple:
        return self.source
    def get_destination(self) -> tuple:
        return self.destination
    def __repr__(self) -> str:
        return f"{self.source} to {self.destination}"