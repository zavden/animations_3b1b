# ==============================================================================
# Scene:      HighCurlFieldBreakingLayersLines
# Source:     videos/_2018/turbulence.py (lines 871-880)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/div_curl.py
#
# Run from this folder:
#     manimgl HighCurlFieldBreakingLayersLines.py HighCurlFieldBreakingLayersLines -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2018/div_curl.py -----

def four_swirls_function(point):
    x, y = point[:2]
    result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result



# ----- From _2018/turbulence.py -----

class HighCurlFieldBreakingLayers(Scene):
    CONFIG = {
        "flow_anim": move_submobjects_along_vector_field,
    }

    def construct(self):
        lines = VGroup(*[
            self.get_line()
            for x in range(20)
        ])
        lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        lines[0::2].set_color(BLUE)
        lines[1::2].set_color(RED)
        all_dots = VGroup(*it.chain(*lines))

        def func(p):
            vect = four_swirls_function(p)
            norm = get_norm(vect)
            if norm > 2:
                vect *= 4.0 / get_norm(vect)**2
            return vect

        self.add(lines)
        self.add(self.flow_anim(all_dots, func))
        self.wait(16)

    def get_line(self):
        line = VGroup(*[Dot() for x in range(100)])
        line.set_height(0.1)
        line.arrange(RIGHT, buff=0)
        line.set_width(10)
        return line


class HighCurlFieldBreakingLayersLines(HighCurlFieldBreakingLayers):
    CONFIG = {
        "flow_anim": move_points_along_vector_field
    }

    def get_line(self):
        line = Line(LEFT, RIGHT)
        line.insert_n_curves(500)
        line.set_width(5)
        return line
