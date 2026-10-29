# ==============================================================================
# Scene:      CrossAndCheck
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 996-1013)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CrossAndCheck.py CrossAndCheck -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CrossAndCheck(InteractiveScene):
    def construct(self):
        # Test
        cross = Cross(Square())
        cross.set_shape(4, 3)
        cross.to_edge(LEFT)
        cross.set_stroke(RED, (0, 10, 10, 10, 0))

        checkmark = Checkmark()
        checkmark.set_height(1)
        checkmark.set_fill(GREEN)
        checkmark.next_to(cross, UP)

        self.play(ShowCreation(cross))
        self.wait()
        self.play(FadeOut(cross))
        self.play(FadeIn(checkmark, UP))
        self.wait()
