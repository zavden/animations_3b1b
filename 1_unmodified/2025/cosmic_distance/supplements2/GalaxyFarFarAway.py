# ==============================================================================
# Scene:      GalaxyFarFarAway
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 1284-1293)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GalaxyFarFarAway.py GalaxyFarFarAway -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GalaxyFarFarAway(InteractiveScene):
    def construct(self):
        # Test
        words = Text("A Galaxy Far\n Far Away", font_size=120)
        words.set_color(YELLOW)
        words.set_backstroke(BLACK, 5)
        self.add(words)

        self.frame.reorient(0, 60, 0)
        self.play(words.animate.shift(20 * UP), run_time=5)
