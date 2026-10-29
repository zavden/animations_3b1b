# ==============================================================================
# Scene:      Exercise
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 824-973)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Exercise.py Exercise -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Exercise(InteractiveScene):
    def construct(self):
        # Tex key word args
        tex_kw = dict(
            t2c={
                R"\sigma_1": RED,
                R"\sigma_2": RED_B,
            }
        )

        # Set up axes
        planes = VGroup(*(
            NumberPlane(
                (-1, 3), (-1, 3),
                background_line_style=dict(stroke_color=GREY_A, stroke_width=1, stroke_opacity=0.5),
                faded_line_style=dict(stroke_color=GREY_A, stroke_width=1, stroke_opacity=0.25),
                width=5, height=5
            )
            for x in range(2)
        ))
        labels = VGroup(*map(Tex, ["x", "y", "x'", "y'"]))
        labels.scale(0.75)
        label_iter = iter(labels)
        for plane in planes:
            for axis, vect in zip(plane.axes, [RIGHT, UP]):
                label = next(label_iter)
                label.next_to(axis.get_end(), vect, SMALL_BUFF)
                plane.add(label)

        planes.arrange(RIGHT, buff=4.0)
        planes.set_width(10)
        planes.to_edge(LEFT)
        planes.set_y(-1.5)

        arrow = Arrow(*planes, stroke_width=6, stroke_color=RED, buff=0.5)

        self.add(planes)
        self.add(arrow)

        # Show lines and intersections
        lines = VGroup(
            Line(planes[0].c2p(-1, 3), planes[0].c2p(3, -1)),
            Line(planes[1].c2p(-0.25, 3), planes[1].c2p(2.25, -1)),
        )
        lines.set_stroke(YELLOW, 2)
        intersection_labels = VGroup(*(
            Tex(tex, **tex_kw)
            for tex in [
                "(s, 0)",
                "(0, s)",
                R"(s / \sigma_1)",
                R"(s / \sigma_2)",
            ]
        ))
        intersection_labels.scale(0.5)
        intersection_labels_iter = iter(intersection_labels)
        dots = Group()

        for plane, line in zip(planes, lines):
            for axis in plane.axes:
                point = find_intersection(
                    line.get_start(), line.get_vector(),
                    axis.get_start(), axis.get_vector(),
                )
                dot = GlowDot(point, color=WHITE)
                dots.add(dot)
                label = next(intersection_labels_iter)
                label.set_backstroke(width=2)
                label.next_to(point, DL, buff=SMALL_BUFF)

        l2_perp = lines[1].copy().rotate(90 * DEGREES)
        l2_perp.shift(planes[1].get_origin() - l2_perp.get_start())
        mid_point = find_intersection(
            l2_perp.get_start(), l2_perp.get_vector(),
            lines[1].get_start(), lines[1].get_vector()
        )
        d_line = Line(planes[1].get_origin(), mid_point)
        d_line.set_stroke(GREEN, 2)
        d_label = Tex("d", font_size=36)
        d_label.next_to(d_line.get_center(), UL, buff=0.05)
        elbow = Elbow()
        elbow.rotate(l2_perp.get_angle() + 90 * DEGREES, about_point=ORIGIN)
        elbow.set_stroke(width=1)
        elbow.shift(mid_point)

        self.add(lines)
        self.add(dots)
        self.add(intersection_labels)
        self.add(d_line)
        self.add(d_label)
        self.add(elbow)

        # Equations
        d_eq = Tex(R"d = \frac{s}{\sqrt{\sigma_1^2 + \sigma_2^2}}", **tex_kw)
        d_eq.scale(0.85)
        d_eq.next_to(planes[1], RIGHT, buff=0.35)

        xy_eq = Tex("x + y = s")
        xy_eq.scale(0.7)
        xy_eq.set_backstroke(width=3)
        xy_eq.next_to(lines[0].get_center(), UR, SMALL_BUFF)

        change_of_coord_eqs = VGroup(
            Tex(R"x' = x / \sigma_1", **tex_kw),
            Tex(R"y' = y / \sigma_2", **tex_kw),
        )
        change_of_coord_eqs.arrange(DOWN)
        change_of_coord_eqs.scale(0.7)
        change_of_coord_eqs.next_to(arrow, UP)

        self.add(d_eq)
        self.add(xy_eq)
        self.add(change_of_coord_eqs)

        # Words
        tex_kw["alignment"] = ""
        words = VGroup(
            TexText(R"""
                Consider the diagonal slice method for two Gaussians with\\
                different standard deviations, $\sigma_1$ and $\sigma_2$:\\
                $$
                f(x) = \frac{1}{\sigma_1 \sqrt{2\pi}} e^{-\frac{1}{2}(x / \sigma_1)^2}
                \quad \text{ and } \quad
                g(y) = \frac{1}{\sigma_2 \sqrt{2\pi}} e^{-\frac{1}{2}(y / \sigma_2)^2}
                \qquad\qquad\qquad\qquad\qquad\qquad
                $$
                The graph of $f(x)g(y)$ is no longer rotationally symmetric.\\
                However, it will be if you pass to a new set of coordinates\\
                $(x', y')$ as illustrated below. Why?
            """, **tex_kw),
            TexText(R"""
                The transformatoin of the line $x + y = s$ is illustrated below.\\
                After the transformation, the area of a the slice of the graph\\
                over this line is changed by some factor which depends on\\
                $\sigma_1$ and $\sigma_2$, but importantly, not on $s$.
                \\ \\
                Explain how to find the distance $d$ in the digram below, and\\
                how this shows that the area of a slice of $f(x)g(y)$ over the line\\
                $x + y = s$ is proportional to $e^{-\frac{1}{2} s^2 / (\sigma_1^2 + \sigma_2^2)}$.
            """, **tex_kw),
        )
        words.arrange(RIGHT, buff=LARGE_BUFF, aligned_edge=UP)
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(UP)
        v_line = Line(words.get_top(), words.get_bottom())
        v_line.set_stroke(GREY_A, 1)
        v_line.move_to(midpoint(words[0].get_right(), words[1].get_left()))
        words.add(v_line)

        self.add(words)
