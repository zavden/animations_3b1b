# ==============================================================================
# Scene:      FourierSeriesIntro
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 128-217)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FourierSeriesIntro.py FourierSeriesIntro -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

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


class FourierSeriesIntro(WriteHeatEquationTemplate):
    def construct(self):
        title_scale_value = 1.5

        title = OldTexText(
            "Fourier ", "Series",
        )
        title.scale(title_scale_value)
        title.to_edge(UP)
        title.generate_target()

        details_coming = OldTexText("Details coming...")
        details_coming.next_to(title.get_corner(DR), DOWN)
        details_coming.set_color(GREY_B)

        # physics = OldTexText("Physics")
        heat = OldTexText("Heat")
        heat.scale(title_scale_value)
        physics = self.get_general_equation()
        physics.set_color_by_tex("{T}", RED)
        arrow1 = Arrow(LEFT, RIGHT)
        arrow2 = Arrow(LEFT, RIGHT)
        group = VGroup(
            heat, arrow1, physics, arrow2, title.target
        )
        group.arrange(RIGHT)
        # physics.align_to(title.target, UP)
        group.to_edge(UP)

        rot_square = Square()
        rot_square.fade(1)
        rot_square.add_updater(lambda m, dt: m.rotate(dt))

        def update_heat_colors(heat):
            colors = [YELLOW, RED]
            vertices = rot_square.get_vertices()
            letters = heat.family_members_with_points()
            for letter, vertex in zip(letters, vertices):
                alpha = (normalize(vertex)[0] + 1) / 2
                i, sa = integer_interpolate(0, len(colors) - 1, alpha)
                letter.set_color(interpolate_color(
                    colors[i], colors[i + 1], alpha,
                ))
        heat.add_updater(update_heat_colors)

        image = ImageMobject("Joseph Fourier")
        image.set_height(5)
        image.next_to(title, DOWN, LARGE_BUFF)
        image.to_edge(LEFT)
        name = OldTexText("Joseph", "Fourier")
        name.next_to(image, DOWN)

        bubble = ThoughtBubble(
            height=2,
            width=2.5,
            direction=RIGHT,
        )
        bubble.set_fill(opacity=0)
        bubble.set_stroke(WHITE)
        bubble.set_stroke(BLACK, 5, background=True)
        bubble.shift(heat.get_center() - bubble.get_bubble_center())
        bubble[:-1].shift(LEFT + 0.2 * DOWN)
        bubble[:-1].rotate(-20 * DEGREES)
        for mob in bubble[:-1]:
            mob.rotate(20 * DEGREES)

        # self.play(FadeInFromDown(title))
        self.add(title)
        self.play(
            FadeInFromDown(image),
            TransformFromCopy(
                title.get_part_by_tex("Fourier"),
                name.get_part_by_tex("Fourier"),
                path_arc=90 * DEGREES,
            ),
            FadeIn(name.get_part_by_tex("Joseph")),
        )
        self.play(Write(details_coming, run_time=1))
        self.play(LaggedStartMap(FadeOut, details_coming[0], run_time=1))
        self.wait()
        self.add(rot_square)
        self.play(
            FadeIn(physics, RIGHT),
            GrowArrow(arrow2),
            FadeIn(heat, RIGHT),
            GrowArrow(arrow1),
            MoveToTarget(title),
        )
        self.play(ShowCreation(bubble))
        self.wait(10)
