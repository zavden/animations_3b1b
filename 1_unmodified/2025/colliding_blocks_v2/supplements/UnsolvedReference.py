# ==============================================================================
# Scene:      UnsolvedReference
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 170-179)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnsolvedReference.py UnsolvedReference -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnsolvedReference(InteractiveScene):
    def construct(self):
        rect = Rectangle(8, 1.25)
        rect.set_stroke(RED, 4)
        label = Text("Unsolved", font_size=60)
        label.set_color(RED)
        label.next_to(rect, UP, buff=MED_SMALL_BUFF)

        self.play(ShowCreation(rect), FadeIn(label, 0.25 * UP))
        self.wait()
