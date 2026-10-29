# ==============================================================================
# Scene:      SquareOnASphere
# Source:     videos/_2025/guest_videos/euclid.py (lines 111-189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SquareOnASphere.py SquareOnASphere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SquareOnASphere(InteractiveScene):
    def construct(self):
        # Add sphere
        frame = self.frame
        self.camera.light_source.set_y(5)
        sphere = Sphere()
        sphere.set_color(GREY_D)
        sphere.set_shading(0.5, 0.25, 0.25)
        mesh = SurfaceMesh(sphere, resolution=(41, 21), normal_nudge=1e-3)
        mesh.set_stroke(WHITE, 1, 0.25)

        frame.reorient(0, 84, 0, ORIGIN, 2.50)
        self.add(sphere, mesh)

        # Show "square" lines
        arc_len = 40 * DEG
        u0 = 270 * DEG
        v0 = 100 * DEG

        line1 = ParametricCurve(lambda t: sphere.uv_func(u0, v0 + arc_len * t))
        line1.set_stroke(RED_D, 3)
        all_lines = VGroup(line1)

        self.play(
            ShowCreation(line1, time_span=(0, 2)),
            frame.animate.reorient(5, 57, 0),
            run_time=3
        )

        orientations = [
            (32, 65, 0),
            (23, 85, 0),
            (6, 84, 0),
        ]

        for orientation in orientations:
            last_line = all_lines[-1]
            elbow = self.get_elbow(last_line)
            new_line = last_line.copy()
            new_line = self.get_rotated_arc(last_line, 90 * DEG)
            new_line.reverse_points()
            self.play(
                ShowCreation(new_line, time_span=(0, 2)),
                ShowCreation(elbow, time_span=(0, 1)),
                frame.animate.reorient(*orientation),
                run_time=3
            )
            all_lines.add(new_line)

        # Show transitions
        for line in all_lines[:3]:
            anim = UpdateFromAlphaFunc(
                line.copy(),
                lambda m, a: m.match_points(self.get_rotated_arc(line, a * 90 * DEG)),
                run_time=3,
                time_span=(0, 2)
            )
            if line is all_lines[0]:
                self.play(
                    anim,
                    frame.animate.reorient(7, 61, 0, (-0.02, -0.01, -0.01), 2.68).set_anim_args(run_time=3)
                )
                frame.add_ambient_rotation(2 * DEG)
            else:
                self.play(anim)
        self.wait(5)

    def get_rotated_arc(self, arc, angle):
        return arc.copy().rotate(angle, about_point=arc.get_end(), axis=arc.get_end())

    def get_elbow(self, arc, prop=0.1):
        corner = arc.get_end()
        rot_arc = self.get_rotated_arc(arc, 90 * DEG)
        v1 = arc.get_points()[-2] - corner
        v2 = rot_arc.get_points()[-2] - corner
        elbow = VMobject()
        elbow.set_points_as_corners([corner + v1, corner + v1 + v2, corner + v2])
        elbow.set_stroke(WHITE, 2)
        return elbow
