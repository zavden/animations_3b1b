# ==============================================================================
# Scene:      UseDefiningFeatures
# Source:     videos/_2018/dandelin.py (lines 963-982)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UseDefiningFeatures.py UseDefiningFeatures -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UseDefiningFeatures(Scene):
    def construct(self):
        title = OldTexText("Problem-solving tip:")
        title.scale(1.5)
        title.to_edge(UP)
        tip = OldTexText(
            """
            - Make sure you're using all the \\\\
            \\phantom{-} defining features of the objects \\\\
            \\phantom{-} involved.
            """,
            alignment=""
        )
        tip.next_to(title, DOWN, MED_LARGE_BUFF)
        tip.shift(MED_SMALL_BUFF * RIGHT)
        tip.set_color(YELLOW)

        self.add(title)
        self.play(Write(tip, run_time=4))
        self.wait()
