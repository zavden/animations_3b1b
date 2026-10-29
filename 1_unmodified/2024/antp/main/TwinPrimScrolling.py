# ==============================================================================
# Scene:      TwinPrimScrolling
# Source:     videos/_2024/antp/main.py (lines 6-82)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwinPrimScrolling.py TwinPrimScrolling -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy

class TwinPrimScrolling(InteractiveScene):
    def construct(self):
        # Create list of primes
        n_max = 1000
        primes = list(sympy.primerange(2, n_max))
        prime_mobs = VGroup(*map(Integer, primes))
        prime_mobs.arrange(RIGHT, buff=MED_LARGE_BUFF)
        prime_mobs.move_to(1 * RIGHT, LEFT)
        prime_mobs.shift(2.5 * DOWN)
        prime_mobs.set_fill(border_width=1)

        twin_prime_color = BLUE
        tp_groups = VGroup()
        twin_primes = set()
        for i in range(len(primes) - 1):
            if primes[i] + 2 == primes[i + 1]:
                twin_primes.add(primes[i])
                twin_primes.add(primes[i + 1])
                arc = Line(
                    prime_mobs[i].get_top(),
                    prime_mobs[i + 1].get_top(),
                    path_arc=-PI,
                    stroke_color=twin_prime_color,
                    stroke_width=2,
                )
                arc.scale(0.9, about_edge=UP)
                plus_2 = Tex("+2", font_size=24)
                plus_2.next_to(arc, UP, SMALL_BUFF)
                plus_2.set_color(twin_prime_color)
                tp_groups.add(VGroup(
                    *prime_mobs[i:i + 2].copy(),
                    arc, plus_2
                ))

        non_twin_primes = VGroup(*(
            pm
            for pm, prime in zip(prime_mobs, primes)
            if prime not in twin_primes
        ))

        highlight_point = 5

        def update_tp_groups(tp_groups):
            for tp_group in tp_groups:
                for mob in tp_group[2:]:
                    mob.match_x(tp_group[:2])
                x_coord = tp_group.get_x()
                if x_coord < -10:
                    tp_groups.remove(tp_group)
                    continue
                pre_alpha = inverse_interpolate(
                    highlight_point + 0.25,
                    highlight_point - 0.25,
                    x_coord
                )
                alpha = clip(pre_alpha, 0, 1)
                color = interpolate_color(WHITE, twin_prime_color, alpha)
                tp_group[:2].set_color(color)
                tp_group[2].set_stroke(width=2 * alpha)
                tp_group[3].set_opacity(alpha)

        tp_groups.add_updater(update_tp_groups)

        self.add(non_twin_primes)
        self.add(tp_groups)

        # Animation
        velocity = 1.5
        run_time = non_twin_primes.get_width()

        def shift_updater(mobject, dt):
            mobject.shift(velocity * dt * LEFT)

        tp_groups.add_updater(shift_updater)
        non_twin_primes.add_updater(shift_updater)

        self.wait(run_time)
