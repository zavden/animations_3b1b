# ==============================================================================
# Scene:      ZetaSum
# Source:     videos/outside_videos/analysis.py (lines 146-175)
# Category:   1 · Renders unmodified
# Includes code copied from: _2016/zeta.py
#
# Run from this folder:
#     manimgl ZetaSum.py ZetaSum -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import mpmath


# ----- From _2016/zeta.py -----

mpmath.mp.dps = 7



# ----- From outside_videos/analysis.py -----

class ZetaSum(Scene):
    def construct(self):
        plane = ComplexPlane()
        self.add(plane)
        plane.scale(0.2)

        s = complex(0.5, 14.135)
        N = int(1e6)
        lines = VGroup()
        color = it.cycle([BLUE, RED])
        r = int(1e3)
        for k in range(1, N + 1, r):
            c = sum([
                L**(-s) * (N - L + 1) / N
                for L in range(k, k + r)
            ])
            line = Line(plane.n2p(0), plane.n2p(c))
            line.set_color(next(color))
            if len(lines) > 0:
                line.shift(lines[-1].get_end())
            lines.add(line)

        self.add(lines)
        self.add(
            Dot(lines[-1].get_end(), color=YELLOW),
            Dot(
                center_of_mass([line.get_end() for line in lines]),
                color=YELLOW
            ),
        )
