from enum import Enum


class CellType(Enum):
    NORMAL = 0
    REBIRTH = 15
    HAPPINESS = 26
    WATER = 27
    TRUTH = 28
    RE_ATOUM = 29
    HORUS = 30


class Cell:
    def __init__(self, x, y, cell_id, cell_type=CellType.NORMAL, occupied_by=None):
        self.x = x
        self.y = y
        self.coordinates = (x, y)
        self.id = cell_id
        self.type = cell_type
        self.occupied_by = occupied_by

    def is_empty(self):
        return self.occupied_by is None

    # for movement
    def set_pawn(self, pawn):
        self.occupied_by = pawn

    def clear(self):
        self.occupied_by = None
