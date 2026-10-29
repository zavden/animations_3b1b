# ==============================================================================
# Scene:      ShowPrimeDensity
# Source:     videos/_2022/zeta/part1.py (lines 23-96)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowPrimeDensity.py ShowPrimeDensity -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - t = smooth() (no argument, incomplete draft in the original) -> t = 10 * soft_smooth(n / x_max), the appearance time of each prime within run_time=11
# ==============================================================================

from manim_imports_ext import *
import sympy

PRIME_COLOR = YELLOW


class ShowPrimeDensity(InteractiveScene):
    def construct(self):
        # Setup
        frame = self.camera.frame

        x_max = 150
        numberline = NumberLine((0, x_max), width=0.7 * x_max)
        numberline.to_edge(LEFT)
        numberline.add_numbers()

        def get_number_animation(n):
            if sympy.isprime(n):
                return self.get_prime_animation(numberline, n)
            else:
                return Animation(Mobject(), remover=True)

        self.add(numberline)

        # Show the first 100 primes
        all_prime_animations = []
        soft_smooth = bezier([0, 0, 1, 1])
        for n in range(x_max):
            if sympy.isprime(n):
                # CHANGE: the original calls smooth() with no argument (a 3b1b draft); t is the instant in [0, 10] at which the prime appears
                t = 10 * soft_smooth(n / x_max)
                all_prime_animations.append(self.get_prime_animation(
                    numberline, n,
                    run_time=11,
                    time_span=(t, t + 1)
                ))


        frame.generate_target()
        frame.target.move_to(numberline.n2p(100))
        frame.target.scale(2)

        self.play(
            LaggedStart(*all_prime_animations, lag_ratio=0.25),
            MoveToTarget(
                frame,
                rate_func=smooth,
                time_span=(2, 10),
            ),
            run_time=10,
        )

        # Zoom out to 1 million

        # Zoom out to 1 trillion

        # Mention logarithm rule

        # Ask about log rule

    def get_prime_animation(self, numberline, prime, **kwargs):
        numberline.get_unit_size()
        point = numberline.n2p(prime)
        dot = GlowDot(point, color=PRIME_COLOR)
        dot.set_glow_factor(0)
        dot.set_radius(0.5)
        dot.set_opacity(0)
        dot.generate_target()
        dot.target.set_glow_factor(2)
        dot.target.set_opacity(1)
        dot.target.set_radius(DEFAULT_GLOW_DOT_RADIUS)

        arrow = Vector(DOWN, color=PRIME_COLOR)
        arrow.move_to(point, DOWN)

        return AnimationGroup(
            ShowCreation(arrow),
            MoveToTarget(dot, rate_func=rush_into),
            numberline.numbers[prime].animate.set_color(PRIME_COLOR),
            **kwargs
        )
