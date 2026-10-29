# ==============================================================================
# Scene:      PiCreatureReactions
# Source:     videos/_2026/2025_P6/p6.py (lines 3696-3719)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiCreatureReactions.py PiCreatureReactions -w -m --fps 15
# ==============================================================================

import tempfile
import os
from manim_imports_ext import *

class PiCreatureReactions(InteractiveScene):
    def construct(self):
        # Add a pi creature
        randy = Randolph(flip_at_start=True)
        self.add(randy)
        self.play(FadeIn(randy, shift=LEFT))

        # React to things
        self.play(randy.change("hooray"), run_time=1)
        self.wait(2)
        self.play(Blink(randy))
        self.wait(4)
        self.play(Blink(randy))
        self.wait(2)
        self.play(randy.change("confused", UP * 4 + LEFT))
        self.wait(1)
        self.play(Blink(randy))
        self.wait(1)
        self.play(randy.change("pondering", LEFT * 3))
        self.wait(2)
        self.play(randy.change("thinking", LEFT * 3))
        self.wait(1)
        self.play(Blink(randy))
        self.wait(3)


_desaturate_cache_dir = os.path.join(tempfile.gettempdir(), "manim_desaturate_cache")


os.makedirs(_desaturate_cache_dir, exist_ok=True)
