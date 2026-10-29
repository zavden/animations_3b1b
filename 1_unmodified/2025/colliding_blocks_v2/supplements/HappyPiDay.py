# ==============================================================================
# Scene:      HappyPiDay
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 127-145)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HappyPiDay.py HappyPiDay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HappyPiDay(TeacherStudentsScene):
    def construct(self):
        # Test
        title = Text("Happy Pi Day!", font_size=72)
        title.to_edge(UP)
        morty = self.teacher
        morty.change_mode("surprised")

        self.play(
            Write(title),
            morty.change("hooray", look_at=title),
            self.change_students("hooray", "surprised", "jamming", look_at=title)
        )
        self.wait()
        self.play(
            morty.change("tease", 2 * UP),
            self.change_students("tease", "surprised", "well", look_at=3 * UR)
        )
        self.wait(4)
