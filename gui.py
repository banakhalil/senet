import tkinter as tk
from tkinter import messagebox
from Board import Board, SENET_PATH, SPECIAL_SYMBOLS
from Expectiminimax import Expectiminimax
from GameState import GameState


class SenetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("  Senet  ")
        self.board_logic = Board()
        self.buttons = {}
        self.game_mode = None  # 1: إنسان ضد إنسان، 2: إنسان ضد كمبيوتر

        # الكمبيوتر سيلعب باللون الأبيض ، وعمق البحث 2
        self.ai_engine = Expectiminimax(depth=2, ai_color="WHITE")

        # إظهار شاشة اختيار النمط عند التشغيل
        self.setup_start_screen()

    # mode screen
    def setup_start_screen(self):
        self.start_frame = tk.Frame(self.root, pady=50, padx=50)
        self.start_frame.pack()

        tk.Label(self.start_frame, text="SENET", font=(
            "Arial", 18, "bold")).pack(pady=10)
        tk.Label(self.start_frame, text="Choose Mode",
                 font=("Arial", 12)).pack(pady=10)

        tk.Button(self.start_frame, text="إنسان ضد إنسان", width=25, height=2, font=("Arial", 10, "bold"),
                  bg="#3498db", fg="white", command=lambda: self.start_game(1)).pack(pady=5)

        tk.Button(self.start_frame, text="(Expectiminimax) إنسان ضد كمبيوتر", width=25, height=2,
                  font=("Arial", 10, "bold"), bg="#e67e22", fg="white", command=lambda: self.start_game(2)).pack(pady=5)

    def start_game(self, mode):
        self.game_mode = mode
        self.start_frame.destroy()
        self.setup_ui()
        self.update_board_display()

    # الواجهة الرئيسية
    def setup_ui(self):
        self.board_frame = tk.Frame(
            self.root, bg="#d2b48c", padx=15, pady=15, relief="sunken", borderwidth=5)
        self.board_frame.pack(pady=10)

        # SENET_PATH بناء الخلايا بناءً على المسار
        for r_idx, row_ids in enumerate(SENET_PATH):
            for c_idx, cell_id in enumerate(row_ids):
                btn = tk.Button(self.board_frame, text="", width=10, height=4,
                                command=lambda cid=cell_id: self.on_cell_click(
                                    cid),
                                font=("Arial", 8, "bold"), relief="raised")
                btn.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                self.buttons[cell_id] = btn

        # الازرار
        self.controls = tk.Frame(self.root, pady=10)
        self.controls.pack()

        self.info_label = tk.Label(self.controls, text=f"{self.board_logic.current_player} :الدور الان",
                                   font=("Arial", 12, "bold"))
        self.info_label.pack()

        self.dice_label = tk.Label(
            self.controls, text=" -- :قيمة الرمية", font=("Arial", 14, "bold"), fg="#2c3e50")
        self.dice_label.pack(pady=5)

        self.roll_btn = tk.Button(self.controls, text="رمي العصي", command=self.roll_dice,
                                  bg="#27ae60", fg="white", width=20, font=("Arial", 10, "bold"))
        self.roll_btn.pack(pady=5)

    def roll_dice(self):
        if self.board_logic.turn_state != "wait_dice":
            return

        steps = self.board_logic.roll_dice()
        if steps:
            self.dice_label.config(text=f"{steps} قيمة الرمية")
            movable = self.board_logic.get_movable_pawns(steps)

            if not movable:
                messagebox.showinfo(
                    "تجاوز الدور", f"ليس لديه حركات، سيتم تخطي الدور {self.board_logic.current_player} اللاعب")
                self.board_logic.switch_player()
                self.board_logic.turn_state = "wait_dice"
                self.update_board_display()
                self.check_ai_turn()  # التحقق إذا كان دور الكمبيوتر تالياً
            else:
                self.update_board_display()
                # إذا كان دور الكمبيوتر، يلعب تلقائياً
                if self.game_mode == 2 and self.board_logic.current_player == self.ai_engine.ai_color:
                    self.root.after(1000, self.ai_move)

    def on_cell_click(self, cell_id):
        # منع المستخدم من اللعب في دور الكمبيوتر
        if self.game_mode == 2 and self.board_logic.current_player == self.ai_engine.ai_color:
            return

        if self.board_logic.turn_state != "wait_move":
            return

        cell = self.board_logic.get_cell(cell_id)
        if cell.occupied_by and cell.occupied_by.color == self.board_logic.current_player:
            pawn_id = cell.occupied_by.id
            success = self.board_logic.handle_movement(
                pawn_id, self.board_logic.current_dice)
            if success:
                self.post_move_actions()
            else:
                messagebox.showwarning("تنبيه", "حركة غير قانونية")
        else:
            messagebox.showwarning("تنبيه", "اختر حجراً يخصك")

    def ai_move(self):
        # الحصول على قيمة الرمية الحالية وحالة اللعبة
        steps = self.board_logic.current_dice
        state = GameState(self.board_logic, self.board_logic.current_player)

        # تخزين العقد وطريقة الاختيار بملف
        try:
            with open(self.ai_engine.log_file, "w", encoding="utf-8") as f:
                f.write(
                    f"--- AI Decision Logic | Current Player: {self.board_logic.current_player} ---\n")
                f.write(f"--- Dice Roll Result: {steps} ---\n\n")
        except Exception as e:
            print(f"Error opening log file: {e}")

        # تصفير عداد العقد قبل كل عملية بحث
        self.ai_engine.nodes_count = 0

        score, best_pawn_id = self.ai_engine.expectiminimax(
            state,
            self.ai_engine.max_depth,
            False,
            steps,
            ""
        )

        if best_pawn_id is None:
            movable = self.board_logic.get_movable_pawns(steps)
            if movable:
                best_pawn_id = movable[0]

        #  طباعة ملخص النتائج بنهاية الملف
        try:
            with open(self.ai_engine.log_file, "a", encoding="utf-8") as f:
                f.write("\n" + "="*40 + "\n")
                f.write(f"FINAL DECISION SUMMARY:\n")
                f.write(
                    f"Total Nodes Explored (Search Space): {self.ai_engine.nodes_count}\n")
                f.write(f"Heuristic Value for Chosen Move: {score}\n")
                f.write(f"Action Taken: Moved Pawn ID {best_pawn_id}\n")
                f.write("="*40 + "\n")
        except Exception as e:
            print(f"Error writing summary to log: {e}")

        if best_pawn_id is not None:
            self.board_logic.handle_movement(best_pawn_id, steps)

        # تحديث الواجهة والتحقق من انتهاء اللعبة أو تبديل الدور
        self.post_move_actions()

    def post_move_actions(self):
        # تحديث الواجهة والتحقق من نهاية اللعبة بعد كل حركة
        self.update_board_display()
        if self.board_logic.is_game_over():
            messagebox.showinfo(
                "نهاية اللعبة", f"مبروك! الفائز هو: {self.board_logic.get_winner()}")
            self.root.destroy()
            return

        self.check_ai_turn()

    def check_ai_turn(self):
        # الكمبيوتر يرمي العصا بعد 800 مل ثانية
        if self.game_mode == 2 and self.board_logic.current_player == self.ai_engine.ai_color:
            self.root.after(800, self.roll_dice)

    def update_board_display(self):
        for cell_id, btn in self.buttons.items():
            cell = self.board_logic.get_cell(cell_id)

            # تلوين المربعات الخاصة
            if cell_id in SPECIAL_SYMBOLS:
                btn.config(
                    bg="#f1c40f", text=f"{cell_id}\n{SPECIAL_SYMBOLS[cell_id]}")
            else:
                btn.config(bg="#ecf0f1", text=str(cell_id))

            # إظهار الأحجار (الأسود والأبيض)
            if cell.occupied_by:
                p = cell.occupied_by
                bg_color = "#2c3e50" if p.color == "BLACK" else "#bdc3c7"
                fg_color = "white" if p.color == "BLACK" else "black"
                btn.config(
                    text=f"{p.color[0]}\nID:{p.id}", bg=bg_color, fg=fg_color)

        self.info_label.config(
            text=f"{self.board_logic.current_player} :الدور الان")


if __name__ == "__main__":
    root = tk.Tk()
    # تعيين حجم النافذة وموقعها
    root.geometry("900x500")
    app = SenetGUI(root)
    root.mainloop()
