# ==============================================================================
# Scene:      UnreasonableUsefulness
# Source:     videos/_2022/puzzles/subsets.py (lines 290-397)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UnreasonableUsefulness.py UnreasonableUsefulness -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ParametricCurve(t_range=(a, b)) -> t_range=(a, b, 0.1): manimgl unpacks t_range into 3 values (functions.py:39) and no longer fills in the step
# ==============================================================================

import mpmath
import sympy
from manim_imports_ext import *

class UnreasonableUsefulness(InteractiveScene):
    def construct(self):
        # Title
        pre_quote = Text(
            "The unreasonable effectiveness of\n"
            "mathematics in the natural sciences",
            t2c={"mathematics": BLUE, "the natural sciences": TEAL},
            alignment="CENTER"
        )
        quote = Text(
            "The unreasonable effectiveness of\n"
            "complex numbers in discrete math",
            t2c={"complex numbers": BLUE, "discrete math": TEAL},
            alignment="CENTER"
        )
        for text in pre_quote, quote:
            text.to_edge(UP)

        self.add(pre_quote)
        self.wait()
        self.remove(pre_quote)
        quote_anim = LaggedStart(*(
            FadeTransform(pre_quote.select_part(t0), quote.select_part(t1))
            for t0, t1 in [
                2 * ["The unreasonable effectiveness of"],
                ["mathematics", "complex numbers"],
                2 * ["in"],
                ["the natural sciences", "discrete math"],
            ]
        ))

        # Plane and numbers
        plane = ComplexPlane((-3, 3), (-3, 3))
        plane.set_height(5.5)
        plane.to_corner(DL)
        plane.add_coordinate_labels(font_size=20)
        plane_title = Tex("\\mathds{C}")
        plane_title.next_to(plane.get_corner(UL), UR, SMALL_BUFF)

        n, m = 8, 12
        numbers = VGroup(*(Integer(n) for n in range(1, n * m + 1)))
        numbers.arrange_in_grid(m, n, buff=MED_LARGE_BUFF)
        numbers.match_height(plane)
        numbers.match_y(plane).to_edge(RIGHT)

        arrow = Arrow(plane, numbers)

        self.play(
            Write(plane, run_time=1, lag_ratio=0.01, stroke_color=WHITE, stroke_width=1),
            Write(plane_title),
            quote_anim,
        )
        self.play(
            GrowArrow(arrow),
            ShowIncreasingSubsets(numbers, run_time=5),
        )
        self.wait()

        # Highlight primes
        prime_rects = VGroup()
        for num in numbers:
            num.generate_target()
            if sympy.isprime(num.get_value()):
                rect = SurroundingRectangle(num, buff=SMALL_BUFF)
                rect.round_corners()
                rect.set_stroke(TEAL, 1)
                prime_rects.add(rect)
            else:
                num.target.set_opacity(0.25)

        self.play(
            LaggedStartMap(MoveToTarget, numbers),
            ShowIncreasingSubsets(prime_rects),
            run_time=7,
        )
        self.wait()

        # Show zeta
        zeta_def = Tex(
            "\\zeta(s) = \\sum_{n = 1}^\\infty {1 \\over n^s}",
            font_size=42,
            tex_to_color_map={"s": YELLOW}
        )
        zeta_def.next_to(plane.c2p(-3, 3), DR)
        zeta_def_highlight = VHighlight(
            zeta_def,
            color_bounds=(BLACK, BLACK),
            max_stroke_addition=12,
        )
        for a, layer in zip(np.linspace(1, 0.2, 5), zeta_def_highlight):
            layer.set_stroke(opacity=a)

        zeta_spiril = ParametricCurve(
            lambda t: plane.n2p(complex(mpmath.zeta(complex(0.5, t)))),
            # CHANGE: ParametricCurve unpacks t_range into (min, max, step) and no longer completes a 2-value t_range; the default step 0.1 is added
            t_range=(0, 42, 0.1),
        )
        zeta_spiril.set_stroke([YELLOW, YELLOW, RED], 2)

        self.play(
            ApplyMethod(
                plane.coordinate_labels[-2:].set_opacity, 0,
                time_span=(3, 4),
            ),
            FadeIn(zeta_def_highlight, time_span=(3, 4)),
            Write(zeta_def, time_span=(2, 4)),
            ShowCreation(zeta_spiril, rate_func=smooth, run_time=16),
        )
        self.wait()
