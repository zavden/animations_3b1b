# ==============================================================================
# Scene:      AskAboutOutside
# Source:     videos/_2026/hairy_ball/spheres.py (lines 972-1119)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AskAboutOutside.py AskAboutOutside -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - The d_normal_point field no longer exists in Surface data: the normal at the example point is obtained with sphere.get_unit_normals()[index] (same normal, without having to subtract the point).
# ==============================================================================

from manim_imports_ext import *

class AskAboutOutside(InteractiveScene):
    def construct(self):
        # Set up
        frame = self.frame
        radius = 2
        axes = ThreeDAxes().scale(radius)
        axes.set_stroke(WHITE, 1, 0.5)
        axes.set_flat_stroke(False)
        axes.set_z_index(1)

        def sphere_uv(u, v):
            return [math.cos(u) * math.sin(v), math.sin(u) * math.sin(v), -math.cos(v)]

        sphere_group = self.get_warped_sphere_group(sphere_uv)
        sphere, mesh = sphere_group

        frame.reorient(-6, 70, 0)
        self.add(sphere, mesh, axes)

        # Show a character on the surface
        morty = Mortimer(mode="confused", height=0.1).flip()
        mirror_morty = morty.copy().flip(axis=RIGHT, about_edge=DOWN)
        mirror_morty.fade(0.5)
        out_arrow = Vector(0.15 * UP, thickness=0.5)
        out_arrow.next_to(morty, LEFT, buff=0.025, aligned_edge=DOWN)
        in_arrow = out_arrow.copy().flip(axis=RIGHT, about_edge=DOWN)
        out_arrow.set_color(BLUE)
        in_arrow.set_color(RED)
        morty_group = VGroup(morty, mirror_morty, out_arrow, in_arrow)

        morty_group.rotate(90 * DEG, RIGHT)
        morty_group.move_to(sphere.get_zenith())
        morty_group.rotate(30 * DEG, axis=UP, about_point=ORIGIN)

        sphere.set_clip_plane(UP, 2)

        self.play(
            FadeIn(morty, time_span=(0, 1)),
            sphere.animate.set_opacity(0.25),
            frame.animate.reorient(-5, 83, 0, (1.09, 0.51, 1.62), 1.15),
            run_time=3
        )
        self.play(GrowArrow(out_arrow))
        self.wait()
        self.play(
            TransformFromCopy(morty, mirror_morty),
            GrowArrow(in_arrow)
        )
        self.wait()

        # Show obvious outside and inside
        out_arrows, in_arrows = all_arrows = VGroup(
            VGroup(
                Arrow(radius * a1 * point, radius * a2 * point, fill_color=color, thickness=4, buff=0)
                for point in compass_directions(24)
            )
            for a1, a2, color in [(1.1, 1.5, BLUE), (0.9, 0.7, RED)]
        )
        all_arrows.rotate(90 * DEG, RIGHT, about_point=ORIGIN)

        self.play(
            frame.animate.reorient(-4, 82, 0, (0.15, -0.01, 0.02), 8.08),
            LaggedStartMap(GrowArrow, out_arrows, lag_ratio=0.01, time_span=(3, 6)),
            run_time=6
        )
        self.wait()
        self.play(
            FadeOut(out_arrows),
            FadeOut(morty_group),
            sphere.animate.set_opacity(1)
        )

        # Warp the sphere
        def twist_sphere_uv(u, v):
            return [math.cos(u + v - 0.5) * math.sin(v), math.sin(u + v - 0.5) * math.sin(v), -math.cos(v)]

        def squish_sphere_uv(u, v):
            x, y, z = twist_sphere_uv(u, v)
            dist = math.sqrt(x**2 + y**2)
            z *= -35 * (dist - 0.25) * (dist - 0.75) * (dist - 0) * (dist - 1.1)
            return (x, y, z)

        twisted_sphere = self.get_warped_sphere_group(twist_sphere_uv)
        squish_sphere = self.get_warped_sphere_group(squish_sphere_uv)

        self.play(
            Transform(sphere_group, twisted_sphere),
            frame.animate.reorient(-1, 73, 0, (-0.23, 0.06, -0.09), 6.00),
            run_time=5
        )
        self.play(
            frame.animate.reorient(12, 73, 0, (-0.09, 0.1, -0.06), 4.71),
            Transform(sphere_group, squish_sphere),
            run_time=5
        )

        # Example point
        index = 9200
        point = sphere.get_points()[index]
        # CHANGE: this manimgl no longer stores the d_normal_point field in Surface data; get_unit_normals() gives the same normal
        normal = sphere.get_unit_normals()[index]
        dot = TrueDot(point, color=YELLOW)
        dot.make_3d()
        dot.deactivate_depth_test()
        dot.set_radius(0.01)
        dot.set_z_index(1)

        in_vect, out_vect = vects = VGroup(
            Vector(sign * 0.2 * normal, thickness=0.5, fill_color=color).shift(point)
            for sign, color in zip([1, -1], [RED, BLUE])
        )
        for vect in vects:
            vect.set_perpendicular_to_camera(frame)

        self.add(dot)
        self.play(
            FadeIn(dot),
            frame.animate.reorient(-47, 81, 0, (-0.55, 0.17, 0.13), 0.65),
            run_time=3
        )
        self.play(GrowArrow(in_vect))
        self.play(GrowArrow(out_vect))
        self.wait()

        # Show a homotopy
        def homotopy(x, y, z, t):
            alpha = clip((x + 3) / 6 - 1 + 2 * t, 0, 1)
            shift = wiggle(alpha, 3)
            return (x, y, z + 0.35 * shift)

        self.play(
            FadeOut(vects, time_span=(0, 1)),
            FadeOut(dot, time_span=(0, 1)),
            Homotopy(homotopy, sphere_group),
            frame.animate.reorient(-44, 78, 0, (-0.16, 0.02, 0.31), 4.18),
            run_time=6,
        )


    def get_warped_sphere_group(self, uv_func, radius=2, mesh_resolution=(61, 31), u_range=(0, TAU), v_range=(0, PI)):
        surface = ParametricSurface(uv_func, u_range=u_range, v_range=v_range, resolution=(201, 101))
        surface.always_sort_to_camera(self.camera)
        surface.set_color(GREY_D)
        mesh = SurfaceMesh(surface, resolution=mesh_resolution, normal_nudge=0)
        mesh.set_stroke(WHITE, 0.5, 0.25)
        mesh.deactivate_depth_test()
        result = Group(surface, mesh)
        result.scale(radius, about_point=ORIGIN)
        return result
