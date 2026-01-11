class Pawn:
    def __init__(self, pawn_id, pawn_color, cell_id=None):
        self.id = pawn_id
        self.color = pawn_color
        self.cell_id = cell_id
        # self.on_special = False  # for tracking, 28,29,30

    def exit_board(self):
        self.cell_id = None
        # self.on_special = False
