# ==============================================================================
# Scene:      Question2
# Source:     videos/_2018/sphere_area.py (lines 3363-3377)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Question2.py Question2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Question2(Scene):
    def construct(self):
        question = OldTexText(
            """
            Question \\#2: What is the area of the shadow of\\\\
            one of these rings?  (In terms of $R$, $\\theta$, and $d\\theta$).
            """,
            tex_to_color_map={
                "shadow": YELLOW,
            }
        )
        question.set_width(FRAME_WIDTH - 1)

        self.play(FadeInFromDown(question))
        self.wait()
