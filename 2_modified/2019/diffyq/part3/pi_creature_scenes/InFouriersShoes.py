# ==============================================================================
# Scene:      InFouriersShoes
# Source:     videos/_2019/diffyq/part3/pi_creature_scenes.py (lines 45-95)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl InFouriersShoes.py InFouriersShoes -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject


# ----- From _2019/diffyq/part2/wordy_scenes.py -----

class WriteHeatEquationTemplate(Scene):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{T}": WHITE,
                "{t}": YELLOW,
                "{x}": GREEN,
                "{y}": RED,
                "{z}": BLUE,
                "\\partial": WHITE,
                "2": WHITE,
            },
        },
    }

    def get_d1_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}({x}, {t})", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2} ({x}, {t})",
            **self.tex_mobject_config
        )

    def get_d1_equation_without_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            **self.tex_mobject_config
        )

    def get_d3_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2} + ",
            "{\\partial^2 {T} \\over \\partial {y}^2} + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_general_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )

    def get_d3_equation_with_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}",
            "({x}, {y}, {z}, {t})", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {y}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "({x}, {y}, {z}, {t})",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_d1_words(self):
        return OldTexText("Heat equation\\\\", "(1 dimension)")

    def get_d3_words(self):
        return OldTexText("Heat equation\\\\", "(3 dimensions)")

    def get_d1_group(self):
        group = VGroup(
            self.get_d1_words(),
            self.get_d1_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group

    def get_d3_group(self):
        group = VGroup(
            self.get_d3_words(),
            self.get_d3_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group



# ----- From _2019/diffyq/part3/pi_creature_scenes.py -----

class InFouriersShoes(PiCreatureScene, WriteHeatEquationTemplate):
    def construct(self):
        randy = self.pi_creature
        fourier = ImageMobject("Joseph Fourier")
        fourier.set_height(4)
        fourier.next_to(randy, RIGHT, LARGE_BUFF)
        fourier.align_to(randy, DOWN)

        equation = self.get_d1_equation()
        equation.next_to(fourier, UP, MED_LARGE_BUFF)

        decades = list(range(1740, 2040, 20))
        time_line = NumberLine(
            x_min=decades[0],
            x_max=decades[-1],
            tick_frequency=1,
            tick_size=0.05,
            longer_tick_multiple=4,
            unit_size=0.2,
            big_tick_numbers=decades,
            numbers_to_show=decades,
            decimal_number_config={
                "group_with_commas": False,
            },
            stroke_width=2,
        )
        time_line.add_numbers()
        time_line.move_to(ORIGIN, RIGHT)
        time_line.to_edge(UP)
        triangle = ArrowTip(start_angle=-90 * DEGREES)
        triangle.set_height(0.25)
        triangle.move_to(time_line.n2p(2019), DOWN)
        triangle.set_color(WHITE)

        self.play(FadeIn(fourier, 2 * LEFT))
        self.play(randy.change, "pondering")
        self.wait()
        self.play(
            DrawBorderThenFill(triangle, run_time=1),
            FadeInFromDown(equation),
            FadeIn(time_line),
        )
        self.play(
            Animation(triangle),
            ApplyMethod(
                time_line.shift,
                time_line.n2p(2019) - time_line.n2p(1822),
                run_time=5
            ),
        )
        self.wait()
