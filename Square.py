from refs import Character, SquareType

class Square:
    """Representation of Square in Hnefatafl game."""

    def __init__(self, lox: tuple):
        """Initializes Square fields."""

        # represents location of the square
        self.lox = lox

        # represents what type of square this is
        self.type = SquareType.NORMAL

        # represents what character, if any, is currently on this square
        self.occupied = Character.EMPTY

    # ---------------------------------------------------------------------------
    # setter methods
    def set_type(self, type: SquareType):
        """Sets the Square type."""
        self.type = type
    def set_character(self, character: Character):
        """Sets the Character on the Square."""
        self.occupied = character
    def clear(self):
        """Sets that a Character has left the Square."""
        self.occupied = Character.EMPTY

    # ---------------------------------------------------------------------------
    # getter methods
    def get_character(self) -> SquareType:
        return self.type
    def get_occupied(self) -> Character:
        return self.occupied

    # ---------------------------------------------------------------------------
    # attacker methods
    def is_available_for_attacker(self) -> bool:
        """Checks that the Square can accept an Attacker."""
        return self.type != SquareType.REFUGE and self.occupied == Character.EMPTY

    def is_available_for_defender(self) -> bool:
        """Checks that the Square can accept a Defender."""
        return self.type != SquareType.REFUGE and self.occupied == Character.EMPTY

    def is_available_for_king(self) -> bool:
        """Checks that the Square can accept the King."""
        return self.occupied == Character.EMPTY
    
    def move_attacker_here(self):
        """Moves an Attacker to the Square."""
        self.occupied = Character.ATTACKER

    def move_defender_here(self):
        """Moves a Defender to the Square."""
        self.occupied = Character.DEFENDER

    def move_king_here(self):
        """Moves the King to the Square."""
        self.occupied = Character.KING

    # ---------------------------------------------------------------------------
    # utility methods
    def to_string(self) -> str:
        if self.occupied == Character.KING:
            return "@"
        elif self.occupied == Character.DEFENDER:
            return "D"
        elif self.occupied == Character.ATTACKER:
            return "A"
        else:
            return "•"