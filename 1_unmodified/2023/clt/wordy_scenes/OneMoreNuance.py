# ==============================================================================
# Scene:      OneMoreNuance
# Source:     videos/_2023/clt/wordy_scenes.py (lines 793-804)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneMoreNuance.py OneMoreNuance -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OneMoreNuance(InteractiveScene):
    def construct(self):
        morty = Mortimer()
        morty.to_edge(DOWN)

        self.play(morty.says("One more\nquick nuance", mode="speaking"))
        self.play(Blink(morty))
        self.play(morty.change("tease", look_at=BOTTOM))
        self.wait()
        for x in range(2):
            self.play(Blink(morty))
            self.wait()
