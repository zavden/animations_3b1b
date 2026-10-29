# ==============================================================================
# Scene:      SteveMouldMention
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 1016-1028)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SteveMouldMention.py SteveMouldMention -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SteveMouldMention(InteractiveScene):
    def construct(self):
        morty = Mortimer(height=2)
        morty.to_edge(DOWN)
        self.play(
            morty.says("""
                This is the part that
                Steve Mould explains
                quite well, by the way
            """, mode="tease")
        )
        self.play(Blink(morty))
        self.wait()
