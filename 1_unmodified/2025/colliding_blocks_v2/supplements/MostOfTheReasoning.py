# ==============================================================================
# Scene:      MostOfTheReasoning
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 594-601)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MostOfTheReasoning.py MostOfTheReasoning -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MostOfTheReasoning(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer(height=2.5).flip()
        morty.to_corner(DL)
        self.play(morty.says("This is most of\nthe physics"))
        self.play(Blink(morty))
        self.wait(2)
