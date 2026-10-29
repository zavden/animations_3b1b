# ==============================================================================
# Scene:      SimulationAnnotations
# Source:     videos/_2021/holomorphic_dynamics.py (lines 3331-3362)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimulationAnnotations.py SimulationAnnotations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimulationAnnotations(Scene):
    def construct(self):
        dots = self.dots = DotCloud()
        n_radii = 200
        cluster_radius = 0.5
        dots.set_points([
            [cluster_radius * r * math.cos(theta), cluster_radius * r * math.sin(theta), 0]
            for r in np.linspace(1, 0, n_radii)
            for theta in np.linspace(0, TAU, int(r * 20)) + random.random() * TAU
        ])

        n_points_label = OldTexText("$\\sim 2{,}000$ points")
        n_points_label.next_to(dots, UP)

        brace = Brace(
            # Line(dots.get_bottom(), dots.get_corner(DR)),
            Line(dots.get_center(), dots.get_right()),
            DOWN, buff=0
        )
        brace_tex = OldTex("\\text{Radius } \\approx 1 / 1{,}000{,}000")
        brace_tex.next_to(dots, DOWN)

        group = VGroup(n_points_label, brace, brace_tex)
        group.set_stroke(BLACK, 5, background=True)

        self.play(Write(n_points_label))
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_tex, DOWN)
        )
        self.wait()
        self.play(FadeOut(group))
