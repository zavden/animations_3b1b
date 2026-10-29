# ==============================================================================
# Scene:      StatsToVenus
# Source:     videos/_2025/cosmic_distance/part2.py (lines 9-21)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StatsToVenus.py StatsToVenus -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StatsToVenus(InteractiveScene):
    def construct(self):
        # Test
        title = TexText(R"Nearest distance to Venus $\approx$ 39,000,000 km $\approx 6{,}200 \times R_E$")
        title.to_edge(UP)
        title.set_backstroke(BLACK, 3)

        self.play(Write(title["Nearest distance to Venus "]))
        self.wait()
        self.play(Write(title[R"$\approx$ 39,000,000 km"]))
        self.wait()
        self.play(Write(title[R"$\approx 6{,}200 \times R_E$"]))
        self.wait()
