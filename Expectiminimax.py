import math
from ThrowingSticks import stick_throw_probabilities
from AI_Search import is_terminal, get_valid_moves, apply_move


class Expectiminimax:
    def __init__(self, depth, ai_color="WHITE"):
        self.max_depth = depth
        self.ai_color = ai_color
        self.opponent_color = "BLACK" if ai_color == "WHITE" else "WHITE"
        self.nodes_count = 0
        self.log_file = "ai_search_log.txt"

    def write_to_file(self, message):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(message)
        except Exception as e:
            print(f"Error writing to log file: {e}")

    def evaluate_heuristic(self, state):
        score = 0
        board = state.board

        # سكور عند الفوز
        if board.is_game_over():
            winner = board.get_winner()
            if winner == self.ai_color:
                return 10000
            else:
                return -10000

        # سكور عند اخراج حجر
        score += (board.exited_pawns[self.ai_color] * 700)
        score -= (board.exited_pawns[self.opponent_color] * 700)

        # opponent_cells = {p.cell_id for p in board.get_pawns_of_player(self.opponent_color) if p.cell_id is not None}

        for pawn in board.get_pawns_of_player(self.ai_color):
            if pawn.cell_id is not None:
                score += pawn.cell_id

                if pawn.cell_id == 30:
                    score += 600
                elif pawn.cell_id == 26:
                    score += 200
                elif pawn.cell_id == 27:
                    score -= 100
                elif pawn.cell_id == 28:
                    # (600 * 4/16) + (15 * 12/16) احتمال الحصول على 3 والفوز + احتمال الحصول على قيمة اخرى والخسارة
                    score += 161.25
                elif pawn.cell_id == 29:
                    # (600 * 6/16) + (15 * 10/16)
                    score += 250

                # سكور اعلى حسب السطر
                if 1 <= pawn.cell_id <= 10:
                    # +3, +6, ... +30
                    score += (pawn.cell_id) * 3

                elif 11 <= pawn.cell_id <= 15:
                    # +31, 35, ... +47
                    score += 27 + (pawn.cell_id - 10) * 4
                elif 16 <= pawn.cell_id <= 25:
                    # +74, +81,... +137
                    # وبضل اقل من قيمة 26
                    score += 67 + (pawn.cell_id - 15) * 7

                # # Vulnerability to swaps: penalize our pawns that opponent can land on (dice 1-5)
                # for d in range(1, 6):
                #     if pawn.cell_id - d >= 1 and (pawn.cell_id - d) in opponent_cells:
                #         if pawn.cell_id >= 16:
                #             score -= 30
                #         elif pawn.cell_id >= 11:
                #             score -= 20
                #         else:
                #             score -= 10
                #         break

                # # Strategic positioning: reward being close to special cells (favor advancing)
                # if pawn.cell_id < 26:
                #     # Distance to cell 26 (Happiness)
                #     dist_to_26 = 26 - pawn.cell_id
                #     if dist_to_26 <= 11:
                #         score += (12 - dist_to_26) * 15  # Bonus: 45, 30, 15 for 1, 2, 3 steps away

        for pawn in board.get_pawns_of_player(self.opponent_color):
            if pawn.cell_id is not None:
                score -= pawn.cell_id

                if pawn.cell_id == 30:
                    score -= 600
                elif pawn.cell_id == 26:
                    score -= 200
                elif pawn.cell_id == 27:
                    score += 100
                elif pawn.cell_id == 28:
                    score -= 161.25
                elif pawn.cell_id == 29:
                    score -= 250

                if 2 <= pawn.cell_id <= 10:
                    # -3, -6, ... -30
                    score -= (pawn.cell_id - 1) * 3
                elif 11 <= pawn.cell_id <= 15:
                    # -31, -35, ... -47
                    score -= 27 + (pawn.cell_id - 10) * 4
                elif 16 <= pawn.cell_id <= 25:
                    # -74, -81,... -137
                    score -= 67 + (pawn.cell_id - 15) * 7

                # # Strategic positioning: penalize opponent being close to special cells
                # if pawn.cell_id < 26:
                #     # Distance to cell 26 (Happiness)
                #     dist_to_26 = 26 - pawn.cell_id
                #     if dist_to_26 <= 11:
                #         score -= (12 - dist_to_26) * 15  # Penalty: -45, -30, -15 for 1, 2, 3 steps away

                # for d in range(1, 6):
                #     if pawn.cell_id - d >= 1 and (pawn.cell_id - d) in opponent_cells:
                #         if pawn.cell_id >= 16:
                #             score += 30
                #         elif pawn.cell_id >= 11:
                #             score += 20
                #         else:
                #             score += 10
                #         break

        if board.current_player == self.opponent_color:
            dice_to_check = board.current_dice if board.current_dice else 1
            movable_pawns = board.get_movable_pawns(dice_to_check)

            if not movable_pawns:
                score += 100

        return score


    def expectiminimax(self, state, depth, is_chance_node, current_dice=None, indent=""):
        # زيادة عداد العقد عند زيارة كل عقدة جديدة
        self.nodes_count += 1

        # تحضير معلومات العقدة لطباعتها في الملف
        node_type = "CHANCE" if is_chance_node else (
            "MAX" if state.current_player == self.ai_color else "MIN")
        log_entry = f"{indent}Node: {node_type}, Depth: {depth}, Dice: {current_dice}\n"
        self.write_to_file(log_entry)

        # حالة النهاية (حالة فوز أو وصول لأقصى عمق)
        if depth == 0 or is_terminal(state):
            score = self.evaluate_heuristic(state)
            self.write_to_file(f"{indent}Reached Leaf - Value: {score}\n")
            return score, None

        if is_chance_node:
            expected_value = 0
            probs = stick_throw_probabilities()

            for dice_val, prob in probs.items():
                val, _ = self.expectiminimax(
                    state, depth - 1, False, dice_val, indent + "  ")
                expected_value += prob * val

            self.write_to_file(f"{indent}Chance Node Result: {expected_value}\n")
            return expected_value, None

        else:
            movable_pawns = get_valid_moves(state, current_dice)

            if not movable_pawns:
                val, _ = self.expectiminimax(
                    state, depth - 1, True, None, indent + "  ")
                return val, None

            # if AI swaps human, add bonus of 8
            if state.current_player == self.ai_color:
                best_val = -math.inf
                best_move = None

                for pawn_id in movable_pawns:
                    is_swap = (state.board.get_move_type(
                        pawn_id, current_dice) == 'swap')

                    next_state = apply_move(state, pawn_id, current_dice)

                    val, _ = self.expectiminimax(
                        next_state, depth - 1, True, None, indent + "  ")

                    if is_swap:
                        val += 8
                    if val > best_val:
                        best_val = val
                        best_move = pawn_id

                    # عند تساوي السكورات اختار الحجر الابعد
                    if val == best_val:
                        if state.board.get_pawn(pawn_id).cell_id > state.board.get_pawn(best_move).cell_id:
                            best_move = pawn_id

                self.write_to_file(f"{indent}MAX Node Best Value: {best_val}\n")
                return best_val, best_move
            else:
                best_val = math.inf
                best_move = None

                for pawn_id in movable_pawns:
                    is_swap = (state.board.get_move_type(
                        pawn_id, current_dice) == 'swap')

                    next_state = apply_move(state, pawn_id, current_dice)

                    val, _ = self.expectiminimax(
                        next_state, depth - 1, True, None, indent + "  ")

                    if is_swap:
                        val -= 8
                    if val < best_val:
                        best_val = val
                        best_move = pawn_id

                    if val == best_val:
                        if state.board.get_pawn(pawn_id).cell_id < state.board.get_pawn(best_move).cell_id:
                            best_move = pawn_id

                self.write_to_file(f"{indent}MIN Node Best Value: {best_val}\n")
                return best_val, best_move
