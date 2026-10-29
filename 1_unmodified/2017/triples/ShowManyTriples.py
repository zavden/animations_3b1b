# ==============================================================================
# Scene:      ShowManyTriples
# Source:     videos/_2017/triples.py (lines 186-266)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowManyTriples.py ShowManyTriples -w -m --fps 15
# ==============================================================================

import fractions
from manim_imports_ext import *

A_COLOR = BLUE


B_COLOR = GREEN


C_COLOR = YELLOW


SIDE_COLORS = [A_COLOR, B_COLOR, C_COLOR]


class ShowManyTriples(Scene):
    def construct(self):
        triples = [
            (u**2 - v**2, 2*u*v, u**2 + v**2)
            for u in range(1, 15)
            for v in range(1, u)
            if fractions.gcd(u, v) == 1 and not (u%2 == v%2)
        ][:40]
        triangles = VGroup()
        titles = VGroup()
        for i, (a, b, c) in enumerate(triples):
            triangle = Polygon(ORIGIN, a*RIGHT, a*RIGHT+b*UP)
            triangle.set_color(WHITE)
            max_width = max_height = 4
            triangle.set_height(max_height)
            if triangle.get_width() > max_width:
                triangle.set_width(max_width)
            triangle.move_to(2*RIGHT)
            num_strings = list(map(str, (a, b, c)))
            labels = list(map(Tex, num_strings))
            for label, color in zip(labels, SIDE_COLORS):
                label.set_color(color)
            labels[0].next_to(triangle, DOWN)
            labels[1].next_to(triangle, RIGHT)
            labels[2].next_to(triangle.get_center(), UP+LEFT)
            triangle.add(*labels)

            title = OldTex(
                str(a), "^2", "+", str(b), "^2", "=", str(c), "^2"
            )
            for num, color in zip([a, b, c], SIDE_COLORS):
                title.set_color_by_tex(str(num), color)
            title.next_to(triangle, UP, LARGE_BUFF)
            title.generate_target()
            title.target.scale(0.5)

            title.target.move_to(
                (-FRAME_X_RADIUS + MED_LARGE_BUFF + 2.7*(i//8))*RIGHT + \
                (FRAME_Y_RADIUS - MED_LARGE_BUFF - (i%8))*UP,
                UP+LEFT
            )

            triangles.add(triangle)
            titles.add(title)

        triangle = triangles[0]
        title = titles[0]
        self.play(
            Write(triangle),
            Write(title),
            run_time = 2,
        )
        self.wait()
        self.play(MoveToTarget(title))
        for i in range(1, 17):
            new_triangle = triangles[i]
            new_title = titles[i]
            if i < 4:
                self.play(
                    Transform(triangle, new_triangle),
                    FadeIn(new_title)
                )
                self.wait()
                self.play(MoveToTarget(new_title))
            else:
                self.play(
                    Transform(triangle, new_triangle),
                    FadeIn(new_title.target)
                )
                self.wait()
        self.play(FadeOut(triangle))
        self.play(LaggedStartMap(
            FadeIn, 
            VGroup(*[
                title.target 
                for title in titles[17:]
            ]),
            run_time = 5
        ))

        self.wait(2)
