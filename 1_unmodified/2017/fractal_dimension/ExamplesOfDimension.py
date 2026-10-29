# ==============================================================================
# Scene:      ExamplesOfDimension
# Source:     videos/_2017/fractal_dimension.py (lines 498-522)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExamplesOfDimension.py ExamplesOfDimension -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Britain(SVGMobject):
    CONFIG = {
        "file_name" : "Britain.svg",
        "stroke_width" : 0,
        "fill_color" : BLUE_D,
        "fill_opacity" : 1,
        "height" : 5,
        "mark_paths_closed" : True,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.set_points(self[0].get_points())
        self.submobjects = []
        self.set_height(self.height)
        self.center()


class ExamplesOfDimension(Scene):
    def construct(self):
        labels = VGroup(*[
            OldTexText("%s-dimensional"%s)
            for s in ("1.585", "1.262", "1.21")
        ])
        fractals = VGroup(*[
            Sierpinski(order = 7),
            KochSnowFlake(order = 5),
            Britain(stroke_width = 2, fill_opacity = 0)
        ])
        for fractal, vect in zip(fractals, [LEFT, ORIGIN, RIGHT]):
            fractal.to_edge(vect)
        fractals[2].shift(0.5*UP)
        fractals[1].shift(0.5*RIGHT)
        for fractal, label, vect in zip(fractals, labels, [DOWN, UP, DOWN]):
            label.next_to(fractal, vect)
            label.shift_onto_screen()
            self.play(
                ShowCreation(fractal),
                Write(label),
                run_time = 3
            )
            self.wait()
        self.wait()
