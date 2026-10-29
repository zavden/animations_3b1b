# ==============================================================================
# Scene:      WillNotAnswer
# Source:     videos/_2024/puzzles/supplements.py (lines 387-418)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WillNotAnswer.py WillNotAnswer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WillNotAnswer(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        self.play(LaggedStart(
            morty.says("I won't give\nyou the answer"),
            self.change_students("angry", "erm", "sassy"),
            lag_ratio=0.5
        ))
        self.wait(3)

        # Spoiler
        det_expr = Tex(R"""
            \text{det}\left(\left[
            \begin{array}{cccc}
            \cdot & \cdot & \cdot & \cdot \\
            \cdot & \cdot & \cdot & \cdot \\
            \cdot & \cdot & \cdot & \cdot \\
            \cdot & \cdot & \cdot & \cdot \\
            \end{array}
            \right]\right)
        """)
        det_expr.next_to(self.hold_up_spot, UP)

        self.play(
            FadeIn(det_expr, UP),
            morty.debubble(mode="raise_right_hand", look_at=det_expr),
            self.change_students("pondering", "pondering", "pondering", look_at=det_expr),
        )
        self.wait(4)
