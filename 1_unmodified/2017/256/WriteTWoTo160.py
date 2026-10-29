# ==============================================================================
# Scene:      WriteTWoTo160
# Source:     videos/_2017/256.py (lines 652-658)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteTWoTo160.py WriteTWoTo160 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteTWoTo160(Scene):
    def construct(self):
        mob = OldTexText("$2^{160}$ ", "Hashes/sec")
        mob[0].set_color(BLUE)
        mob.scale(2)
        self.play(Write(mob))
        self.wait()
