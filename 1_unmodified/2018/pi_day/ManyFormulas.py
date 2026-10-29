# ==============================================================================
# Scene:      ManyFormulas
# Source:     videos/_2018/pi_day.py (lines 395-443)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyFormulas.py ManyFormulas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ManyFormulas(Scene):
    def construct(self):
        formulas = VGroup(
            OldTex("\\sin(x + \\tau) = \\sin(x)"),
            OldTex("e^{\\tau i} = 1"),
            OldTex("n! \\approx \\sqrt{\\tau n} \\left(\\frac{n}{e} \\right)^n"),
            OldTex("c_n = \\frac{1}{\\tau} \\int_0^\\tau f(x) e^{inx}dx"),
        )
        formulas.arrange(DOWN, buff = MED_LARGE_BUFF)
        formulas.to_edge(LEFT)

        self.play(LaggedStartMap(FadeIn, formulas, run_time = 3))

        circle = Circle(color = YELLOW, radius = 2)
        circle.to_edge(RIGHT)
        radius = Line(circle.get_center(), circle.get_right())
        radius.set_color(WHITE)

        angle_groups = VGroup()
        for denom in 5, 4, 3, 2:
            radius_copy = radius.copy()
            radius_copy.rotate(TAU/denom, about_point = circle.get_center())
            arc = Arc(
                angle = TAU/denom,
                stroke_color = RED,
                stroke_width = 4,
                radius = circle.radius,
            )
            arc.shift(circle.get_center())
            mini_arc = arc.copy()
            mini_arc.set_stroke(WHITE, 2)
            mini_arc.scale(0.15, about_point = circle.get_center())
            tau_tex = OldTex("\\tau/%d"%denom)
            point = mini_arc.point_from_proportion(0.5)
            tau_tex.next_to(point, direction = point - circle.get_center())
            angle_group = VGroup(radius_copy, mini_arc, tau_tex, arc)
            angle_groups.add(angle_group)


        angle_group = angle_groups[0]
        self.play(*list(map(FadeIn, [circle, radius])))
        self.play(
            circle.set_stroke, {"width" : 1,},
            FadeIn(angle_group),
        )
        self.wait()
        for group in angle_groups[1:]:
            self.play(Transform(angle_group, group, path_arc = TAU/8))
            self.wait()
