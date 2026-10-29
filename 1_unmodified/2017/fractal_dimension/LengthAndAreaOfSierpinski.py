# ==============================================================================
# Scene:      LengthAndAreaOfSierpinski
# Source:     videos/_2017/fractal_dimension.py (lines 1175-1221)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LengthAndAreaOfSierpinski.py LengthAndAreaOfSierpinski -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowSierpinskiCurve(Scene):
    CONFIG = {
        "max_order" : 8,
    }
    def construct(self):
        curve = self.get_curve(2)
        self.play(ShowCreation(curve, run_time = 2))
        for order in range(3, self.max_order + 1):
            self.play(Transform(
                curve, self.get_curve(order),
                run_time = 2
            ))
            self.wait()

    def get_curve(self, order):
        curve = SierpinskiCurve(order = order, monochromatic = True)
        curve.set_color(RED)
        return curve


class LengthAndAreaOfSierpinski(ShowSierpinskiCurve):
    CONFIG = {
        "curve_start_order" : 5,
        "sierpinski_start_order" : 4,
        "n_iterations" : 3,
    }
    def construct(self):
        length = OldTexText("Length = $\\infty$")
        length.shift(FRAME_X_RADIUS*LEFT/2).to_edge(UP)
        area = OldTexText("Area = $0$")
        area.shift(FRAME_X_RADIUS*RIGHT/2).to_edge(UP)
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        self.add(length, area, v_line)

        curve = self.get_curve(order = self.curve_start_order)
        sierp = self.get_sierpinski(order = self.sierpinski_start_order)
        self.add(curve, sierp)
        self.wait()

        for x in range(self.n_iterations):
            new_curve = self.get_curve(order = self.curve_start_order+x+1)
            alpha = (x+1.0)/self.n_iterations
            stroke_width = interpolate(3, 1, alpha)
            new_curve.set_stroke(width = stroke_width)

            new_sierp = self.get_sierpinski(
                order = self.sierpinski_start_order+x+1
            )
            self.play(
                Transform(curve, new_curve),
                Transform(sierp, new_sierp),
                run_time = 2
            )
        self.play(sierp.set_fill, None, 0)
        self.wait()

    def get_curve(self, order):
        # curve = ShowSierpinskiCurve.get_curve(self, order)
        curve = SierpinskiCurve(order = order)
        curve.set_height(4).center()
        curve.shift(FRAME_X_RADIUS*LEFT/2)
        return curve

    def get_sierpinski(self, order):
        result = Sierpinski(order = order)
        result.shift(FRAME_X_RADIUS*RIGHT/2)
        return result
