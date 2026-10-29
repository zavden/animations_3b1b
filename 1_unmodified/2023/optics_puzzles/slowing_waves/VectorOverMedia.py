# ==============================================================================
# Scene:      VectorOverMedia
# Source:     videos/_2023/optics_puzzles/slowing_waves.py (lines 131-147)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VectorOverMedia.py VectorOverMedia -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class VectorOverMedia(InteractiveScene):
    def construct(self):
        vect = Vector(DOWN)
        vect.next_to(UP, UP)
        vect.to_edge(LEFT, buff=0)

        def update_vect(v, dt):
            # speed = 1.5 if v.get_x() < 0 else 1.0
            speed = 1.33 if v.get_x() < 0 else 1.33 / 1.5
            v.shift(dt * RIGHT * speed)

        vect.add_updater(update_vect)
        word = Text("Phase velocity")
        word.add_updater(lambda m: m.next_to(vect, UP))
        self.add(vect)
        self.add(word)
        self.wait(13)
