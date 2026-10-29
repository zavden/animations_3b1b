# ==============================================================================
# Scene:      LookAround
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1503-1520)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookAround.py LookAround -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LookAround(InteractiveScene):
    def construct(self):
        # Test
        circle = Circle(radius=2)
        circle.stretch(1.5, 0)
        arrows = VGroup(*(
            Arrow(v, 2 * v, buff=0, stroke_width=8, stroke_color=GREY_B)
            for alpha in np.arange(0, 1, 1 / 12)
            for v in [circle.pfp(alpha)]
        ))
        words1 = Text("Look\naround", font_size=90)
        words2 = Text("Most things\nare opaque", font_size=72)

        self.add(words1)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.2))
        self.wait()
        self.play(FadeTransform(words1, words2))
        self.wait()
