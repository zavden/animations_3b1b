# ==============================================================================
# Scene:      RationalNumbers
# Source:     videos/_2023/gauss_int/herschel.py (lines 431-497)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RationalNumbers.py RationalNumbers -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class RationalNumbers(InteractiveScene):
    def construct(self):
        # Interval
        interval = UnitInterval((0, 1, 1))
        interval.center()
        interval.add_numbers(font_size=36, num_decimal_places=0)
        self.add(interval)

        # Add rational points
        pairs = []
        max_n = 100
        for n in range(2, max_n):
            for k in range(1, n):
                if math.gcd(n, k) == 1:
                    pairs.append((k, n))

        lines = VGroup()
        line_groups = VGroup(*(VGroup() for n in range(max_n - 2)))
        labels = VGroup()
        frac_template = Tex(R"1 \over 2")
        frac_template.make_number_changeable("1")
        frac_template.make_number_changeable("2")

        for pair in pairs:
            k, n = pair
            line = Line(DOWN, UP)
            line.set_height(2.0 / n)
            line.set_stroke(TEAL, width=4.0 / math.sqrt(n))
            line.move_to(interval.n2p(k / n))
            lines.add(line)
            line_groups[n - 2].add(line)

            if n < 15:
                frac = frac_template.copy()
                frac[0].set_value(k)
                frac[2].set_value(n)
                frac[1].match_width(frac[2])
                frac.set_height(1.5 / n)
                frac.next_to(line, UP, SMALL_BUFF)
                labels.add(frac)

        line_groups.set_submobject_colors_by_gradient(BLUE, TEAL)

        for i, j in [(0, 9), (9, 27), (27, len(labels))]:
            self.play(
                LaggedStartMap(FadeIn, lines[i:j], lag_ratio=0.75),
                LaggedStartMap(FadeIn, labels[i:j], lag_ratio=0.75),
                rate_func=linear,
                run_time=3,
            )
        self.play(
            LaggedStartMap(FadeIn, lines[27:], lag_ratio=0.75),
            run_time=10,
            rate_func=rush_into,
        )
        self.wait()

        # Transition to real
        real_line = Line(interval.n2p(0), interval.n2p(1))
        real_line.insert_n_curves(50)
        real_line.set_stroke([TEAL, BLUE, TEAL], width=[0, 3, 3, 0])
        self.play(
            LaggedStart(*(Rotate(line, -90 * DEGREES) for line in lines), lag_ratio=1 / len(lines), run_time=3),
            FadeOut(labels, lag_ratio=0.1, run_time=1),
            ShowCreation(real_line, time_span=(2, 3)),
        )
        self.wait()
