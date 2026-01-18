from Board import Board
from copy import deepcopy
from GameState import GameState

#  هدول التوابع بيستخدمهم computer وقت بيلعب مع الانسان

# تابع إنشاء حالة البداية للعبة


def initial_state():
    board = Board()
    return GameState(board, board.current_player)

# تابع يحدد الحالة يلي رح تنتهي عنها اللعبة


def is_terminal(state):
    return state.board.is_game_over()

# يعيد قائمة بالحركات الممكنة للاعب (Computer) بحسب نتيجة الرمي
# رح نستخدمو بخوارزمية Expectiminimax


def get_valid_moves(state, steps):
    board = state.board
    current_player = state.current_player

    moves = []
    for pawn in board.get_pawns_of_player(current_player):
        move_type = board.get_move_type(pawn.id, steps)
        if move_type != 'invalid':
            moves.append(pawn.id)

    return moves

# وقت خوارزمية ai بدها تطبق حركات معينة رح تستخدم هاد التابع للتفكير


def apply_move(state, pawn_id, steps):
    new_board = deepcopy(state.board)

    new_board.handle_movement(pawn_id, steps)

    return GameState(
        new_board,
        new_board.current_player
    )
