# ==============================================================================
# Scene:      PascalNetScene
# Source:     videos/_2018/eop/pascal.py (lines 168-218)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PascalNetScene.py PascalNetScene -w -m --fps 15
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


nb_levels = 5


dev_x_step = 2


dev_y_step = 5


class PascalNetScene(Scene):

    def construct(self):

        unit_width = 0.25
        top_height = 4.0
        level_height = 2.0 * top_height / nb_levels

        start_points = np.array([top_height * UP])

        dev_start = start_points[0]

        j = 0

        for n in range(nb_levels):

            half_width = 0.5 * (n + 0.5) * unit_width

            stop_points_left = start_points.copy()
            stop_points_left[:,0] -= 0.5 * unit_width
            stop_points_left[:,1] -= level_height

            stop_points_right = start_points.copy()
            stop_points_right[:,0] += 0.5 * unit_width
            stop_points_right[:,1] -= level_height
            
            for (p,q) in zip(start_points,stop_points_left):
                alpha = np.abs((p[0]+q[0])/2) / half_width
                color = rainbow_color(alpha)
                line = Line(p,q, stroke_color = color)
                self.add(line)

            for (i,(p,q)) in enumerate(zip(start_points,stop_points_right)):
                alpha = np.abs((p[0]+q[0])/2) / half_width
                color = rainbow_color(alpha)
                line = Line(p,q, stroke_color = color)
                self.add(line)

            if (n + 1) % dev_y_step == 0 and n != 1:
                j += dev_x_step
                dev_stop = stop_points_left[j]
                line = Line(dev_start,dev_stop,stroke_color = WHITE)
                self.add(line)
                dot = Dot(dev_stop, fill_color = WHITE)
                self.add_foreground_mobject(dot)
                dev_start = dev_stop

            start_points = np.append(stop_points_left,[stop_points_right[-1]], axis = 0)


        self.wait()
