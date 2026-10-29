# ==============================================================================
# Scene:      SphereStrips
# Source:     videos/_2024/puzzles/added_dimension.py (lines 1738-1984)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereStrips.py SphereStrips -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SphereStrips(InteractiveScene):
    def construct(self):
        # Axes
        frame = self.frame
        frame.set_height(3)
        axes = ThreeDAxes((-2, 2), (-2, 2), (-2, 2))
        axes.set_stroke(width=1)
        plane = NumberPlane((-2, 2), (-2, 2))
        plane.fade(0.5)
        self.add(axes)
        self.add(plane)

        # Circle
        circle = Circle()
        circle.set_stroke(YELLOW, 3)
        circle.set_fill(BLACK, 0.0)
        self.add(circle)

        # Sphere
        sphere = ParametricSurface(
            lambda u, v: [
                np.sin(u) * np.cos(v),
                np.sin(u) * np.sin(v),
                np.cos(u)
            ],
            u_range=(0, PI),
            v_range=(0, 2 * PI)
        )
        sphere.set_opacity(0.5)
        sphere.set_shading(0.5, 0.5, 0.5)
        sphere.always_sort_to_camera(self.camera)
        sphere.set_clip_plane(OUT, 1e-3)

        # Show pre_strip
        delta_x = 0.25
        x0 = 0.5
        strip = self.get_strip(x0, x0 + delta_x, 0)
        pre_strip = strip.copy()
        pre_strip.stretch(1e-3, 2)
        pre_strip.set_z_index(1)
        circle.set_clip_plane(UP, 10)  # Why?
        plane.set_clip_plane(UP, 10)  # Why?

        self.play(ShowCreation(pre_strip, run_time=2))
        self.wait()

        # Expand
        pre_sphere = sphere.copy()
        pre_sphere.stretch(0, 2)
        pre_sphere.shift(1e-2 * IN)
        pre_sphere.set_opacity(0)

        strip.save_state()
        strip.become(pre_strip)
        sphere.save_state()
        sphere.become(pre_sphere)

        self.remove(pre_strip)
        self.add(strip, sphere)

        self.play(
            frame.animate.reorient(-34, 59, 0),
            run_time=2
        )
        self.wait()
        self.add(pre_sphere, pre_strip)
        self.play(
            Restore(strip),
            Restore(sphere),
            run_time=3
        )
        self.play(
            frame.animate.reorient(40, 59, 0),
            run_time=7
        )
        self.wait()

        # Note the area
        brace = Brace(pre_strip, UP)
        brace.add(brace.get_tex(R"d", font_size=24, buff=0.05))
        brace.rotate(90 * DEGREES, RIGHT)
        brace.next_to(strip, OUT, buff=0)

        area_label = TexText(R"Area = $\pi d$")
        area_label.to_corner(UR)
        area_label.fix_in_frame()

        self.play(
            GrowFromCenter(brace, time_span=(1, 2)),
            frame.animate.reorient(-2, 94, 0, (0.31, 0.11, 0.63), 2.35),
            run_time=3,
        )
        self.wait()
        self.play(
            Write(area_label),
            Transform(
                brace[-1].copy(),
                brace[-1].copy().scale(0.5).shift(1.5 * RIGHT + 0.25 * OUT).set_opacity(0),
                remover=True
            )
        )
        self.play(FlashAround(area_label, run_time=2))
        self.wait()

        # Move strip around
        x0_tracker = ValueTracker(x0)
        strip.add_updater(lambda m: m.become(self.get_strip(
            x0_tracker.get_value(),
            x0_tracker.get_value() + delta_x,
            theta=0
        )))
        brace.add_updater(lambda m: m.next_to(strip, OUT, buff=0))

        self.play(
            x0_tracker.animate.set_value(-0.99),
            frame.animate.reorient(-24, 82, 0, (0.4, 0.08, 0.63), 2.67),
            run_time=5,
        )
        self.play(
            x0_tracker.animate.set_value(0.5),
            frame.animate.reorient(2, 76, 0, (0.4, 0.08, 0.63), 2.67),
            run_time=5
        )
        strip.clear_updaters()
        brace.clear_updaters()
        self.play(FadeOut(brace), FadeOut(area_label))

        # Reorient and add make full sphere
        self.play(
            frame.animate.reorient(29, 74, 0, ORIGIN, 3.00).set_anim_args(run_time=2),
            sphere.animate.set_clip_plane(OUT, 1),
            strip.animate.set_clip_plane(OUT, 1),
        )
        self.play(
            frame.animate.reorient(7, 67, 0),
            Rotate(strip, PI / 2, DOWN, about_point=ORIGIN),
            run_time=2
        )
        self.wait()

        # Add cylinder
        clyinder = ParametricSurface(
            lambda u, v: [np.cos(v), np.sin(v), u],
            u_range=[-1, 1],
            v_range=[0, TAU],
        )
        cylinder_mesh = SurfaceMesh(clyinder, resolution=(33, 51))
        cylinder_mesh.set_stroke(WHITE, 1, 0.25)
        cylinder_mesh.set_clip_plane(UP, 20)
        cylinder_mesh.match_height(sphere)

        self.play(self.frame.animate.reorient(26, 69, 0, (-0.0, -0.0, 0.0), 3.00), run_time=3)
        self.play(ShowCreation(cylinder_mesh, lag_ratio=0.01))
        self.wait()

        # Project the strip
        def clyinder_projection(points):
            radii = np.apply_along_axis(np.linalg.norm, 1, points[:, :2])
            return np.transpose([points[:, 0] / radii, points[:, 1] / radii, points[:, 2]])

        def get_proj_strip(strip):
            return strip.copy().apply_points_function(clyinder_projection).set_opacity(0.8)

        proj_strip = get_proj_strip(strip)
        proj_strip.save_state()
        proj_strip.become(strip)

        self.add(proj_strip, cylinder_mesh)
        self.play(
            frame.animate.reorient(-28, 62, 0).set_anim_args(run_time=4),
            Restore(proj_strip, run_time=2),
        )
        self.wait()

        # Vary the height of the strip
        strip.add_updater(lambda m: m.become(
            self.get_strip(
                x0_tracker.get_value(),
                x0_tracker.get_value() + delta_x,
                theta=0,
            ).rotate(PI / 2, DOWN, about_point=ORIGIN)
        ))
        proj_strip.add_updater(lambda m: m.match_z(strip))
        sphere.set_clip_plane(UP, 20)

        self.add(sphere, cylinder_mesh)
        frame.add_ambient_rotation()
        for value in [0.75, 0, 0.5]:
            self.play(x0_tracker.animate.set_value(value), run_time=6)

        frame.clear_updaters()
        strip.clear_updaters()
        proj_strip.clear_updaters()

        # Go back to the hemisphere state
        self.play(
            FadeOut(cylinder_mesh),
            FadeOut(proj_strip, 5 * OUT),
        )
        strip.set_clip_plane(OUT, 0)
        sphere.set_clip_plane(OUT, 1)
        self.play(
            frame.animate.reorient(23, 68, 0),
            sphere.animate.set_clip_plane(OUT, 0),
            Rotate(strip, PI / 2, axis=UP, about_point=ORIGIN),
            run_time=3
        )
        self.wait()

        # Cover with more strips
        strips = Group(
            self.get_strip(
                *sorted(np.random.random(2)),
                theta=random.uniform(0, TAU),
                color=random_bright_color(),
            ).shift(x * 1e-3 * OUT)
            for x in range(1, 20)
        )
        strips.set_opacity(0.5)

        self.play(
            ShowCreation(strips, lag_ratio=0.9),
            frame.animate.reorient(-17, 31, 0),
            run_time=10
        )
        self.play(
            frame.animate.reorient(-24, 64, 0),
            run_time=8,
        )
        self.wait()

    def get_strip(self, x0, x1, theta, color=BLUE):
        strip = ParametricSurface(
            lambda u, v: [
                np.cos(u),
                np.sin(u) * np.cos(v),
                np.sin(u) * np.sin(v),
            ],
            u_range=(math.acos(x1), math.acos(x0)),
            v_range=(0, TAU),
        )
        strip.rotate(theta, OUT, about_point=ORIGIN)
        strip.scale(1.001, about_point=ORIGIN)
        strip.set_color(color)
        strip.set_shading(0.5, 0.5, 0.5)
        strip.set_clip_plane(OUT, 1e-3)
        return strip
