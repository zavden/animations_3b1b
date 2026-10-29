# ==============================================================================
# Scene:      GoalOfRediscovery
# Source:     videos/_2021/quick_eigen.py (lines 304-322)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GoalOfRediscovery.py GoalOfRediscovery -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GoalOfRediscovery(TeacherStudentsScene):
    def construct(self):
        self.play(
            PiCreatureSays(self.teacher, OldTexText("The goal is\\\\rediscovery")),
            self.change_students(
                "happy", "tease", "hooray",
                run_time=1.5,
            )
        )
        self.wait(2)

        recap_words = Text("Quick recap")
        recap_words.move_to(self.screen, UP)
        self.play(
            RemovePiCreatureBubble(self.teacher, target_mode="raise_right_hand", look_at=recap_words),
            self.change_students("pondering", "hesitant", "pondering", look_at=recap_words),
            GrowFromPoint(recap_words, self.teacher.get_corner(UL)),
        )
        self.wait(4)
