from Pawn import Pawn
from Cell import Cell, CellType
from enum import Enum
from copy import deepcopy

symbols = {
    CellType.REBIRTH: "#",
    CellType.HAPPINESS: "@",
    CellType.WATER: "~",
    CellType.TRUTH: "%",
    CellType.RE_ATOUM: "$",
    CellType.HORUS: "&"
}


class Board:
    def __init__(self):
        self.pawns = []
        self.cells = self._init_cells()
        self._init_pawns()
        self.current_player = "BLACK"
        self.exited_pawns = {"white": 0, "black": 0}

    def _init_cells(self):
        cells = {}
        # 1 - 10
        for i in range(10):
            cell_id = i + 1
            cells[cell_id] = Cell(cell_id, 0, i)

        # 11 - 20
        for i in range(10):
            cell_id = 20 - i
            cells[cell_id] = Cell(cell_id, 1, i)

        # 21 - 30
        for i in range(10):
            cell_id = 21 + i
            cells[cell_id] = Cell(cell_id, 2, i)

        special_ids = [15, 26, 27, 28, 29, 30]
        for cell_id in special_ids:
            cell_type = CellType(cell_id)
            cells[cell_id].type = cell_type

        return cells

    def _init_pawns(self):
        pawn_id = 1

        for cell_id in range(1, 15):
            color = "WHITE" if cell_id % 2 == 1 else "BLACK"
            pawn = Pawn(pawn_id, color, cell_id)

            self.pawns.append(pawn)
            self.cells[cell_id].occupied_by = pawn
            pawn_id += 1

    def print_board(self):
        print("\n")
        for cell_id in range(1, 11):
            cell = self.cells[cell_id]
            if cell.occupied_by:
                if cell.occupied_by.color == "WHITE":
                    print(f"{'W' + str(cell.occupied_by.id):<4}",
                          end="")
                else:
                    print(f"{'B' + str(cell.occupied_by.id):<4}", end="")
            else:
                symbol = symbols.get(cell.type, '.')
                print(f"{symbol:<4}", end="")
        print("\n")

        for cell_id in range(20, 10, -1):
            cell = self.cells[cell_id]
            if cell.occupied_by:
                if cell.occupied_by.color == "WHITE":
                    print(f"{'W' + str(cell.occupied_by.id):<4}", end="")
                else:
                    print(f"{'B' + str(cell.occupied_by.id):<4}", end="")
            else:
                symbol = symbols.get(cell.type, '.')
                print(f"{symbol:<4}", end="")
        print("\n")

        for cell_id in range(21, 31):
            cell = self.cells[cell_id]
            if cell.occupied_by:
                if cell.occupied_by.color == "WHITE":
                    print(f"{'W' + str(cell.occupied_by.id):<4}", end="")
                else:
                    print(f"{'B' + str(cell.occupied_by.id):<4}", end="")
            else:
                symbol = symbols.get(cell.type, '.')
                print(f"{symbol:<4}", end="")
        print()

        print("=" * 40)
        print("\n")


if __name__ == "__main__":
    board = Board()
    board.print_board()
