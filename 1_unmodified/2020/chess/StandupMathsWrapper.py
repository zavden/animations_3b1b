# ==============================================================================
# Scene:      StandupMathsWrapper
# Source:     videos/_2020/chess.py (lines 968-990)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StandupMathsWrapper.py StandupMathsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StandupMathsWrapper(Scene):
    CONFIG = {
        "title": "Solution on Stand-up Maths"
    }

    def construct(self):
        fsr = FullScreenFadeRectangle()
        fsr.set_fill(GREY_E, 1)
        self.add(fsr)

        title = OldTexText(self.title)
        title.scale(1.5)
        title.to_edge(UP)

        rect = ScreenRectangle(height=6)
        rect.set_stroke(WHITE, 2)
        rect.set_fill(BLACK, 1)
        rect.next_to(title, DOWN)
        rb = AnimatedBoundary(rect)

        self.add(rect, rb)
        self.play(Write(title))
        self.wait(30)
