# ==============================================================================
# Scene:      NDimensionalBallGrid
# Source:     videos/_2023/gauss_int/supplements.py (lines 1146-1235)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NDimensionalBallGrid.py NDimensionalBallGrid -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class NDimensionalBallGrid(InteractiveScene):
    def construct(self):
        # Setup grid
        N_terms = 7
        grid = Square().get_grid(3, N_terms + 1, buff=0, group_by_rows=True)
        grid.set_stroke(WHITE, 1)
        for row in grid:
            row[0].stretch(1.5, 0, about_edge=RIGHT)
        grid.set_width(FRAME_WIDTH - 1)
        grid.center().to_edge(DOWN, buff=1.0)
        self.add(grid)

        # Content
        kw = dict(t2c={"r": BLUE})
        numbers = VGroup(
            *(Integer(n) for n in range(1, 6)),
            Tex(R"\cdots"),
            Text(R"N"),
        )
        interiors = VGroup(
            Tex(R"2r", **kw),
            Tex(R"\pi r^2", **kw),
            Tex(R"\frac{4}{3} \pi r^3", **kw),
            Tex(R"\frac{1}{2} \pi^2 r^4", **kw),
            Tex(R"\frac{8}{15} \pi^2 r^5", **kw),
            Tex(R"\cdots"),
            Tex(R"\frac{\pi^{n / 2}}{(n / 2)!} r^n", **kw),
        )
        exteriors = VGroup(
            Tex(R"2", **kw),
            Tex(R"2 \pi r", **kw),
            Tex(R"4 \pi r^2", **kw),
            Tex(R"2 \pi^2 r^3", **kw),
            Tex(R"\frac{8}{3} \pi^2 r^4", **kw),
            Tex(R"\cdots"),
            Tex(R"n \frac{\pi^{n / 2}}{(n / 2)!} r^{n - 1}", **kw),
        )
        for group, row in zip([numbers, interiors, exteriors], grid):
            for elem, square in zip(group, row[1:]):
                elem.set_max_width(0.8 * square.get_width())
                elem.move_to(square)

        row_titles = VGroup(
            Text("Dimension"),
            TexText(R"Volume of \\ $n$-ball", font_size=30),
            TexText(R"Volume of \\ $n$-ball boundary", font_size=30),
        )
        for title, row in zip(row_titles, grid):
            title.set_max_width(0.8 * row[0].get_width())
            title.move_to(row[0])

        self.add(row_titles, numbers)

        # Shapes
        line = Line()
        line.set_stroke(BLUE_A, 3)
        one_ball = VGroup(
            line,
            Dot(line.get_start()),
            Dot(line.get_end())
        )
        one_ball[1:].set_color(BLUE)

        circle = Circle()
        circle.set_stroke(BLUE, 2)
        circle.set_fill(BLUE, 0.5)

        sphere = Sphere(color=BLUE)
        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(WHITE, 0.5, 0.5)
        ball = Group(sphere, mesh)
        ball.rotate(70 * DEGREES, LEFT)

        shapes = Group(
            one_ball, circle, ball,
            Randolph("shruggie"),
            Tex(R"\dots"),
            *VectorizedPoint().replicate(2),
        )
        for shape, square in zip(shapes, grid[0][1:]):
            shape.set_max_width(0.7 * square.get_width())
            shape.move_to(square.get_top())
            shape.shift(0.6 * shape.get_width() * UP)
        shapes[4].match_y(shapes[0])

        # Animate in
        for shape, interior, exterior in zip(shapes, interiors, exteriors):
            self.play(FadeIn(shape), FadeIn(interior))
            self.play(TransformMatchingTex(interior.copy(), exterior, run_time=1))
        self.wait()
