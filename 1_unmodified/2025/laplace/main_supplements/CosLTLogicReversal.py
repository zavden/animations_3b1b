# ==============================================================================
# Scene:      CosLTLogicReversal
# Source:     videos/_2025/laplace/main_supplements.py (lines 734-749)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CosLTLogicReversal.py CosLTLogicReversal -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CosLTLogicReversal(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle().set_fill(GREY_E, 0.5))
        arrow = Tex(R"\rightarrow", font_size=120)
        cos_lt = Tex(
            R"\frac{s}{s^2 + \omega^2}",
            font_size=90,
            t2c={"s": YELLOW, R"\omega": PINK}
        )
        cos_lt.next_to(arrow, RIGHT, LARGE_BUFF)

        self.add(arrow, cos_lt)
        self.wait()
        self.play(cos_lt.animate.next_to(arrow, LEFT, LARGE_BUFF).set_anim_args(path_arc=120 * DEG), run_time=3)
        self.wait()
