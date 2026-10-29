# ==============================================================================
# Scene:      CosineEqualsWhat
# Source:     videos/_2025/laplace/main_supplements.py (lines 752-762)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CosineEqualsWhat.py CosineEqualsWhat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CosineEqualsWhat(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle().set_fill(GREY_E, 0.5))
        cos = Tex(R"\cos(t) = ???", font_size=90, t2c={"t": BLUE})
        q_marks = cos["???"][0]
        q_marks.scale(1.2, about_edge=UL)
        q_marks.space_out_submobjects(1.1)
        q_marks.shift(MED_SMALL_BUFF * RIGHT)
        self.add(cos)
        self.play(Write(q_marks))
        self.wait()
