# ==============================================================================
# Scene:      HighlightTheSlope
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 562-591)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HighlightTheSlope.py HighlightTheSlope -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HighlightTheSlope(TeacherStudentsScene):
    def construct(self):
        # Test
        slope = Tex(R"-\sqrt{m_1 \over m_2}", t2c={"m_1": BLUE, "m_2": BLUE}, font_size=60)
        slope.next_to(self.hold_up_spot, UP)
        rect = SurroundingRectangle(slope)

        sqrt_highlight = slope[R"\sqrt"][0].copy()
        sqrt_highlight.set_stroke(YELLOW, 4).set_fill(opacity=0)
        sqrt_highlight.insert_n_curves(100)

        self.play(
            self.teacher.change("raise_right_hand", slope),
            self.change_students("erm", "sassy", "well", look_at=slope),
            FadeIn(slope, UP),
        )
        self.wait()
        self.play(
            FlashAround(slope),
            ShowCreation(rect),
            self.change_students("pondering", "pondering", "thinking", look_at=slope)
        )
        self.wait()

        self.remove(rect)
        rect_copy = rect.replicate(2)
        self.play(Transform(rect_copy, sqrt_highlight))
        self.wait()
        self.play(FadeOut(rect_copy))
        self.wait(4)
