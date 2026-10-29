# ==============================================================================
# Scene:      AndGate
# Source:     videos/_2024/transformers/supplements.py (lines 1726-1738)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AndGate.py AndGate -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AndGate(InteractiveScene):
    def construct(self):
        # Test
        gate = SVGMobject("and_gate")
        gate.set_fill(WHITE).set_stroke(width=0)
        name = Text("AND\nGate", font_size=96, alignment="LEFT")
        name.next_to(gate, RIGHT, LARGE_BUFF)
        self.play(
            Write(gate),
            FadeIn(name, lag_ratio=0.1, time_span=(0, 2)),
            run_time=3
        )
        self.wait()
