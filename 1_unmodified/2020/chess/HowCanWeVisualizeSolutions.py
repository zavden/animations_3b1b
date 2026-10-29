# ==============================================================================
# Scene:      HowCanWeVisualizeSolutions
# Source:     videos/_2020/chess.py (lines 1051-1065)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HowCanWeVisualizeSolutions.py HowCanWeVisualizeSolutions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HowCanWeVisualizeSolutions(TeacherStudentsScene):
    def construct(self):
        self.teacher_says(
            "How can we\\\\visualize solutions",
            bubble_config={
                "height": 3,
                "width": 4,
                "fill_opacity": 0,
            },
            added_anims=[self.change_students("pondering", "thinking", "pondering")]
        )
        self.look_at(self.screen),
        self.wait(1)
        self.play_student_changes("thinking", "erm", "confused")
        self.wait(5)
