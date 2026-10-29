# ==============================================================================
# Scene:      PowersOfTwo
# Source:     videos/_2019/valentines.py (lines 4-91)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PowersOfTwo.py PowersOfTwo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PowersOfTwo(MovingCameraScene):
    def construct(self):
        R = 3
        circle = Circle(radius=R)
        circle.set_stroke(BLUE, 2)
        n = 101
        dots = VGroup()
        numbers = VGroup()
        points = [
            rotate_vector(R * DOWN, k * TAU / n)
            for k in range(n)
        ]
        dots = VGroup(*[
            Dot(point, radius=0.03, color=YELLOW)
            for point in points
        ])
        numbers = VGroup(*[
            Integer(k).scale(0.2).move_to((1.03) * point)
            for k, point in enumerate(points)
        ])
        lines = VGroup(*[
            Line(points[k], points[(2 * k) % n])
            for k in range(n)
        ])
        lines.set_stroke(RED, 2)
        arrows = VGroup(*[
            Arrow(
                n1.get_bottom(), n2.get_bottom(),
                path_arc=90 * DEGREES,
                buff=0.02,
                max_tip_length_to_length_ratio=0.1,
            )
            for n1, n2 in zip(numbers, numbers[::2])
        ])
        transforms = [
            Transform(
                numbers[k].copy(), numbers[(2 * k) % n].copy(),
            )
            for k in range(n)
        ]

        title = OldTex(
            "\\mathds{Z} / (101 \\mathds{Z})"
        )
        title.scale(2)

        frame = self.camera_frame
        frame.save_state()

        self.add(circle, title)
        self.play(
            LaggedStart(*map(FadeInFromLarge, dots)),
            LaggedStart(*[
                FadeIn(n, -normalize(n.get_center()))
                for n in numbers
            ]),
            run_time=2,
        )
        self.play(
            frame.scale, 0.25,
            {"about_point": circle.get_bottom() + SMALL_BUFF * DOWN}
        )
        n_examples = 6
        for k in range(1, n_examples):
            self.play(
                ShowCreation(lines[k]),
                transforms[k],
                ShowCreation(arrows[k])
            )
        self.play(
            frame.restore,
            FadeOut(arrows[:n_examples])
        )
        self.play(
            LaggedStart(*map(ShowCreation, lines[n_examples:])),
            LaggedStart(*transforms[n_examples:]),
            FadeOut(title, rate_func=squish_rate_func(smooth, 0, 0.5)),
            run_time=10,
            lag_ratio=0.01,
        )
        self.play(
            LaggedStart(*[
                ShowCreationThenFadeOut(line.copy().set_stroke(PINK, 3))
                for line in lines
            ]),
            run_time=3
        )
        self.wait(4)
