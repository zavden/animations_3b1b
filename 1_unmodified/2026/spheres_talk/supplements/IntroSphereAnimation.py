# ==============================================================================
# Scene:      IntroSphereAnimation
# Source:     videos/_2026/spheres_talk/supplements.py (lines 28-104)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroSphereAnimation.py IntroSphereAnimation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroSphereAnimation(InteractiveScene):
    def construct(self):
        # Circles to sphere
        frame = self.frame
        frame.set_height(4)

        circle = Circle(radius = 1)
        circle.set_stroke(TEAL, 2)

        lattitude_lines = VGroup(
            Circle(radius=math.sqrt(1 - z**2)).set_z(z)
            for z in np.linspace(-0.99, 0.99, 50)
        )
        lattitude_lines.set_stroke(TEAL, 1, 0.5)

        self.play(ShowCreation(circle))
        self.remove(circle)
        self.play(
            LaggedStart(
                (TransformFromCopy(circle, lat_line)
                for lat_line in lattitude_lines),
                lag_ratio=0.05,
            ),
            frame.animate.reorient(-2, 56, 0, (0.02, -0.09, -0.07), 2.83),
            run_time=6,
        )
        frame.add_ambient_rotation(4 * DEG)
        self.wait()

        # Spheres
        mesh = SurfaceMesh(Sphere(radius=1), resolution=(101, 201))
        sphere = VMobject()
        for part in mesh:
            sphere.append_vectorized_mobject(part)
        sphere.set_stroke(BLUE, 0.1)

        lattitude_spheres = VGroup()
        pre_points = sphere.get_points().copy()
        for w in np.linspace(-0.99, 0.99, 20):
            points_4d = np.zeros((len(pre_points), 4))
            points_4d[:, :3] = pre_points * math.sqrt(1 - w**2)
            points_4d[:, 3] = w
            lat_sphere = sphere.copy()
            lat_sphere.points_4d = points_4d
            lattitude_spheres.add(lat_sphere)

        lattitude_spheres.set_stroke(opacity=0.1)

        angle_tracker = ValueTracker(0)

        def update_lat_sphere(lat_sphere):
            rot_matrix_T = rotation_matrix_transpose(angle_tracker.get_value(), axis=UR)
            pre_proj = lat_sphere.points_4d.copy()
            pre_proj[:, 1:] = np.dot(pre_proj[:, 1:], rot_matrix_T)
            lat_sphere.set_points(pre_proj[:, :3])

        for lat_sphere in lattitude_spheres:
            lat_sphere.add_updater(update_lat_sphere)

        self.play(FadeIn(sphere), FadeOut(lattitude_lines))
        self.wait()
        self.play(
            LaggedStart(
                (ReplacementTransform(sphere.copy().scale(0.99).set_opacity(0), lat_sphere)
                for lat_sphere in lattitude_spheres),
                lag_ratio=0.05,
            ),
            FadeOut(sphere),
            angle_tracker.animate.set_value(80 * DEG),
            run_time=6
        )
        self.wait()
        self.play(
            angle_tracker.animate.set_value(360 * DEG),
            run_time=12,
        )
        self.wait()
