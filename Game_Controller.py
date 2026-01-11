# التوابع هون لتناوب اللعب بين المستخدم والكمبيوتر
class GameController:
    def __init__(self, board):
        self.board = board

    def play_turn(self):
        steps = self.board.roll_dice()

        movable = self.board.get_movable_pawns(steps)
        if not movable:
            print("No possible moves. Turn skipped")
            self.board.switch_player()
            self.board.turn_state = "wait_dice"
            return

        if self.board.current_player == "BLACK":
            # Human
            try:
                self.board.print_board()
                pawn_id = int(input("Choose pawn: "))
                self.board.handle_movement(pawn_id, steps)
            except ValueError:
                print("please enter a valid number")
                self.board.turn_state = "wait_move"
        else:
            # Computer
            # هون عم يختار اول حركة متاحة منعدلو وقت نبلش بالخوارزميات
            pawn_id = movable[0]
            self.board.handle_movement(pawn_id, steps)
            self.board.print_board()
