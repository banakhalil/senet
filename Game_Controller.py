# التوابع هون لتناوب اللعب بين المستخدم والكمبيوتر
from Expectiminimax import Expectiminimax
from GameState import GameState


class GameController:
    def __init__(self, board):
        self.board = board
        self.ai_agent = Expectiminimax(depth=2, ai_color="WHITE")

    def play_turn(self):
        steps = self.board.roll_dice()

        if not steps:
            return

        movable = self.board.get_movable_pawns(steps)
        if not movable:
            print("No possible moves. Turn skipped")
            self.board.switch_player()
            self.board.turn_state = "wait_dice"
            return

        print("you can move these pawns:", movable)

        if self.board.current_player == "BLACK":
            # Human
            while True:
                try:
                    pawn_id = int(input("Choose pawn: "))
                except ValueError:
                    print("Please enter a valid number")
                    continue

                success = self.board.handle_movement(pawn_id, steps)
                if success:
                    break

            print(
                f"WHITE: {self.board.exited_pawns["WHITE"]}   BLACK: {self.board.exited_pawns["BLACK"]}")
            print("\n" + "-" * 10)
            print(f"Player: {self.board.current_player}")
            self.board.print_board()
        else:
            # Computer
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

            print(
                f"AI selected pawn ID: {best_pawn_id} based on evaluation: {score}")
            self.board.handle_movement(best_pawn_id, steps)
            print(
                f"WHITE: {self.board.exited_pawns["WHITE"]}   BLACK: {self.board.exited_pawns["BLACK"]}")
            print("\n" + "-" * 10)
            print(f"Player: {self.board.current_player}")
            self.board.print_board()
