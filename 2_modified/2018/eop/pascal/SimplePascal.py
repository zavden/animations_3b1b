# ==============================================================================
# Scene:      SimplePascal
# Source:     videos/_2018/eop/pascal.py (lines 98-162)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SimplePascal.py SimplePascal -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - added rainbow_color/graded_color (+GRADE_COLOR_1/2) copied from eop/reusables/eop_helpers.py, which the file never imported
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.combinatorics import *

# CHANGE: rainbow_color and graded_color live in eop/reusables/eop_helpers.py, which this file never imported (the original repo file relied on a Cairo-era path); copied here with the colors they use
GRADE_COLOR_1 = RED_E
GRADE_COLOR_2 = BLUE_C

def rainbow_color(alpha):
    nb_colors = 100
    rainbow = color_gradient([RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE], nb_colors)
    rainbow = np.append(rainbow, PURPLE)
    index = int(alpha * nb_colors)
    return rainbow[index]

def graded_color(n, k):
    if n != 0:
        alpha = float(k) / n
    else:
        alpha = 0.5
    return interpolate_color(GRADE_COLOR_1, GRADE_COLOR_2, alpha)


def graded_square(n,k):
    return Square(
        side_length = 1, 
        fill_color = graded_color(n,k), 
        fill_opacity = 1, 
        stroke_width = 1
    )


class SimplePascal(Scene):

    def build_new_pascal_row(self,old_pt):

        lowest_row_copy = old_pt.get_lowest_row().copy()
        self.add(lowest_row_copy)

        n = old_pt.nrows - 1
        lowest_row_copy1 = old_pt.get_lowest_row()
        lowest_row_copy2 = lowest_row_copy1.copy()


        start_mob = VGroup(lowest_row_copy1, lowest_row_copy2)
        self.add(start_mob)

        new_pt = old_pt.copy()
        cell_height = old_pt.height / old_pt.nrows
        cell_width = old_pt.width / old_pt.nrows
        new_pt.nrows += 1
        new_pt.height = new_pt.nrows * cell_height
        new_pt.width = new_pt.nrows * cell_width

        new_pt.init_points()
        # align with original (copy got centered on screen)
        c1 = new_pt.coords_to_mobs[0][0].get_center()
        c2 = old_pt.coords_to_mobs[0][0].get_center()
        v = c2 - c1
        new_pt.shift(v)

        new_row_left_copy = VGroup(*[
            new_pt.coords_to_mobs[n+1][k]
            for k in range(0,n+1)
        ])

        new_row_right_copy = VGroup(*[
            new_pt.coords_to_mobs[n+1][k]
            for k in range(1,n+2)
        ]).copy()

        target_mob = VGroup(new_row_left_copy, new_row_right_copy)
        self.play(Transform(start_mob, target_mob))

        return new_pt



    def construct(self):

        cell_height = 1
        cell_width = 1
        nrows = 1
        pt = GeneralizedPascalsTriangle(
            nrows = nrows, 
            height = nrows * cell_height, 
            width = nrows * cell_width, 
            submob_class = graded_square,
            portion_to_fill = 0.9
        )
        pt.shift(3 * UP)
        self.add(pt)
        lowest_row_copy = pt.get_lowest_row().copy()
        self.add(lowest_row_copy)
        #self.play(BuildNewPascalRow(pt, duplicate_row = lowest_row_copy))
        for i in range(7):
            pt = self.build_new_pascal_row(pt)
