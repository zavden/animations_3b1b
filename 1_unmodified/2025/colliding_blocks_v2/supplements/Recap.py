# ==============================================================================
# Scene:      Recap
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 182-187)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Recap.py Recap -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Recap(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer()
        self.play(morty.says(TexText("Let's Recap"), look_at=DL))
        self.wait()
