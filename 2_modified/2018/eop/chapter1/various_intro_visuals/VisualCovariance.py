# ==============================================================================
# Scene:      VisualCovariance
# Source:     videos/_2018/eop/chapter1/various_intro_visuals.py (lines 61-111)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl VisualCovariance.py VisualCovariance -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
# ==============================================================================

from manim_imports_ext import *
# CHANGE: Removed Cairo-package imports (mobject.*, utils.*, constants, animation.*, for_3b1b_videos.*): they do not exist in ManimGL and manim_imports_ext already provides these names
from random import *
import itertools as it

class VisualCovariance(Scene):


    def construct(self):

        size = 4
        square = Square(side_length = size)
        n_points = 30
        cloud = VGroup(*[
            Dot((x + 0.8*y) * RIGHT + y * UP).set_fill(WHITE, 1)
            for x, y in zip(
                np.random.normal(0, 1, n_points),
                np.random.normal(0, 1, n_points)
            )
        ])
        self.add_foreground_mobject(cloud)

        x_axis = Vector(8*RIGHT, color = WHITE).move_to(2.5*DOWN)
        y_axis = Vector(5*UP, color = WHITE).move_to(4*LEFT)

        self.add(x_axis, y_axis)


        random_pairs = [ (p1, p2) for (p1, p2) in
            it.combinations(cloud, 2)
        ]
        np.random.shuffle(random_pairs)



        for (p1, p2) in random_pairs:
            c1, c2 = p1.get_center(), p2.get_center()
            x1, y1, x2, y2 = c1[0], c1[1], c2[0], c2[1]
            if x1 >= x2:
                continue
            if y2 > y1:
                # make a red rect
                color = RED
                opacity = 0.1
               
            elif y2 < y1:
                # make a blue rect
                color = BLUE
                opacity = 0.2

            rect = Rectangle(width = x2 - x1, height = abs(y2 - y1))
            rect.set_fill(color = color, opacity = opacity)
            rect.set_stroke(width = 0)
            rect.move_to((c1+c2)/2)

            self.play(FadeIn(rect), run_time = 0.05)
