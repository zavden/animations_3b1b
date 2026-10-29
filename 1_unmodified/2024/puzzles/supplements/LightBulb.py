# ==============================================================================
# Scene:      LightBulb
# Source:     videos/_2024/puzzles/supplements.py (lines 891-912)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LightBulb.py LightBulb -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LightBulb(InteractiveScene):
    def construct(self):
        # Add bulb
        bulb = SVGMobject("light_bulb")
        bulb.set_fill(YELLOW, 0.1)
        bulb.set_height(3)
        fancy_bulb = VGroup()
        for part in bulb:
            for x in range(20):
                fancy_bulb.add(part.copy())
                part.scale(0.97)

        self.add(fancy_bulb)

        # Light
        N = 300
        radiation = VGroup(
            Circle(radius=interpolate(0.5, 10, a)).set_stroke(YELLOW, 2, interpolate(0.5, 0.2, a))
            for a in np.linspace(0, 1, N)
        )

        self.play(LaggedStartMap(VFadeInThenOut, radiation, lag_ratio=1.0 / N, run_time=5))
