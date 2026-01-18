from Pawn import Pawn
from Cell import Cell, CellType
from enum import Enum
from copy import deepcopy
from ThrowingSticks import ThrowingSticks

# S لتسهيل عمليه الطباعة عللا شكل حرف
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

wait_dice = "wait_dice"
wait_move = "wait_move"


class Board:
    def __init__(self):
        self.pawns = []
        self.cells = self._init_cells()
        self._init_pawns()
        self.current_player = "BLACK"
        self.turn_state = wait_dice
        self.current_dice = None
        self.exited_pawns = {"WHITE": 0, "BLACK": 0}
        self.stick_thrower = ThrowingSticks()

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

    def get_cell(self, cell_id):
        return self.cells[cell_id]

    def get_pawn(self, pawn_id):
        return next((x for x in self.pawns if x.id == pawn_id), None)

    def roll_dice(self):
        if self.turn_state != wait_dice:
            print("you must move before rolling again")
            return None

        self.current_dice = self.stick_thrower.throw_sticks()
        self.turn_state = wait_move

        print(f"Num of steps: {self.current_dice}")
        return self.current_dice

    def copy(self):
        return deepcopy(self)

    def switch_player(self):
        self.current_player = "WHITE" if self.current_player == "BLACK" else "BLACK"

    def print_board(self):
        print("\n")
        # print(f"Player: {self.current_player}\n")
        for row_ids in SENET_PATH:  # S يستخدم هذا المسار لترتيب الطباعة بشكل
            for cell_id in row_ids:
                # (dictionary) يجلب بيانات الخلية من مصفوفة الخلايا
                cell = self.cells[cell_id]
                if cell.occupied_by:
                    print(
                        f"[{cell.occupied_by.color[0]}{cell.occupied_by.id:<2}]", end=" ")
                elif cell_id in SPECIAL_SYMBOLS:
                    print(f"[{SPECIAL_SYMBOLS[cell_id]:<3}]", end=" ")
                else:
                    print(f"[   ]", end=" ")
            print("\n")

    def get_move_type(self, pawn_id, dice_result):

        pawn = self.get_pawn(pawn_id)
        if not pawn or pawn.cell_id == None:
            return 'invalid'

        current_cell_id = pawn.cell_id
        # نوع الحركة حسب الخلية الحالية
        if current_cell_id == 30:
            return 'exit'

        if current_cell_id == 28:
            if dice_result == 3:
                return 'exit'
            else:
                return 'to_15'

        if current_cell_id == 29:
            if dice_result == 2:
                return 'exit'
            else:
                return 'to_15'

        # نوع الحركة بالاعتماد على الخلية الهدف
        target_cell_id = current_cell_id + dice_result

        if current_cell_id == 26:
            if target_cell_id > 30:
                return 'exit'

        if target_cell_id > 26 and current_cell_id < 26:
            return 'invalid'

        if target_cell_id == 27:
            return 'to_15'

        target_cell = self.cells[target_cell_id]

        if target_cell.occupied_by is None:
            return 'move'

        target_pawn = target_cell.occupied_by

        if target_pawn.color == pawn.color:
            return 'invalid'

        return 'swap'

    def handle_movement(self, pawn_id, dice_result):
        allowed_pawns = self.get_movable_pawns(dice_result)

        pawn = self.get_pawn(pawn_id)
        if not pawn:
            return False

        if pawn.color != self.current_player:
            print("invalid move: cannot move opponent's pawn")
            return False

        if pawn_id not in allowed_pawns:
            print("This pawn cannot be moved with the current dice result")
            return False

        # التحقق من وجود احجار على الخلايا الخاصة، ولم يقم اللاعب بتحريكها
        moved_pawns_to_15 = self.special_to15(pawn_id)

        # نوع الحركة
        move_type = self.get_move_type(pawn_id, dice_result)

        if move_type == 'invalid':
            print("invalid move")
            return False

        elif move_type == 'move':
            self.move(pawn_id, dice_result)

        elif move_type == 'swap':
            self.swap(pawn_id, dice_result)

        elif move_type == 'to_15':
            self.move_to_15(pawn_id)

        elif move_type == 'exit':
            self.exit(pawn_id)

        # في نهاية كل دور، التحقق من وجود احجار يجب ان تعاد الى بيت البعث
        if moved_pawns_to_15:
            for pawn_id_to_15 in moved_pawns_to_15:
                self.move_to_15(pawn_id_to_15)

        self.switch_player()
        self.turn_state = wait_dice
        self.current_dice = None
        return True

    def move(self, pawn_id, dice_result):
        # تحريك الحجر لخلية فاضية
        pawn = self.get_pawn(pawn_id)

        current_cell_id = pawn.cell_id
        current_cell = self.get_cell(current_cell_id)
        current_cell.clear()

        target_cell_id = current_cell_id + dice_result
        target_cell = self.get_cell(target_cell_id)
        target_cell.set_pawn(pawn)

        pawn.cell_id = target_cell_id

    def swap(self, pawn_id, dice_result):
        pawn1 = self.get_pawn(pawn_id)

        current_cell_id = pawn1.cell_id
        current_cell = self.get_cell(pawn1.cell_id)

        target_cell_id = current_cell_id + dice_result
        target_cell = self.get_cell(target_cell_id)

        pawn2 = self.get_pawn(target_cell.occupied_by.id)

        current_cell.set_pawn(pawn2)
        pawn2.cell_id = current_cell_id

        target_cell.set_pawn(pawn1)
        pawn1.cell_id = target_cell_id

    def move_to_15(self, pawn_id):
        pawn = self.get_pawn(pawn_id)
        current_cell = self.get_cell(pawn.cell_id)
        current_cell.clear()

        for cell_id in range(15, 0, -1):
            cell = self.get_cell(cell_id)
            if cell.is_empty():
                cell.set_pawn(pawn)
                pawn.cell_id = cell.id
                return

    def special_to15(self, pawn_id):
        # برجع ليست من الاحجار يلي لازم ترجع عال15
        moved_pawn_ids = []
        for cell_id in [28, 29, 30]:
            cell = self.get_cell(cell_id)
            pawn = cell.occupied_by
            if pawn and pawn.color == self.current_player:
                # اذا الحجر يلي رح يختارو اللاعب مو نفسو يلي موجود ع الخلايا الخاصة ، رح نرجع الحجر لل 15
                if pawn.id != pawn_id:
                    moved_pawn_ids.append(pawn.id)

        return moved_pawn_ids

    def exit(self, pawn_id):
        pawn = self.get_pawn(pawn_id)
        cell = self.get_cell(pawn.cell_id)
        cell.clear()
        pawn.exit_board()
        if pawn.color == "WHITE":
            self.exited_pawns["WHITE"] += 1
        else:
            self.exited_pawns["BLACK"] += 1

    def get_pawns_of_player(self, color):
        player_pawns = []

        for pawn in self.pawns:
            # بجيب احجار اللاعب الحالي والاحجار يلي طلعت من البورد ما برجعها
            if pawn.color == color and pawn.cell_id is not None:
                player_pawns.append(pawn)

        return player_pawns

    def get_movable_pawns(self, dice_result):
        movable_pawns = []

        # بجيب كل أحجار اللاعب الحالي
        for pawn in self.get_pawns_of_player(self.current_player):

            move_type = self.get_move_type(pawn.id, dice_result)

            if move_type != 'invalid':
                movable_pawns.append(pawn.id)

        return movable_pawns

    def is_game_over(self):
        return (
            self.exited_pawns["WHITE"] == 7 or
            self.exited_pawns["BLACK"] == 7
        )

    def get_winner(self):
        if self.exited_pawns["WHITE"] == 7:
            return "WHITE"
        if self.exited_pawns["BLACK"] == 7:
            return "BLACK"
        return None
