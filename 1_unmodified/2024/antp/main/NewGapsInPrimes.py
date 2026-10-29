# ==============================================================================
# Scene:      NewGapsInPrimes
# Source:     videos/_2024/antp/main.py (lines 735-803)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewGapsInPrimes.py NewGapsInPrimes -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import sympy

class NewGapsInPrimes(InteractiveScene):
    def construct(self):
        # Show number line
        x_min = 99980
        x_max = 100100
        line = NumberLine(
            x_range=(x_min, x_max),
            width=0.5 * (x_max - x_min)
        )
        line.to_edge(LEFT).shift(2 * LEFT)
        line.set_y(1)
        
        primes = [n for n in range(x_min, x_max) if sympy.isprime(n)]
        labels = line.add_numbers(primes, font_size=48)
        lc = labels[:2].get_center()
        labels[:2].arrange(RIGHT, buff=0.5).move_to(lc)
        dots = GlowDots([line.n2p(p) for p in primes])

        self.add(line)
        self.add(dots)

        # Pan over
        center_label = labels[-2]
        self.play(
            self.frame.animate.match_x(center_label).set_height(11),
            run_time=8
        )

        # Label it
        prime_label = TexText(R"Big prime, $p$", font_size=96)
        prime_label.set_color(YELLOW)
        prime_label.next_to(center_label.get_corner(DL), DOWN, 1.5, aligned_edge=RIGHT)
        arrow = Arrow(
            prime_label[-1].get_top(), center_label.get_bottom(),
            buff=0.25,
        )
        arrow.set_stroke(YELLOW)

        self.play(
            FadeIn(prime_label),
            GrowArrow(arrow),
        )
        self.wait()

        # Show the gap
        brace = Brace(Line(*dots.get_points()[-2:]), UP)
        gap_label = Text("gap", font_size=72)
        gap_label.next_to(brace, UP)
        self.play(
            GrowFromPoint(brace, brace.get_left()),
            FadeIn(gap_label, 2 * RIGHT)
        )
        self.wait()

        # Expected gap size
        eq = TexText(R"E[gap] = $\ln(p)$", font_size=96)
        eq["p"][-1].set_color(YELLOW)
        eq.next_to(self.frame.get_top(), DOWN, buff=MED_LARGE_BUFF)

        self.play(LaggedStart(
            FadeIn(eq["E["]),
            FadeIn(eq["] = "]),
            FadeIn(eq[R"\ln("]),
            FadeIn(eq[R")"]),
            FadeTransform(gap_label.copy(), eq["gap"][0]),
            FadeTransform(prime_label[-1].copy(), eq["p"][-1]),
            lag_ratio=0.1,
        ))
        self.wait()
