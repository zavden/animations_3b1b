# ==============================================================================
# Scene:      GlimpseOfNextVideo
# Source:     videos/_2019/bayes/part1.py (lines 4114-4198)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl GlimpseOfNextVideo.py GlimpseOfNextVideo -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Restore the compatible GraphScene base instead of the repo's empty stub.
# ==============================================================================

from manim_imports_ext import *
import scipy.integrate

HYPOTHESIS_COLOR = YELLOW


EVIDENCE_COLOR1 = BLUE_C


# CHANGE: restore the GraphScene base; the repo stub lost setup_axes and its helpers.
from cairo_compat import GraphScene as CairoGraphScene

class GraphScene(CairoGraphScene):
    pass


class GlimpseOfNextVideo(GraphScene):
    CONFIG = {
        "x_axis_label": "",
        "y_axis_label": "",
        "x_min": 0,
        "x_max": 15,
        "x_axis_width": 12,
        "y_min": 0,
        "y_max": 1.0,
        "y_axis_height": 6,
        "y_tick_frequency": 0.125,
        "add_x_coords": True,
        "formula_position": ORIGIN,
        "dx": 0.2,
    }

    def setup(self):
        super().setup()
        self.setup_axes()
        self.y_axis.add_numbers(
            0.25, 0.5, 0.75, 1,
            num_decimal_places=2,
            direction=LEFT,
        )
        if self.add_x_coords:
            self.x_axis.add_numbers(*range(1, 15),)

    def construct(self):
        f1 = self.prior

        def f2(x):
            return f1(x) * self.likelihood(x)

        pe = scipy.integrate.quad(f2, 0, 20)[0]

        graph1 = self.get_graph(f1)
        graph2 = self.get_graph(f2)

        rects1 = self.get_riemann_rectangles(graph1, dx=self.dx)
        rects2 = self.get_riemann_rectangles(graph2, dx=self.dx)

        rects1.set_color(YELLOW_D)
        rects2.set_color(BLUE)
        for rects in rects1, rects2:
            rects.set_stroke(WHITE, 1)

        rects1.save_state()
        rects1.stretch(0, 1, about_edge=DOWN)

        formula = self.get_formula()

        self.play(
            FadeInFromDown(formula[:4]),
            Restore(rects1, lag_ratio=0.05, run_time=2)
        )
        self.wait()
        self.add(rects1.copy().set_opacity(0.4))
        self.play(
            FadeInFromDown(formula[4:10]),
            Transform(rects1, rects2),
        )
        self.wait()
        self.play(
            rects1.stretch, 1 / pe, 1, {"about_edge": DOWN},
            Write(formula[10:], run_time=1)
        )
        self.wait()

    def get_formula(self):
        formula = OldTex(
            "p(H) p(E|H) \\over p(E)",
            tex_to_color_map={
                "H": HYPOTHESIS_COLOR,
                "E": EVIDENCE_COLOR1,
            },
            isolate=list("p(|)")
        )
        formula.move_to(self.formula_position)
        return formula

    def prior(self, x):
        return (x**3 / 6) * np.exp(-x)

    def likelihood(self, x):
        return np.exp(-0.5 * x)
