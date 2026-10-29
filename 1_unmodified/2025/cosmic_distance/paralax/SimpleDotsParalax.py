# ==============================================================================
# Scene:      SimpleDotsParalax
# Source:     videos/_2025/cosmic_distance/paralax.py (lines 5-70)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleDotsParalax.py SimpleDotsParalax -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleDotsParalax(InteractiveScene):
    show_pi_perspective = False

    def construct(self):
        # Add stars
        frame = self.frame
        self.set_floor_plane("xz")

        height = 4
        cube = VCube(height)
        cube.set_fill(opacity=0)
        cube.set_stroke(BLUE, 2)

        n_stars = 200
        stars = GlowDots(np.random.uniform(-1, 1, (n_stars, 3)))
        stars.scale(height / 2)
        stars.set_color(WHITE)
        stars.set_glow_factor(2)
        stars.set_radii(np.random.uniform(0, 0.075, n_stars))

        self.add(cube)
        self.add(stars)

        self.play(ShowCreation(stars, run_time=4))

        # Add randy
        randy = Randolph(height=1)
        randy.next_to(cube, LEFT, buff=1)

        self.play(
            VFadeIn(randy),
            randy.change("pondering", look_at=RIGHT)
        )

        if self.show_pi_perspective:
            self.play(
                frame.animate.reorient(-89, -4, 0, (0.01, 0.21, 0.0), 3.05),
                randy.animate.set_opacity(0),
                cube.animate.set_stroke(width=5).set_anti_alias_width(10),
                run_time=3,
            )
            frame.always.match_z(randy)
        else:
            self.play(frame.animate.reorient(-40, -26, 0), run_time=3)

        # Move up and down
        for dy in [1, -2, 2, -2, 1]:
            self.play(randy.animate.shift(dy * 1.5 * IN), run_time=5)

        return

        # Show some triangle
        star_points = np.array(list(filter(lambda p: get_norm(p) < 1, stars.get_points())))
        star_points[0] *= 10
        random.seed(1)
        verts = random.sample(list(star_points), 3)
        triangle = Polygon(*verts)
        triangle.set_color(RED)
        red_stars = DotCloud(verts)
        red_stars.set_radius(0.02)
        red_stars.set_color(RED)

        self.play(
            ShowCreation(triangle),
            FadeIn(red_stars),
        )
