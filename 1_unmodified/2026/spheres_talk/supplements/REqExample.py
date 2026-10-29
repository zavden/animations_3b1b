# ==============================================================================
# Scene:      REqExample
# Source:     videos/_2026/spheres_talk/supplements.py (lines 210-214)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl REqExample.py REqExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class REqExample(InteractiveScene):
    def construct(self):
        # Test
        tex = Tex(R"r = \sqrt{10} - 1 \approx 2.162")
        self.add(tex)
