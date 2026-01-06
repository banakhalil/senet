from Pawn import Pawn
from Cell import Cell, CellType
from enum import Enum
from copy import deepcopy

# symbols = {
#     CellType.REBIRTH: "#",
#     CellType.HAPPINESS: "@",
#     CellType.WATER: "~",
#     CellType.TRUTH: "%",
#     CellType.RE_ATOUM: "$",
#     CellType.HORUS: "&"
# }

SENET_PATH = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [20, 19, 18, 17, 16, 15, 14, 13, 12, 11],
    [21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
]

SPECIAL_SYMBOLS = {
    15: "#",  # (Rebirth)
    26: "@",  # (Happiness)
    27: "~~",  # (Water)
    28: "%",  # (Three Truths)
    29: "$",  # (Re-Atoum)
    30: "&"  # (Horus)
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
        for i in range(1, 31):
            cell_id = i
            cells[cell_id] = Cell(cell_id)

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

    # def get_cell():
    #     return

    # def get_pawn(self, pawn_id):
    #     return next((x for x in self.pawns if x.id == pawn_id), None)

    def print_board(self):
        for row_ids in SENET_PATH:  # يستخدم المصفوفة الأصلية ليعرف ترتيب الأرقام
            for cell_id in row_ids:
                # يجلب بيانات الخلية من القاموس الخطي
                cell = self.cells[cell_id]
                if cell.occupied_by:
                    print(f"[{cell.occupied_by.color[0]}]", end=" ")
                elif cell_id in SPECIAL_SYMBOLS:
                    print(f"[{SPECIAL_SYMBOLS[cell_id]}]", end=" ")
                else:
                    print(f"[ ]", end=" ")
            print()

        # print("\n")
        # for cell_id in range(1, 11):
        #     cell = self.cells[cell_id]
        #     if cell.occupied_by:
        #         if cell.occupied_by.color == "WHITE":
        #             print(f"{'W' + str(cell.occupied_by.id):<4}",
        #                   end="")
        #         else:
        #             print(f"{'B' + str(cell.occupied_by.id):<4}", end="")
        #     else:
        #         symbol = symbols.get(cell.type, '.')
        #         print(f"{symbol:<4}", end="")
        # print("\n")

        # for cell_id in range(20, 10, -1):
        #     cell = self.cells[cell_id]
        #     if cell.occupied_by:
        #         if cell.occupied_by.color == "WHITE":
        #             print(f"{'W' + str(cell.occupied_by.id):<4}", end="")
        #         else:
        #             print(f"{'B' + str(cell.occupied_by.id):<4}", end="")
        #     else:
        #         symbol = symbols.get(cell.type, '.')
        #         print(f"{symbol:<4}", end="")
        # print("\n")

        # for cell_id in range(21, 31):
        #     cell = self.cells[cell_id]
        #     if cell.occupied_by:
        #         if cell.occupied_by.color == "WHITE":
        #             print(f"{'W' + str(cell.occupied_by.id):<4}", end="")
        #         else:
        #             print(f"{'B' + str(cell.occupied_by.id):<4}", end="")
        #     else:
        #         symbol = symbols.get(cell.type, '.')
        #         print(f"{symbol:<4}", end="")
        # print()

        # print("=" * 40)
        # print("\n")

    def get_move_type(self, pawn_id, dice):

        pawn = self.get_pawn(pawn_id)
        if not pawn or pawn.cell_id == None:
            return 'invalid'

        current_cell_id = pawn.cell_id
        target_cell_id = current_cell_id + dice

        if target_cell_id > 30:
            if current_cell_id in [26, 28, 29, 30]:
                return 'exit'

            else:
                return 'invalid'

        if target_cell_id > 26 and current_cell_id < 26:
            return 'invalid'

        if target_cell_id == 27:
            return 'to_15'

        # if current_cell_id == 28 and dice !=3:
        #     return 'to_15'

        # if current_cell_id == 29 and dice !=2:
        #     return 'to_15'

        # if current_cell_id == 30 and dice !=3:
        #     return 'to_15'
        # الحصول على الخلية الهدف

        target_cell = self.cells[target_cell_id]

        if target_cell.occupied_by is None:
            return 'move'

        target_pawn = target_cell.occupied_by

        if target_pawn.color == pawn.color:
            return 'invalid'

        return 'swap'

    # def handle_movement(self, pawn_id, dice_result):

    #     move_type = self.get_move_type(pawn_id, dice_result)

    #     if move_type == 'invalid':
    #         print("invalid move")
    #         return False

    #     if move_type == 'move':
    #         self.move(pawn_id, dice_result)

    # def move(self, pawn_id, dice):
    #     target_cell_id = pawn_id + dice


if __name__ == "__main__":
    board = Board()
    board.print_board()
    # print(board.get_move_type(1, 4))
