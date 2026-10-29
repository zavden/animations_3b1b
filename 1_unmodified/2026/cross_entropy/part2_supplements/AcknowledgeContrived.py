# ==============================================================================
# Scene:      AcknowledgeContrived
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 42-48)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AcknowledgeContrived.py AcknowledgeContrived -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AcknowledgeContrived(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer().flip()
        self.play(morty.says("Contrived? Yes. \n But bear with me..."))
        self.play(morty.change("shruggie"))
        self.wait()
