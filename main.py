from Board import Board, wait_dice, wait_move
from Game_Controller import GameController


def play_human():
    board = Board()

    while True:
        if board.is_game_over():
            print("Game Over!")
            print("Winner:", board.get_winner())
            break

        if board.turn_state == wait_dice:
            print("\n" + "-" * 10)
            board.print_board()
            input("press Enter to throw sticks ")
            steps = board.roll_dice()
            movable = board.get_movable_pawns(steps)

            if not movable:
                print("No possible moves. Turn skipped.")
                board.switch_player()
                board.turn_state = wait_dice
                continue

            print("you can moves these pawns:", movable)

        elif board.turn_state == wait_move:
            try:
                pawn_id = int(input("choose pawn id to move: "))
            except ValueError:
                print("please enter a valid number")
                continue

            success = board.handle_movement(pawn_id, board.current_dice)

            if success:
                board.turn_state = wait_dice
            else:
                print("Try again")

# تابع اللعب مع الذكاء، منعدل عليه حسب مو طالبين بملف المشروع بس هاد مبدئي
# def play_ai():
#     board = Board()
#     controller = GameController(board)

#     while not board.is_game_over():
#         controller.play_turn()

#     print("\nGame Over!")
#     print("Winner:", board.get_winner())


def main():
    print("Choose mode:")
    print("1. Human x Human")
    print("2. Human x AI")
    print("3. Exit")

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            play_human()
            break
        elif choice == "2":
            play_ai()
            break
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
