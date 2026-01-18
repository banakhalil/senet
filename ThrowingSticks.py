import random

# هاد التابع رح تستخدمو خوارزمية الذكاء وقت بدا تحسب احتمالات الرمية
# يستخدم في عقدة الحظ


def stick_throw_probabilities():
    probabilities = {
        1: 4/16,
        2: 6/16,
        3: 4/16,
        4: 1/16,
        5: 1/16
    }
    return probabilities


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
