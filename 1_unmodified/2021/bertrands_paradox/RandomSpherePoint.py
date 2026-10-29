# ==============================================================================
# Scene:      RandomSpherePoint
# Source:     videos/_2021/bertrands_paradox.py (lines 820-950)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomSpherePoint.py RandomSpherePoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RandomSpherePoint(Scene):
    def construct(self):
        # Setup
        frame = self.camera.frame
        frame.reorient(-20, 70)
        frame.add_updater(lambda m, dt: m.increment_theta(0.015 * dt))

        grid = NumberPlane(
            (-6, 6), (-4, 4),
            background_line_style={
                "stroke_color": GREY_B,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "stroke_width": 1,
            }
        )
        grid.scale(2)
        plane = Rectangle()
        plane.set_stroke(width=0)
        plane.set_gloss(0.5)
        plane.set_fill(GREY_C, 0.5)
        plane.replace(grid, stretch=True)
        plane.add(grid)
        plane.shift(2 * IN)
        self.add(plane)

        sphere_radius = 2
        sphere = Sphere(radius=sphere_radius)
        sphere.set_color(BLUE_E)
        sphere.set_opacity(1.0)
        sphere.move_to(1.5 * OUT)

        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(width=0.5, opacity=0.5)
        mesh.apply_depth_test()
        mesh_shadow = mesh.copy().set_stroke(opacity=0.1)
        mesh_shadow.deactivate_depth_test()

        sphere = Group(sphere, mesh, mesh_shadow)
        self.add(*sphere)

        # Random point
        words = OldTexText("Choose a random$^{*}$\\\\point on a sphere")
        words.fix_in_frame()
        words.to_corner(UL)

        technicality = OldTexText(
            "$^{*}$From a distribution that's\\\\",
            "invariant under rotational symmetries.",
            font_size=30
        )
        technicality[1].set_color(YELLOW)
        technicality.fix_in_frame()
        technicality.to_corner(UR)
        technicality.to_edge(RIGHT, buff=MED_SMALL_BUFF)

        def random_sphere_point():
            p = [1, 1, 1]
            while get_norm(p) > 1:
                p = np.random.uniform(-1, 1, 3)
            p = sphere_radius * normalize(p)
            return p + sphere.get_center()

        dot = TrueDot()
        dot.set_radius(0.5)
        dot.set_color(YELLOW)
        dot.set_glow_factor(5)
        dot.move_to(random_sphere_point())

        self.add(words)
        dot.set_radius(0)
        self.play(dot.animate.set_radius(0.5))

        for x in range(11):
            dot.move_to(random_sphere_point())
            dot.set_opacity(random.choice([0.25, 1.0]))
            if x == 5:
                self.play(FadeIn(technicality), run_time=0.5)
            else:
                self.wait(0.5)
        self.play(FadeOut(dot))

        # Little patch
        band = sphere[0].copy()
        band.pointwise_become_partial(sphere[0], 0.7, 0.8)
        patch = band.copy()
        patch.pointwise_become_partial(band, 0.7, 0.75, axis=0)
        patch.set_color(TEAL)
        patch.set_opacity(0.8)
        patch.deactivate_depth_test()

        dot.move_to(patch)

        def show_dots_in_patch(n=2000):
            dots = DotCloud([
                random_sphere_point()
                for x in range(n)
            ])
            dots.set_color(WHITE)
            dots.set_radius(0.02)
            dots.set_glow_factor(1)
            dots.set_opacity([
                0.25 if point[1] > 0 else 1.0
                for point in dots.get_points()
            ])
            dots.add_updater(lambda m: m)
            self.play(ShowCreation(dots, run_time=6, rate_func=linear))
            self.wait()
            self.play(FadeOut(dots))

        self.play(GrowFromCenter(patch))
        self.wait()
        show_dots_in_patch()
        self.wait()

        # patch_copy = patch.copy()
        self.play(*(
            Rotate(
                sm, PI / 3, axis=OUT + RIGHT,
                about_point=sphere.get_center(),
                run_time=2,
            )
            for sm in (*sphere, patch)
        ))
        show_dots_in_patch()
        self.wait()

        # Embed
        self.embed()
