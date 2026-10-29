# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/eoc/chapter9.py (lines 2050-2129)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(GraphScene):
    CONFIG = {
        "x_min" : -0.2,
        "x_max" : 3.5,
        "x_leftmost_tick" : 0,
        "x_tick_frequency" : np.pi/4,
        "x_axis_label" : "",
        "y_min" : -0.75,
        "y_max" : 0.75,
        "y_axis_height" : 4.5,
        "y_tick_frequency" : 0.25,
        "y_axis_label" : ""
    }
    def construct(self):
        self.setup_axes()
        self.remove(self.axes)

        sine = self.get_graph(np.sin)
        rects = self.get_riemann_rectangles(
            sine,
            x_min = 0,
            x_max = np.pi,
            dx = 0.01,
            stroke_width = 0,
        )
        sine.add_to_back(rects)
        sine.add(self.axes.copy())
        sine.to_corner(UP+LEFT, buff = SMALL_BUFF)
        sine.scale(0.9)

        area = OldTexText("Area")
        area.scale(3)
        area.move_to(rects)

        cosine = self.get_graph(lambda x : -np.cos(x))
        cosine.set_stroke(GREEN, 8)
        line = self.get_secant_slope_group(
            0.75*np.pi, cosine, 
            dx = 0.01
        ).secant_line
        line.set_stroke(PINK, 7)
        cosine.add(line)
        cosine.add(self.axes.copy())
        cosine.scale(0.7)
        cosine.to_corner(DOWN+RIGHT, buff = MED_SMALL_BUFF)

        slope = OldTexText("Slope")
        slope.scale(3)
        # slope.next_to(cosine, LEFT, buff = 0)
        # slope.to_edge(DOWN)
        slope.to_corner(DOWN+RIGHT)

        double_arrow = DoubleArrow(
            area.get_bottom(),
            slope.get_left(),
            color = YELLOW,
            tip_length = 0.75,
            buff = MED_LARGE_BUFF
        )
        double_arrow.set_stroke(width = 18)

        triangle = Polygon(
            ORIGIN, UP, UP+RIGHT,
            stroke_width = 0,
            fill_color = BLUE_E,
            fill_opacity = 0.5,
        )
        triangle.stretch_to_fit_width(FRAME_WIDTH)
        triangle.stretch_to_fit_height(FRAME_HEIGHT)
        triangle.to_corner(UP+LEFT, buff = 0)

        alt_triangle = triangle.copy()
        alt_triangle.rotate(np.pi)
        alt_triangle.set_fill(BLACK, 1)

        self.add(
            triangle, sine, area, 
            alt_triangle, cosine, slope, 
            double_arrow,
        )
