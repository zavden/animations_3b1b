# ==============================================================================
# Scene:      SpecificCases
# Source:     videos/_2021/some1.py (lines 724-785)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpecificCases.py SpecificCases -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpecificCases(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        title = Text("Applications for optimization", font_size=72)
        title.to_edge(UP)
        self.add(title)

        grid = Square().get_grid(1, 2, buff=0)
        grid.set_height(6)
        grid.set_width(13, stretch=True)
        grid.to_edge(DOWN)
        grid.set_fill(BLACK, 1)

        labels = VGroup(
            Text("Profit maximization"),
            Text("Distance between curves"),
        )
        for label, square in zip(labels, grid):
            label.next_to(square.get_top(), DOWN)

        self.add(grid)
        self.add(labels)

        # Fill 'em
        r_axes = Axes(
            x_range=(-3, 3), y_range=(-3, 3),
            width=6, height=4.5,
            axis_config={"include_tip": False},
        )
        r_axes.move_to(grid[1], DOWN).shift(0.25 * UP)
        circle = Circle()
        circle.set_height(get_norm(r_axes.c2p(0, 0) - r_axes.c2p(0, 2)))
        circle.move_to(r_axes.c2p(1, 1))
        circle.set_stroke(YELLOW)
        parabola = r_axes.get_graph(
            lambda x: 0.2 * (x**2 - 4)
        )
        parabola.set_stroke(RED_D)
        smallest_line = Line(
            circle.pfp(0.83),
            parabola.pfp(0.76),
            stroke_width=3
        )

        self.add(circle, parabola, smallest_line)

        l_axes = Axes(
            (0, 10),
            (-3, 8),
            width=6, height=4.5,
        )
        l_axes.move_to(grid[0], DOWN).shift(0.25 * UP)
        x_label = Text("production", font_size=24)
        x_label.next_to(l_axes.x_axis, DOWN, SMALL_BUFF, aligned_edge=RIGHT)
        y_label = Text("profit", font_size=24)
        y_label.next_to(l_axes.y_axis, RIGHT, SMALL_BUFF, aligned_edge=UP)
        graph = l_axes.get_graph(
            lambda x: -0.07 * x * (x - 4) * (x - 9.5)
        )
        graph.set_stroke(GREEN, 3)

        self.add(l_axes, x_label, y_label, graph)
