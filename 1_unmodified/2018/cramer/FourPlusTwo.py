# ==============================================================================
# Scene:      FourPlusTwo
# Source:     videos/_2018/cramer.py (lines 2162-2178)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FourPlusTwo.py FourPlusTwo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FourPlusTwo(Scene):
    def construct(self):
        p1 = OldTex("(4)(1)")
        p2 = OldTex("-(-1)(2)")
        p2.next_to(p1, RIGHT, SMALL_BUFF)
        b1 = Brace(p1, UP)
        b2 = Brace(p2, UP)
        t1 = b1.get_tex("4", buff=SMALL_BUFF)
        t2 = b2.get_tex("+2", buff=SMALL_BUFF)

        for b, t in (b1, t1), (b2, t2):
            t.set_stroke(BLACK, 3, background=True)
            self.play(
                GrowFromCenter(b),
                Write(t)
            )
        self.wait()
