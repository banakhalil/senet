import random

class ThrowingSticks:
    def __init__(self):
        self.sticks_count = 4


    def _throw_one_stick(self):
        return "BLACK" if random.random() < 0.5 else "WHITE"
    

    def throw_sticks(self):
        dark_faces = 0

        for stick in range(self.sticks_count):
            if self._throw_one_stick() == "BLACK":
                dark_faces += 1

        if dark_faces == 0:
            return 5
        else:
            return dark_faces

    
# steps_num هاي القيمة يلي رح ناخدها بتوابع الحركة 
steps_num = ThrowingSticks().throw_sticks()

print("number of steps", steps_num)
