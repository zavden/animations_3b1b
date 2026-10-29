# ==============================================================================
# Scene:      WriteWhiteLightReflectionHologram
# Source:     videos/_2024/holograms/supplements.py (lines 70-76)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteWhiteLightReflectionHologram.py WriteWhiteLightReflectionHologram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteWhiteLightReflectionHologram(InteractiveScene):
    def construct(self):
        # Test
        title = Text("White Light Reflection Hologram", font_size=72)
        title.to_edge(UP)
        self.play(Write(title, stroke_color=WHITE, stroke_width=3, lag_ratio=0.1, run_time=3))
        self.wait()
