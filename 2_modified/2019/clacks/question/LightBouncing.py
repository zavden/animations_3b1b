# ==============================================================================
# Scene:      LightBouncing
# Source:     videos/_2019/clacks/question.py (lines 501-569)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LightBouncing.py LightBouncing -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth

class LightBouncing(MovingCameraScene):
    CONFIG = {
        "theta": np.arctan(0.15),
        "show_fanning": False,
        "mirror_shift_vect": 5 * LEFT,
        "mirror_length": 10,
        "beam_start_x": 12,
        "beam_height": 1,
    }

    def construct(self):
        theta = self.theta
        h_line = Line(ORIGIN, self.mirror_length * RIGHT)
        d_line = h_line.copy().rotate(theta, about_point=ORIGIN)
        mirrors = VGroup(h_line, d_line)
        self.add(mirrors)

        beam_height = self.beam_height
        start_point = self.beam_start_x * RIGHT + beam_height * UP
        points = [start_point] + [
            np.array([
                (beam_height / np.tan(k * theta)),
                beam_height,
                0,
            ])
            for k in range(1, int(PI / theta))
        ] + [rotate(start_point, PI, UP)]
        reflected_points = []
        for k, point in enumerate(points):
            reflected_point = rotate_vector(point, -2 * (k // 2) * theta)
            reflected_point[1] = abs(reflected_point[1])
            reflected_points.append(reflected_point)
        beam = VMobject()
        beam.set_points_as_corners(reflected_points)
        beam.set_stroke(YELLOW, 2)

        anims = [self.get_beam_anim(beam)]

        if self.show_fanning:
            for k in range(2, int(PI / theta) + 1):
                line = h_line.copy()
                line.set_stroke(WHITE, 1)
                line.rotate(k * theta, about_point=ORIGIN)
                self.add(line)
            straight_beam = VMobject()
            straight_beam.set_points_as_corners(points)
            straight_beam.set_stroke(YELLOW, 2)
            anims.append(self.get_beam_anim(straight_beam))

        self.camera_frame.shift(-self.mirror_shift_vect)
        self.play(*anims)
        self.wait()

    def get_beam_anim(self, beam):
        dot = Dot()
        dot.scale(0.5)
        dot.match_color(beam)
        return AnimationGroup(
            ShowPassingFlash(
                beam,
                run_time=5,
                rate_func=lambda t: smooth(t, 5),
                time_width=0.05,
            ),
            UpdateFromFunc(
                dot,
                lambda m: m.move_to(beam.get_points()[-1])
            ),
        )
