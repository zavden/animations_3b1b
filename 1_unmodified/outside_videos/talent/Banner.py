# ==============================================================================
# Scene:      Banner
# Source:     videos/outside_videos/talent.py (lines 4-52)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Banner.py Banner -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Banner(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        self.set_floor_plane("xz")

        n_walks = 30
        line_groups = VGroup()
        all_dots = Group()
        for n in range(n_walks):
            line, dots = self.get_random_walk()
            line.set_stroke(opacity=random.random()**2)
            line_groups.add(line)
            all_dots.add(dots)

        line_groups.set_stroke(flat=True)

        # Animate
        frame.set_field_of_view(0.1 * DEG)
        frame.reorient(45, -35, 0, (4.49, 2.29, -0.07), 5.96)
        self.play(
            LaggedStart(
                (ShowCreation(line, rate_func=linear)
                for line in line_groups),
                lag_ratio=0.1,
            ),
            LaggedStartMap(FadeIn, all_dots, lag_ratio=0.1, time_span=(0, 5)),
            frame.animate.reorient(0, 0, 0, (4.5, 2, 0), 5.96).set_anim_args(time_span=(7, 15)),
            run_time=15,
        )

    def get_random_walk(self, n_steps=25):
        line = VMobject()
        point = ORIGIN.copy()
        line.start_new_path(ORIGIN)

        choices = [UP, UP, UP, DOWN, LEFT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, IN, IN, OUT, OUT]

        all_points = [point.copy()]
        for n in range(n_steps):
            point += random.choice(choices)
            line.add_line_to(point)
            all_points.append(point.copy())

        line.set_stroke([BLUE_E, TEAL], width=3, opacity=0.5)
        dots = DotCloud(all_points)
        dots.set_color(WHITE, 0.1)

        return Group(line, dots)
