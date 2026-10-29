# ==============================================================================
# Scene:      OneDRegionBoundary
# Source:     videos/_2018/WindingNumber_G.py (lines 1489-1593)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl OneDRegionBoundary.py OneDRegionBoundary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class OneDRegionBoundary(Scene):
    CONFIG = {
        "graph_color" : BLUE,
        "region_rect_height" : 0.1,
    }
    def construct(self):
        x0 = self.x0 = 3 
        x1 = self.x1 = 6
        fx0 = self.fx0 = -2
        fx1 = self.fx1 = 2

        axes = self.axes = Axes(
            x_min = -1, x_max = 10,
            y_min = -3, y_max = 3,
        )
        axes.center()
        axes.set_stroke(width = 2)

        input_word = OldTexText("Input")
        input_word.next_to(axes.x_axis, UP, SMALL_BUFF, RIGHT)
        output_word = OldTexText("Output")
        output_word.next_to(axes.y_axis, UP)
        axes.add(input_word, output_word)
        self.add(axes)

        graph = self.get_graph_part(1, 1)
        alt_graphs = [
            self.get_graph_part(*points)
            for points in [
                (-1, -2),
                (-1, -1, -1),
                (1, 1, 1),
                (-0.75, 0, 1.75),
                (-3, -2, -1),
            ]
        ]

        #Region and boundary
        line = Line(axes.coords_to_point(x0, 0), axes.coords_to_point(x1, 0))
        region = Rectangle(
            stroke_width = 0,
            fill_color = YELLOW,
            fill_opacity = 0.5,
            height = self.region_rect_height
        )
        region.match_width(line, stretch = True)
        region.move_to(line)

        region_words = OldTexText("Input region")
        region_words.set_width(0.8*region.get_width())
        region_words.next_to(region, UP)

        x0_arrow, x1_arrow = arrows = VGroup(*[
            Arrow(
                axes.coords_to_point(x, 0),
                axes.coords_to_point(x, fx),
                color = color,
                buff = 0
            )
            for x, fx, color in [(x0, fx0, RED), (x1, fx1, GREEN)]
        ])
        minus = OldTex("-")
        minus.match_color(x0_arrow)
        minus.next_to(x0_arrow, UP)
        plus = OldTex("+")
        plus.match_color(x1_arrow)
        plus.next_to(x1_arrow, DOWN)
        signs = VGroup(plus, minus)


        self.play(
            GrowFromCenter(region),
            FadeIn(region_words)
        )
        self.wait()
        self.play(*it.chain(
            list(map(GrowArrow, arrows)),
            list(map(Write, signs))
        ))
        self.wait()
        self.play(
            ShowCreation(graph), 
            FadeOut(region_words),
        )
        self.wait()
        for alt_graph in alt_graphs + alt_graphs:
            self.play(Transform(graph, alt_graph, path_arc = 0.1*TAU))
        self.wait()


    ###

    def get_graph_part(self, *interim_values):
        result = VMobject()
        result.set_stroke(self.graph_color, 3)
        result.set_fill(opacity = 0)
        values = [self.fx0] + list(interim_values) + [self.fx1]
        result.set_points_smoothly([
            self.axes.coords_to_point(x, fx)
            for x, fx in zip(
                np.linspace(self.x0, self.x1, len(values)),
                values
            )
        ])
        return result
