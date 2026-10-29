# ==============================================================================
# Scene:      LetsHaveFun
# Source:     videos/_2023/clt/wordy_scenes.py (lines 807-815)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LetsHaveFun.py LetsHaveFun -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LetsHaveFun(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.to_edge(DOWN)

        self.play(morty.says("Let's have\nsome fun", mode="hooray", look_at=BOTTOM))
        for x in range(2):
            self.play(Blink(morty))
            self.wait()
