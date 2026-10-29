# ==============================================================================
# Scene:      CausalInfluence
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1523-1540)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CausalInfluence.py CausalInfluence -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CausalInfluence(InteractiveScene):
    def construct(self):
        words = TexText(R"No causal influence can \\ propagate faster than $c$", font_size=72)
        c = words["$c$"]
        c.set_color(YELLOW)
        rect = SurroundingRectangle(c)
        arrow = Vector(UP)
        arrow.set_color(YELLOW)
        arrow.next_to(rect, DOWN)

        self.add(words)
        self.wait()
        self.play(
            GrowArrow(arrow),
            ShowCreation(rect),
            FlashAround(c),
        )
        self.wait()
