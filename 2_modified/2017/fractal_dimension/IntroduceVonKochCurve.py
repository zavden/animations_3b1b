# ==============================================================================
# Scene:      IntroduceVonKochCurve
# Source:     videos/_2017/fractal_dimension.py (lines 161-232)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl IntroduceVonKochCurve.py IntroduceVonKochCurve -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 2 integer division in slice
# ==============================================================================

from manim_imports_ext import *

class IntroduceVonKochCurve(Scene):
    CONFIG = {
        "order" : 5,
        "stroke_width" : 3,
    }
    def construct(self):
        snowflake = self.get_snowflake()
        name = OldTexText("Von Koch Snowflake")
        name.to_edge(UP)

        self.play(ShowCreation(snowflake, run_time = 3))
        self.play(Write(name, run_time = 2))
        curve = self.isolate_one_curve(snowflake)
        self.wait()

        self.zoom_in_on(curve)
        self.zoom_in_on(curve)
        self.zoom_in_on(curve)

    def get_snowflake(self):
        triangle = RegularPolygon(n = 3, start_angle = np.pi/2)
        triangle.set_height(4)
        curves = VGroup(*[
            KochCurve(
                order = self.order,
                stroke_width = self.stroke_width
            )
            for x in range(3)
        ])
        for index, curve in enumerate(curves):
            width = curve.get_width()
            curve.move_to(
                (np.sqrt(3)/6)*width*UP, DOWN
            )
            curve.rotate(-index*2*np.pi/3)
        curves.set_color_by_gradient(BLUE, WHITE, BLUE)

        return curves

    def isolate_one_curve(self, snowflake):
        self.play(*[
            ApplyMethod(curve.shift, curve.get_center()/2)
            for curve in snowflake
        ])
        self.wait()
        self.play(
            snowflake.scale, 2.1,
            snowflake.next_to, UP, DOWN
        )
        self.remove(*snowflake[1:])
        return snowflake[0]

    def zoom_in_on(self, curve):
        larger_curve = KochCurve(
            order = self.order+1,
            stroke_width = self.stroke_width
        )
        larger_curve.replace(curve)
        larger_curve.scale(3, about_point = curve.get_corner(DOWN+LEFT))
        larger_curve.set_color_by_gradient(
            curve[0].get_color(),
            curve[-1].get_color(),
        )

        self.play(Transform(curve, larger_curve, run_time = 2))
        n_parts = len(curve.split())
        # CHANGE: Python 2 integer division in slice
        sub_portion = VGroup(*curve[:n_parts//4])
        self.play(
            sub_portion.set_color, YELLOW,
            rate_func = there_and_back
        )
        self.wait()
