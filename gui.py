import tkinter as tk
from tkinter import messagebox
from Board import Board, SENET_PATH, SPECIAL_SYMBOLS

class SenetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(" Senet  ")
        self.board_logic = Board()
        self.buttons = {}
        
        # إنشاء العناصر الرسومية
        self.setup_ui()
        self.update_board_display()

    def setup_ui(self):
        # إطار الرقعة
        self.board_frame = tk.Frame(self.root, bg="#d2b48c", padx=10, pady=10)
        self.board_frame.pack()

        # إنشاء الأزرار بناءً على المسار المتعرج الموجود في كودك
        for r_idx, row_ids in enumerate(SENET_PATH):
            for c_idx, cell_id in enumerate(row_ids):
                btn = tk.Button(self.board_frame, text="", width=6, height=3,
                               command=lambda cid=cell_id: self.on_cell_click(cid),
                               font=("Arial", 10, "bold"))
                btn.grid(row=r_idx, column=c_idx, padx=2, pady=2)
                self.buttons[cell_id] = btn

        # منطقة التحكم
        self.controls = tk.Frame(self.root, pady=20)
        self.controls.pack()

        self.info_label = tk.Label(self.controls, text=f"الدور الآن: {self.board_logic.current_player}", font=("Arial", 12))
        self.info_label.pack()

        self.dice_label = tk.Label(self.controls, text="قيمة الرمية: --", font=("Arial", 14, "bold"), fg="blue")
        self.dice_label.pack()

        self.roll_btn = tk.Button(self.controls, text="رمي العصي", command=self.roll_dice, bg="#4CAF50", fg="white")
        self.roll_btn.pack(pady=5)

    def roll_dice(self):
        # استخدام تابع roll_dice  jkk 
        steps = self.board_logic.roll_dice()
        if steps:
            self.dice_label.config(text=f"قيمة الرمية: {steps}")
            movable = self.board_logic.get_movable_pawns(steps)
            if not movable:
                messagebox.showinfo("تنبيه", "لا توجد حركات ممكنة، تم نقل الدور.")
                self.board_logic.switch_player()
                self.board_logic.turn_state = "wait_dice"
                self.update_board_display()
        self.update_board_display()

    def on_cell_click(self, cell_id):
        if self.board_logic.turn_state != "wait_move":
            return

        # البحث عن الحجر الموجود في هذه الخلية
        cell = self.board_logic.get_cell(cell_id)
        if cell.occupied_by:
            pawn_id = cell.occupied_by.id
            # تنفيذ الحركة باستخدام  handle_movement  
            success = self.board_logic.handle_movement(pawn_id, self.board_logic.current_dice)
            if success:
                if self.board_logic.is_game_over():
                    messagebox.showinfo("مبروك", f"الفائز هو: {self.board_logic.get_winner()}")
                    self.root.quit()
                self.update_board_display()
            else:
                messagebox.showwarning("حركة غير مسموحة", "لا يمكن تحريك هذا الحجر!")

    def update_board_display(self):
        # تحديث ألوان وأشكال الخلايا
        for cell_id, btn in self.buttons.items():
            cell = self.board_logic.get_cell(cell_id)
            
            # تمييز المربعات الخاصة بالألوان حسب القواعد [cite: 36, 39, 42, 44, 45, 48]
            if cell_id in SPECIAL_SYMBOLS:
                btn.config(bg="#ffeb3b", text=SPECIAL_SYMBOLS[cell_id]) # لون أصفر للمربعات الخاصة
            else:
                btn.config(bg="white", text=str(cell_id))

            # إظهار الأحجار
            if cell.occupied_by:
                color_name = "Black" if cell.occupied_by.color == "BLACK" else "White"
                p_id = cell.occupied_by.id
                btn.config(text=f"{color_name}\n({p_id})", bg="#90aead" if color_name=="White" else "#4e4e4e", fg="white")
        
        self.info_label.config(text=f"الدور الآن: {self.board_logic.current_player}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SenetGUI(root)
    root.mainloop()