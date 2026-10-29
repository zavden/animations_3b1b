# ==============================================================================
# Scene:      NotQuiteRight
# Source:     videos/_2021/shadows.py (lines 1578-1592)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotQuiteRight.py NotQuiteRight -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotQuiteRight(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.teacher_says(
            "Not quite right...",
            target_mode="hesitant",
            bubble_config={"height": 3, "width": 4},
            added_anims=[
                self.change_students(
                    "pondering", "thinking", "erm",
                    look_at=self.screen,
                )
            ]
        )
        self.wait(4)
