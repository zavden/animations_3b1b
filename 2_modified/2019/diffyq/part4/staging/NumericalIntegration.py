# ==============================================================================
# Scene:      NumericalIntegration
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1898-1995)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NumericalIntegration.py NumericalIntegration -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth

class NumericalIntegration(Scene):
    CONFIG = {
        "tex_config": {
            "tex_to_color_map": {
                "{t}": LIGHT_PINK,
                "{dt}": LIGHT_PINK,
                "{n}": YELLOW,
                "{0.01}": WHITE,
            }
        }
    }

    def construct(self):
        self.add_title()
        self.add_integral()

    def add_title(self):
        title = OldTexText("Integrate numerically")
        title.scale(1.5)
        title.to_edge(UP)
        line = Line()
        line.set_width(title.get_width() + 1)
        line.next_to(title, DOWN)
        self.add(title, line)
        self.title = title

    def add_integral(self):
        integral = OldTex(
            "c_{n}", "=", "\\int_0^1 f({t})"
            "e^{-{n} \\cdot 2\\pi i {t}}{dt}",
            **self.tex_config,
        )
        integral.to_edge(LEFT)

        sum_tex = OldTex(
            " \\approx \\text{sum([} \\dots",
            "f({0.01}) e^{-{n} \\cdot 2\\pi i ({0.01})}({0.01})"
            "\\dots \\text{])}",
            **self.tex_config,
        )
        sum_tex.next_to(
            integral.get_part_by_tex("="), DOWN,
            buff=LARGE_BUFF,
            aligned_edge=LEFT,
        )

        group = VGroup(integral, sum_tex)
        group.next_to(self.title, DOWN, LARGE_BUFF)

        t_tracker = ValueTracker(0)
        decimal_templates = sum_tex.get_parts_by_tex("{0.01}")
        decimal_templates.set_color(LIGHT_PINK)
        decimals = VGroup(*[DecimalNumber() for x in range(2)])
        for d, dt in zip(decimals, decimal_templates):
            d.replace(dt)
            d.set_color(LIGHT_PINK)
            d.add_updater(lambda d: d.set_value(
                t_tracker.get_value()
            ))
            dt.set_opacity(0)

        delta_t_brace = Brace(decimal_templates[-1], UP, buff=SMALL_BUFF)
        delta_t = delta_t_brace.get_tex(
            "\\Delta t", buff=SMALL_BUFF
        )
        delta_t.set_color(PINK)

        input_line = UnitInterval(
            unit_size=10,
        )
        input_line.next_to(group, DOWN, LARGE_BUFF)
        input_line.add_numbers(0, 0.5, 1)
        dots = VGroup(*[
            Dot(
                input_line.n2p(t),
                color=PINK,
                radius=0.03,
            ).stretch(2, 1)
            for t in np.arange(0, 1, 0.01)
        ])

        self.add(integral)
        self.add(sum_tex)
        self.add(decimals)
        self.add(delta_t, delta_t_brace)
        self.add(input_line)

        time = 15
        self.play(
            t_tracker.set_value, 0.99,
            ShowIncreasingSubsets(dots),
            run_time=time,
            rate_func=lambda t: smooth(t, 1),
        )
        self.wait()

    def get_term(self, t, dt):
        pass
