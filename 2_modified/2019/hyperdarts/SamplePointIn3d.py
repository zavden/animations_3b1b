# ==============================================================================
# Scene:      SamplePointIn3d
# Source:     videos/_2019/hyperdarts.py (lines 1330-1431)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SamplePointIn3d.py SamplePointIn3d -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
#   - Translucent cube and sphere with a high z_index (in GL they write depth and hid lines, labels and points that are painted afterwards).
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's VMobject faces, needed for fill, stroke and indexing.
from cairo_compat import CairoSphere as Sphere, CairoCube as Cube

class SamplePointIn3d(SpecialThreeDScene):
    def construct(self):
        axes = self.axes = self.get_axes()
        sphere = self.get_sphere()
        sphere.set_fill(BLUE_E, 0.25)
        sphere.set_stroke(opacity=0.5)

        cube = Cube()
        cube.replace(sphere)
        cube.set_fill(GREY, 0.2)
        cube.set_stroke(WHITE, 1, opacity=0.5)
        # CHANGE: the cube and the sphere are translucent and in GL they write depth: whatever is painted afterwards (lines, labels, point,
        # point cloud) ends up hidden behind their faces. Cairo ordered them back to front; here they are drawn at the end (z_index). The
        # sphere (inside the cube) goes before the cube.
        sphere.set_z_index(10)
        cube.set_z_index(20)

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-120 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.03)

        dot = Sphere()
        # dot = Dot()
        dot.set_shade_in_3d(True)
        dot.set_width(0.1)

        dot.move_to(axes.c2p(*np.random.uniform(0, 1, size=3)))
        lines = always_redraw(lambda: self.get_lines(dot.get_center()))
        labels = always_redraw(lambda: self.get_labels(lines))

        self.add(axes)
        self.add(cube)

        for line, label in zip(lines, labels):
            self.play(
                ShowCreation(line),
                FadeIn(label)
            )
        self.add(lines, labels)
        self.play(GrowFromCenter(dot))
        self.play(DrawBorderThenFill(sphere, stroke_width=1))
        self.wait(2)

        n_points = 3000
        points = [
            axes.c2p(*np.random.uniform(-1, 1, 3))
            for x in range(n_points)
        ]
        # point_cloud = PMobject().add_points(points)
        dots = VGroup(*[
            Dot(
                point,
                radius=0.01,
                shade_in_3d=True,
            )
            for point in points
        ])
        dots.set_stroke(WHITE, 2)
        dots.set_opacity(0.5)
        self.play(ShowIncreasingSubsets(dots, run_time=9))
        # self.play(ShowCreation(point_cloud, run_time=3))
        self.wait(4)
        return

        for x in range(6):
            self.play(
                point.move_to,
                axes.c2p(*np.random.uniform(-1, 1, size=3))
            )
            self.wait(2)
        self.wait(7)

    def get_lines(self, point):
        axes = self.axes
        x, y, z = axes.p2c(point)
        p0 = axes.c2p(0, 0, 0)
        p1 = axes.c2p(x, 0, 0)
        p2 = axes.c2p(x, y, 0)
        p3 = axes.c2p(x, y, z)
        x_line = DashedLine(p0, p1, color=GREEN)
        y_line = DashedLine(p1, p2, color=RED)
        z_line = DashedLine(p2, p3, color=BLUE)
        lines = VGroup(x_line, y_line, z_line)
        lines.set_shade_in_3d(True)
        return lines

    def get_labels(self, lines):
        x_label = OldTex("x")
        y_label = OldTex("y")
        z_label = OldTex("z")
        result = VGroup(x_label, y_label, z_label)
        result.rotate(90 * DEGREES, RIGHT)
        result.set_shade_in_3d(True)

        x_line, y_line, z_line = lines

        x_label.match_color(x_line)
        y_label.match_color(y_line)
        z_label.match_color(z_line)

        x_label.next_to(x_line, IN, SMALL_BUFF)
        y_label.next_to(y_line, RIGHT + OUT, SMALL_BUFF)
        z_label.next_to(z_line, RIGHT, SMALL_BUFF)

        return result
