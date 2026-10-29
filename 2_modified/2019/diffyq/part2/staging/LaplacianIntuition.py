# ==============================================================================
# Scene:      LaplacianIntuition
# Source:     videos/_2019/diffyq/part2/staging.py (lines 564-658)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LaplacianIntuition.py LaplacianIntuition -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's VMobject faces, needed for fill, stroke and indexing.
from cairo_compat import CairoParametricSurface as ParametricSurface

class LaplacianIntuition(SpecialThreeDScene):
    CONFIG = {
        "three_d_axes_config": {
            "x_min": -5,
            "x_max": 5,
            "y_min": -5,
            "y_max": 5,
        },
        "surface_resolution": 32,
    }

    def construct(self):
        axes = self.get_axes()
        axes.scale(0.5, about_point=ORIGIN)
        self.set_camera_to_default_position()
        self.begin_ambient_camera_rotation()

        def func(x, y):
            return np.array([
                x, y,
                2.7 + 0.5 * (np.sin(x) + np.cos(y)) -
                0.025 * (x**2 + y**2)
            ])

        surface_config = {
            "u_min": -5,
            "u_max": 5,
            "v_min": -5,
            "v_max": 5,
            "resolution": self.surface_resolution,
        }
        # plane = ParametricSurface(
        #     lambda u, v: np.array([u, v, 0]),
        #     **surface_config
        # )
        # plane.set_stroke(WHITE, width=0.1)
        # plane.set_fill(WHITE, opacity=0.1)
        plane = Square(
            side_length=10,
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.1,
        )
        plane.center()
        plane.set_shade_in_3d(True)

        surface = ParametricSurface(
            func, **surface_config
        )
        surface.set_stroke(BLUE, width=0.1)
        surface.set_fill(BLUE, opacity=0.25)

        self.add(axes, plane, surface)

        point = VectorizedPoint(np.array([2, -2, 0]))
        dot = Dot()
        dot.set_color(GREEN)
        dot.add_updater(lambda d: d.move_to(point))
        line = always_redraw(lambda: DashedLine(
            point.get_location(),
            func(*point.get_location()[:2]),
            background_image_file="VerticalTempGradient",
        ))

        circle = Circle(radius=0.25)
        circle.set_color(YELLOW)
        circle.insert_n_curves(20)
        circle.add_updater(lambda m: m.move_to(point))
        circle.set_shade_in_3d(True)
        surface_circle = always_redraw(
            lambda: circle.copy().apply_function(
                lambda p: func(*p[:2])
            ).shift(
                0.02 * IN
            ).color_using_background_image("VerticalTempGradient")
        )

        self.play(FadeInFromLarge(dot))
        self.play(ShowCreation(line))
        self.play(TransformFromCopy(dot, circle))
        self.play(
            Transform(
                circle.copy(),
                surface_circle.copy().clear_updaters(),
                remover=True,
            )
        )
        self.add(surface_circle)

        self.wait()
        for vect in [4 * LEFT, DOWN, 4 * RIGHT, UP]:
            self.play(
                point.shift, vect,
                run_time=3,
            )
