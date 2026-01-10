from Pawn import Pawn
from Cell import Cell, CellType
from enum import Enum
from copy import deepcopy
from ThrowingSticks import ThrowingSticks


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

    def get_pawns_of_player(self, color):
        player_pawns = []

        for pawn in self.pawns:
            #بجيب احجار اللاعب الحالي والاحجار يلي طلعت من البورد ما برجعها
            if pawn.color == color and pawn.cell_id is not None:
                player_pawns.append(pawn)

        return player_pawns
    
    def show_movable_pawns(self):
        movable = self.get_movable_pawns(self.current_dice)
        print("You can move the following pawns:", movable)

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
        print(f"Player: {self.current_player}\n")
        for row_ids in SENET_PATH:  # يستخدم المصفوفة الأصلية ليعرف ترتيب الأرقام
            for cell_id in row_ids:
                # يجلب بيانات الخلية من القاموس الخطي
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

        if pawn_id not in allowed_pawns:
            print("This pawn cannot be moved with the current dice result")
            return False
        
        pawn = self.get_pawn(pawn_id)
        if not pawn:
            return False

        if pawn.color != self.current_player:
            print("invalid move: cannot move opponent's pawn")
            return False
        
        # عالجنا حالة الانتقال ل 15 هون بل تابع special_to15
        moved_pawns_to_15 = []
        for cell_id in [28, 29 , 30]:
            cell = self.get_cell(cell_id)
            if cell.occupied_by and cell.occupied_by.color == self.current_player:
                # اذا الحجر يلي رح يختارو اللاعب غير يلي موجود ع الخلايا الخاصة ، رح نرجع الحجر لل 15
                if cell.occupied_by.id != pawn_id:
                    moved_pawns_to_15.append(cell.occupied_by.id)

        # if pawn.cell_id == 30:
        #     self.exit(pawn_id)
        #     self.switch_player()
        #     return True
        """هون كان عم يرجع الحجر ل 15 ببداية الدور قبل ما اللاعب يختار حجر ليحركو"""
        # moved_pawn_ids = self.special_to15()

        # if moved_pawn_ids and pawn_id in moved_pawn_ids:
        #     self.switch_player()
        #     return True

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

        for pawn_id_to_15 in moved_pawns_to_15:
            self.move_to_15(pawn_id_to_15)

        self.switch_player()
        self.turn_state = wait_dice
        self.current_dice = None
        return True
    

    def move(self, pawn_id, dice_result):
        "تحريك الحجر لخلية فاضية"
        pawn = self.get_pawn(pawn_id)

        current_cell_id = pawn.cell_id
        current_cell = self.get_cell(current_cell_id)
        current_cell.clear()

        target_cell_id = current_cell_id + dice_result
        target_cell = self.get_cell(target_cell_id)
        target_cell.set_pawn(pawn)

        pawn.cell_id = target_cell_id

        if pawn.cell_id in [28, 29, 30]:
            pawn.on_special = True
        else:
            pawn.on_special = False

        self.print_board()

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

        if pawn1.cell_id in [28, 29, 30]:
            pawn1.on_special = True
        else:
            pawn1.on_special = False

        if pawn2.cell_id in [28, 29, 30]:
            pawn2.on_special = True
        else:
            pawn2.on_special = False

        self.print_board()

    def move_to_15(self, pawn_id):
        pawn = self.get_pawn(pawn_id)
        current_cell = self.get_cell(pawn.cell_id)
        current_cell.clear()

        for cell_id in range(15, 0, -1):
            cell = self.get_cell(cell_id)
            if cell.is_empty():
                cell.set_pawn(pawn)
                pawn.cell_id = cell.id
                pawn.on_special = False
                self.print_board()
                return

    # def special_to15(self):
    #     # auto move to 15 in next turn
    #     moved_pawn_ids = []
    #     for cell_id in [28, 29, 30]:
    #         cell = self.get_cell(cell_id)
    #         pawn = cell.occupied_by
    #         if pawn and pawn.on_special and pawn.color == self.current_player:
    #             self.move_to_15(pawn.id)
    #             moved_pawn_ids.append(pawn.id)

    #     return moved_pawn_ids

    def exit(self, pawn_id):
        pawn = self.get_pawn(pawn_id)
        cell = self.get_cell(pawn.cell_id)
        cell.clear()
        pawn.exit_board()
        if pawn.color == "WHITE":
            self.exited_pawns["WHITE"] += 1
        else:
            self.exited_pawns["BLACK"] += 1

        self.print_board()

    
    def get_movable_pawns(self, dice_result):
        movable_pawns = []

        # بجيب كل أحجار اللاعب الحالي
        for pawn in self.get_pawns_of_player(self.current_player):

            move_type = self.get_move_type(pawn.id, dice_result)

            if move_type != 'invalid':
                movable_pawns.append(pawn.id)

        return movable_pawns
    
    def is_game_over(self):
        return(
            self.exited_pawns["WHITE"] == 7 or 
            self.exited_pawns["BLACK"] == 7
        )
    
    def get_winner(self):
        if self.exited_pawns["WHITE"] == 7:
            return "WHITE"
        if self.exited_pawns["BLACK"] == 7:
            return "BLACK"
        return None


if __name__ == "__main__":
    board = Board()

    while True:
        if board.is_game_over():
            print("Game Over!")
            print("Winner:" , board.get_winner())
            break
        
        print("\n" + "-" * 10)
        board.print_board()

        # print(f"Current player: {board.current_player}")

        if board.turn_state == wait_dice:
            input("press Enter to throw sticks ")
            steps = board.roll_dice()
            movable = board.get_movable_pawns(steps)

            if not movable:
                print("No possible moves. Turn skipped.")
                board.switch_player()
                board.turn_state = wait_dice
                continue
            
            print("you can moves these pawns:" , movable)

        elif board.turn_state == wait_move:
            try:
                pawn_id = int(input("choose pawn id to move: "))
            except ValueError:
                print("please enter a valid number")
                continue

            success = board.handle_movement(pawn_id , board.current_dice)

            if success:
                board.turn_state = wait_dice
            else:
                print("Try again")




    # MOVE
    # print(board.get_move_type(14, 2))
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 1)
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 1)
    # print(board.get_cell(15).occupied_by)

    # SWAP
    # print(board.get_move_type(1, 5))
    # print(board.get_cell(1).occupied_by.id)
    # board.handle_movement(1, 5)
    # print(board.get_cell(1).occupied_by)
    # print(board.get_cell(5).occupied_by)

    # to 15
    # print(board.get_move_type(14, 5))
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 5)
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 5)
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 3)
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 2)
    # print(board.get_cell(15).occupied_by)
    # board.handle_movement(14, 1)
    # print(board.get_cell(15).occupied_by)

    # special to 15
    # board.handle_movement(14, 1)
    # board.handle_movement(13, 5)
    # board.handle_movement(14, 1)
    # board.handle_movement(13, 5)
    # board.handle_movement(14, 1)
    # board.handle_movement(13, 3)
    # board.handle_movement(14, 1)

    # board.handle_movement(13, 4)
    # board.handle_movement(14, 1)
    # board.handle_movement(13, 5)
    # board.handle_movement(14, 1)
    # board.handle_movement(11, 1)
    # board.handle_movement(14, 4)
    # board.handle_movement(11, 1)
    # board.handle_movement(14, 2)
    # board.handle_movement(11, 1)
    # board.handle_movement(14, 2)
    # board.handle_movement(11, 1)
    # board.handle_movement(12, 1)


    # board.handle_movement(13, 1)
    # print(board.get_cell(28).occupied_by)
    # board.print_board()
    # board.handle_movement(14, 2)

    # board.handle_movement(13, 5)
    # board.handle_movement(13, 5)
    # board.handle_movement(13, 2)
    # board.handle_movement(13, 4)
    # board.handle_movement(13, 1)
