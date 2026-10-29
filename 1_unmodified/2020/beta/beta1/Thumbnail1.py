# ==============================================================================
# Scene:      Thumbnail1
# Source:     videos/_2020/beta/beta1.py (lines 17-38)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail1.py Thumbnail1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail1(Scene):
    def construct(self):
        p1 = "$96\\%$"
        p2 = "$93\\%$"
        n1 = "50"
        n2 = "200"
        t2c = {
            p1: BLUE,
            p2: YELLOW,
            n1: BLUE_C,
            n2: YELLOW,
        }
        kw = {"tex_to_color_map": t2c}
        text = VGroup(
            OldTexText(f"{p1} with {n1} reviews", **kw),
            OldTexText("vs.", **kw),
            OldTexText(f"{p2} with {n2} reviews", **kw),
        )
        text.scale(2)
        text.arrange(DOWN, buff=LARGE_BUFF)
        text.set_width(FRAME_WIDTH - 1)
        self.add(text)
