# ==============================================================================
# Scene:      ShowDerivativeVideo
# Source:     videos/_2019/diffyq/part1/staging.py (lines 1242-1266)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowDerivativeVideo.py ShowDerivativeVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowDerivativeVideo(Scene):
    def construct(self):
        title = OldTexText("Essence of", "Calculus")
        title.scale(1.5)
        title.to_edge(UP)

        title2 = OldTexText("Essence of", "Linear Algebra")
        title2.scale(1.5)
        title2.move_to(title, DOWN)

        rect = ScreenRectangle(height=6)
        rect = rect.copy()
        rect.set_style(
            fill_opacity=1,
            fill_color=BLACK,
            stroke_width=0,
        )
        rect.next_to(title, DOWN)
        animated_rect = AnimatedBoundary(rect)

        self.add(title, rect)
        self.add(animated_rect)
        self.wait(5)
        self.play(ReplacementTransform(title, title2))
        self.wait(10)
