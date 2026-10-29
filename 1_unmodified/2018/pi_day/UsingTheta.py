# ==============================================================================
# Scene:      UsingTheta
# Source:     videos/_2018/pi_day.py (lines 678-725)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UsingTheta.py UsingTheta -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UsingTheta(Scene):
    def construct(self):
        plane = NumberPlane(x_unit_size = 3, y_unit_size = 3)
        # planes.fade(0.5)
        # plane.secondary_lines.fade(0.5)
        plane.fade(0.5)
        self.add(plane)

        circle = Circle(radius = 3)
        circle.set_stroke(YELLOW, 2)
        self.add(circle)

        radius = Line(ORIGIN, circle.get_right())
        arc = Arc(radius = 0.5, angle = TAU, num_anchors = 200)
        arc.set_color(GREEN)
        start_arc = arc.copy()

        theta = OldTex("\\theta", "=")
        theta[0].match_color(arc)
        theta.add_background_rectangle()
        update_theta = Mobject.add_updater(
            theta, lambda m : m.shift(
                rotate_vector(0.9*RIGHT, radius.get_angle()/2) \
                - m[1][0].get_center()
            )
        )

        angle = Integer(0, unit = "^\\circ")
        update_angle = ContinualChangingDecimal(
            angle, lambda a : radius.get_angle()*(360/TAU),
            position_update_func = lambda a : a.next_to(theta, RIGHT, SMALL_BUFF)
        )

        self.add(update_theta, update_angle)
        last_frac = 0
        for frac in 1./4, 1./12, 3./8, 1./6, 5./6:
            self.play(
                Rotate(radius, angle = (frac-last_frac)*TAU, about_point = ORIGIN),
                UpdateFromAlphaFunc(
                    arc,
                    lambda m, a : m.pointwise_become_partial(
                        start_arc, 0, interpolate(last_frac, frac, a)
                    )
                ),
                run_time = 3
            )
            last_frac = frac
            self.wait()
