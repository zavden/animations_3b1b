# ==============================================================================
# Scene:      NotAsUnique
# Source:     videos/_2022/some2/winners.py (lines 1208-1214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotAsUnique.py NotAsUnique -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotAsUnique(TeacherStudentsScene):
    def construct(self):
        self.play(
            self.teacher.says("It's not as\nunique these days", mode="shruggie"),
            self.change_students("happy", "tease", "happy")
        )
        self.wait(3)
