# ==============================================================================
# Scene:      IsntThatObvious
# Source:     videos/_2021/shadows.py (lines 2192-2214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IsntThatObvious.py IsntThatObvious -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IsntThatObvious(TeacherStudentsScene):
    def construct(self):
        self.remove(self.background)
        self.student_says(
            OldTexText("Isn't that obvious?"),
            bubble_config={
                "height": 3,
                "width": 4,
                "direction": LEFT,
            },
            target_mode="angry",
            look_at=self.screen,
            added_anims=[LaggedStart(
                self.teacher.change("guilty"),
                self.students[0].change("pondering", self.screen),
                self.students[1].change("erm", self.screen),
            )]
        )
        self.wait(2)
        self.play(
            self.students[0].change("hesitant"),
        )
        self.wait(2)
