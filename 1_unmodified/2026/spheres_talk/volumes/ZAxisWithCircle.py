# ==============================================================================
# Scene:      ZAxisWithCircle
# Source:     videos/_2026/spheres_talk/volumes.py (lines 908-951)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ZAxisWithCircle.py ZAxisWithCircle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ZAxisWithCircle(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        axes = ThreeDAxes((-2, 2), (-2, 2), (-2, 2))
        axes.set_width(4)
        sphere = Sphere(radius=1)
        sphere.always_sort_to_camera(self.camera)
        sphere.set_color(BLUE, 0.2)
        mesh = SurfaceMesh(sphere, resolution=(51, 26))
        mesh.set_stroke(WHITE, 2, 0.25)

        z_tracker = ValueTracker(0.6)
        get_z = z_tracker.get_value

        z_line = Line(axes.c2p(0, 0, -1), axes.c2p(0, 0, 1))
        z_line.set_stroke(GREEN, 10)
        z_line.apply_depth_test()
        z_dot = TrueDot(color=GREEN, radius=0.05)
        z_dot.make_3d()
        z_dot.add_updater(lambda m: m.move_to(axes.z_axis.n2p(get_z())))

        circle = Circle(radius=0.8)
        circle.apply_depth_test()
        circle.set_stroke(RED, 10)
        circle.add_updater(lambda m: m.set_width(2.01 * math.sqrt(1 - get_z()**2)))
        circle.add_updater(lambda m: m.move_to(axes.z_axis.n2p(get_z())))

        circle_shadow = VGroup()

        def update_shadow(shadow):
            if len(shadow) > 0 and abs(shadow[-1].get_z() - circle.get_z()) < 5e-3:
                return
            shadow.add(circle.copy().clear_updaters().set_stroke(opacity=0.15, width=2).set_width(2))
            return shadow

        circle_shadow.add_updater(update_shadow)

        frame.reorient(23, 70, 0, (-0.06, 0.05, -0.19), 3.02)
        self.add(axes, z_line, z_dot, circle, sphere, mesh)
        # self.add(circle_shadow)
        self.play(z_tracker.animate.set_value(0.9), run_time=4)
        self.play(z_tracker.animate.set_value(-0.9), run_time=8)
        self.play(z_tracker.animate.set_value(0.6), run_time=6)
