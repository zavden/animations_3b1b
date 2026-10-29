# ==============================================================================
# Scene:      InfinitePrimes
# Source:     videos/_2024/antp/main.py (lines 134-190)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InfinitePrimes.py InfinitePrimes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy

class InfinitePrimes(InteractiveScene):
    def construct(self):
        # Test
        n_max = 150
        primes = list(sympy.primerange(2, n_max))
        prime_mobs = VGroup(*map(Integer, primes))
        prime_mobs.set_height(1.5)
        prime_mobs.use_winding_fill(False)

        def update_opacity(prime):
            # alpha = inverse_interpolate(10, 0, prime.get_y())
            alpha = inverse_interpolate(-20, 0, prime.get_z())
            prime.set_fill(opacity=alpha)

        for n, prime in enumerate(prime_mobs):
            # prime.rotate(88 * DEGREES, RIGHT)
            prime.set_height(1.5 * 0.95**n)
            prime.move_to(3 * n * IN)
            prime.add_updater(update_opacity)

        rect = FullScreenRectangle()
        rect.set_fill(BLACK, 1)
        rect.fix_in_frame()

        self.frame.reorient(-70, -30, 70)
        self.frame.set_focal_distance(5)

        self.add(prime_mobs)
        self.play(
            prime_mobs.animate.shift(70 * OUT),
            FadeIn(rect, time_span=(10, 12)),
            run_time=12,
            rate_func=rush_into,
        )

    def old_attempt(self):
        # Old attempt
        point = UL
        height = 2
        shift = 0.75 * np.array([1, -1.2, 0])
        scale = 1.0
        opacity = 1.0

        scale_factor = 0.65
        shift_scale_factor = 0.7
        opacity_scale_factor = 0.9

        for n, mob in enumerate(prime_mobs):
            mob.set_height(height * scale_factor**n)
            mob.move_to(point + sum(
                shift * shift_scale_factor**k
                for k in range(n)
            ))
            mob.set_fill(opacity=opacity * opacity_scale_factor**n)

        prime_mobs.submobjects.reverse()
        self.add(prime_mobs)
