# التوابع هون لتناوب اللعب بين المستخدم والكمبيوتر
class GameController:
    def __init__(self, board):
        self.board = board
        self.ai_agent = Expectiminimax(depth=2, ai_color="WHITE")
    def play_turn(self):
        steps = self.board.roll_dice()
        if not steps: return
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
            # pawn_id = movable[0]
            # self.board.handle_movement(pawn_id, steps)
            # self.board.print_board()

            
            current_state = GameState(self.board, self.board.current_player)
            
            # استدعاء Expectiminimax
            score, best_pawn_id = self.ai_agent.expectiminimax(
                current_state, 
                self.ai_agent.max_depth, 
                False, 
                steps
            )

            if best_pawn_id is None:
                best_pawn_id = movable[0]

                print(f"AI selected pawn ID: {best_pawn_id} based on evaluation: {score}")            self.board.handle_movement(best_pawn_id, steps)
            self.board.print_board()