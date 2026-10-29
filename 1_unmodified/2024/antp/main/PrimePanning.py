# ==============================================================================
# Scene:      PrimePanning
# Source:     videos/_2024/antp/main.py (lines 478-503)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PrimePanning.py PrimePanning -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy

class PrimePanning(InteractiveScene):
    def construct(self):
        # (A bit too much copy paste from above)
        N_max = 500
        number_line = NumberLine(
            (0, N_max),
            unit_size=0.5,
            tick_size=0.075,
        )
        number_line.ticks[::10].stretch(2, 1)
        number_line.add_numbers(range(0, N_max), font_size=20, buff=0.2)
        number_line.move_to(2 * LEFT, LEFT)
        self.add(number_line)

        # Primes
        primes = np.array(list(sympy.primerange(0, N_max)))
        dots = GlowDots(number_line.n2p(primes))
        dots.set_glow_factor(2)
        dots.set_radius(0.35)
        self.add(dots)

        # Pan
        frame = self.frame
        frame.set_height(4)
        frame.add_updater(lambda m, dt: m.shift(1.5 * dt * RIGHT))
        self.wait(90)
