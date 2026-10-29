# ==============================================================================
# Scene:      Seeking4DAnalog
# Source:     videos/_2024/puzzles/supplements.py (lines 521-546)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Seeking4DAnalog.py Seeking4DAnalog -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Seeking4DAnalog(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenRectangle())
        screens = Rectangle(4, 3).replicate(2)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 2)
        screens.set_height(4.5)
        screens.arrange(RIGHT, buff=1)
        screens.move_to(0.5 * DOWN)

        titles = VGroup(
            TexText(R"2d tiling \\ $\downarrow$ \\ 3d cube stack"),
            TexText(R"3d tiling \\ $\downarrow$ \\ 4d hypercube stack"),
        )
        for title, screen in zip(titles, screens):
            title.next_to(screen, UP)

        self.add(screens)
        self.play(Write(titles[0]))
        self.wait()
        self.play(TransformMatchingStrings(
            titles[0].copy(), titles[1],
            key_map={"2d": "3d", "3d": "4d"}
        ))
        self.wait()
