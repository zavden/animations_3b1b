# ==============================================================================
# Scene:      TweakMuInFormula
# Source:     videos/_2019/diffyq/part1/phase_space.py (lines 1043-1116)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl TweakMuInFormula.py TweakMuInFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/phase_space.py -----

class TweakMuInFormula(Scene):
    def construct(self):
        self.add(FullScreenFadeRectangle(
            opacity=0.75,
        ))

        ode = get_ode()
        ode.to_edge(DOWN, buff=LARGE_BUFF)
        mu = ode.get_part_by_tex("\\mu")
        lil_rect = SurroundingRectangle(mu, buff=0.5 * SMALL_BUFF)
        lil_rect.stretch(1.2, 1, about_edge=DOWN)
        lil_rect.set_stroke(PINK, 2)

        interval = UnitInterval()
        interval.add_numbers(
            *np.arange(0, 1.2, 0.2)
        )
        interval.next_to(ode, UP, LARGE_BUFF)
        big_rect_seed = SurroundingRectangle(interval, buff=MED_SMALL_BUFF)
        big_rect_seed.stretch(1.5, 1, about_edge=DOWN)
        big_rect_seed.stretch(1.2, 0)
        big_rect = VGroup(*[
            DashedLine(v1, v2)
            for v1, v2 in adjacent_pairs(big_rect_seed.get_vertices())
        ])
        big_rect.set_stroke(PINK, 2)

        arrow = Arrow(
            lil_rect.get_top(),
            big_rect_seed.point_from_proportion(0.65),
            buff=SMALL_BUFF,
        )
        arrow.match_color(lil_rect)

        mu_tracker = ValueTracker(0.1)
        get_mu = mu_tracker.get_value

        triangle = Triangle(
            start_angle=-90 * DEGREES,
            stroke_width=0,
            fill_opacity=1,
            fill_color=WHITE,
        )
        triangle.set_height(0.2)
        triangle.add_updater(lambda t: t.next_to(
            interval.number_to_point(get_mu()),
            UP, buff=0,
        ))

        equation = VGroup(
            OldTex("\\mu = "),
            DecimalNumber(),
        )
        equation.add_updater(
            lambda e: e.arrange(RIGHT).next_to(
                triangle, UP, SMALL_BUFF,
            ).shift(0.4 * RIGHT)
        )
        equation[-1].add_updater(
            lambda d: d.set_value(get_mu()).shift(0.05 * UL)
        )

        self.add(ode)
        self.play(ShowCreation(lil_rect))
        self.play(
            GrowFromPoint(interval, mu.get_center()),
            GrowFromPoint(triangle, mu.get_center()),
            GrowFromPoint(equation, mu.get_center()),
            TransformFromCopy(lil_rect, big_rect),
            ShowCreation(arrow)
        )
        self.wait()
        self.play(mu_tracker.set_value, 0.9, run_time=5)
        self.wait()
