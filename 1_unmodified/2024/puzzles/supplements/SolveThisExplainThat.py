# ==============================================================================
# Scene:      SolveThisExplainThat
# Source:     videos/_2024/puzzles/supplements.py (lines 443-464)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SolveThisExplainThat.py SolveThisExplainThat -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SolveThisExplainThat(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = Rectangle(4, 3).replicate(2)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 2)
        screens.set_height(4.5)
        screens.arrange(RIGHT, buff=1)
        screens.move_to(0.5 * DOWN)

        titles = VGroup(
            Text("Solving this..."),
            Text("...explains this"),
        )
        for title, screen in zip(titles, screens):
            title.next_to(screen, UP)

        self.add(screens)
        self.play(Write(titles[0]))
        self.wait()
        self.play(TransformMatchingStrings(titles[0].copy(), titles[1], path_arc=-45 * DEGREES))
        self.wait()
