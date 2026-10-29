# ==============================================================================
# Scene:      WriteTransmissionHologram
# Source:     videos/_2024/holograms/supplements.py (lines 61-67)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteTransmissionHologram.py WriteTransmissionHologram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteTransmissionHologram(InteractiveScene):
    def construct(self):
        # Test
        title = Text("Transmission Hologram", font_size=96)
        title.to_edge(UP)
        self.play(Write(title, stroke_color=GREEN_SCREEN, stroke_width=3, lag_ratio=0.1, run_time=3))
        self.wait()
