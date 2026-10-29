# ==============================================================================
# Scene:      InverseSquareLaw
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 646-777)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InverseSquareLaw.py InverseSquareLaw -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InverseSquareLaw(InteractiveScene):
    def construct(self):
        # Initial area
        frame = self.frame
        frame.reorient(43, 75, 0)

        light = GlowDot(color=WHITE, radius=0.5)
        axes = ThreeDAxes()
        axes.set_stroke(width=1)
        self.add(axes)

        sphere = Sphere(radius=2)
        sphere.set_color(WHITE, 0.25)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(41, 21))
        mesh.set_stroke(WHITE, 1, 0.25)

        self.add(light)

        # Show eminating light
        big_sphere = sphere.copy().pointwise_become_partial(sphere, 0.5, 1)
        theta, phi = frame.get_euler_angles()[:2]
        big_sphere.rotate(phi, UP, about_point=ORIGIN)
        big_sphere.rotate(theta, IN, about_point=ORIGIN)
        big_sphere.always_sort_to_camera(self.camera)
        big_sphere.scale(3, about_point=ORIGIN)

        radiation, op_tracker = self.beaming_effect(big_sphere, opacity_range=(0.15, 0), n_components=20, speed=0.5)

        op_tracker.set_value(0)
        self.add(radiation)
        self.play(op_tracker.animate.set_value(1), run_time=2)
        self.wait(6)
        self.add(sphere, mesh, radiation)
        self.play(
            op_tracker.animate.set_value(0),
            FadeIn(sphere),
            FadeIn(mesh),
        )
        self.remove(radiation)
        self.wait()

        # Show patch
        patch = ParametricSurface(
            lambda u, v: sphere.uv_func(u, v),
            u_range=(0 * DEG, 9 * DEG),
            v_range=(90 * DEG, 99 * DEG),
        )
        patch.set_color(WHITE)

        beam, op_tracker = self.beaming_effect(patch)

        op_tracker.set_value(0)
        self.add(beam, sphere, mesh)
        self.play(
            op_tracker.animate.set_value(1),
            sphere.animate.set_opacity(0.1),
            mesh.animate.set_stroke(opacity=0.1),
            FadeIn(patch),
        )
        self.wait(2)
        self.play(frame.animate.reorient(72, 75, 0, (-0.12, -0.13, 0.0), 8), run_time=10)

        # Compare to full sphere
        sphere_highlight = sphere.copy()
        sphere_highlight.scale(1.01)
        sphere_highlight.set_color(BLUE, 0.2)

        self.play(ShowCreation(sphere_highlight, run_time=2))
        self.play(FadeOut(sphere_highlight))
        self.wait(3)

        # Grow the sphere
        patch.target = patch.generate_target()
        patch.target.scale(2, about_point=ORIGIN)

        division = VGroup(
            ParametricCurve(lambda t: 2 * sphere.uv_func(t, 94.5 * DEG), t_range=(0 * DEG, 9 * DEG, DEG)),
            ParametricCurve(lambda t: 2 * sphere.uv_func(4.5 * DEG, t), t_range=(90 * DEG, 99 * DEG, DEG)),
        )
        division.set_stroke(GREY_C, 1)

        sphere_group = Group(sphere, mesh)
        ghost_sphere = sphere_group.copy()
        ghost_sphere[0].set_opacity(0.05)
        ghost_sphere[1].set_stroke(opacity=0.05)
        ghost_sphere.scale(0.999)

        self.add(ghost_sphere)
        self.play(
            sphere_group.animate.scale(2),
            MoveToTarget(patch),
            frame.animate.reorient(65, 78, 0, ORIGIN, 8).set_anim_args(run_time=3),
            run_time=2
        )
        self.play(FadeIn(division))
        self.wait(6)

        self.play(
            patch.animate.scale(0.5, about_edge=IN + DOWN).set_opacity(0.5),
            FadeOut(division),
            run_time=2
        )
        self.play(
            frame.animate.reorient(103, 78, 0, (-0.0, 0.0, 0.0), 8.00),
            run_time=18,
        )

    def beaming_effect(self, piece, n_components=20, speed=0.5, opacity_range=(0.5, 0.25)):
        pieces = piece.replicate(n_components)
        d_alpha_range = np.arange(0, 1, 1.0 / n_components)
        radius = get_norm(piece.get_right())

        master_opacity_tracker = ValueTracker(1)

        def update_pieces(pieces):
            beam_time = radius / speed
            alpha = self.time / beam_time

            for subpiece, d_alpha in zip(pieces, d_alpha_range):
                sub_alpha = (alpha + d_alpha) % 1
                subpiece.become(piece)
                pre_opacity = interpolate(*opacity_range, sub_alpha)
                subpiece.set_opacity(pre_opacity * master_opacity_tracker.get_value())
                subpiece.scale(0.99 * sub_alpha, about_point=ORIGIN)

            pieces.sort(get_norm)

            return pieces

        pieces.add_updater(update_pieces)
        return pieces, master_opacity_tracker
