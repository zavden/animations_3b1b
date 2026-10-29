# ==============================================================================
# Scene:      InsertTwoCos
# Source:     videos/_2022/borwein/main.py (lines 588-646)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InsertTwoCos.py InsertTwoCos -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex requires a StringMobject and OldTex is not one; it matches glyphs by shape)
# ==============================================================================

from manim_imports_ext import *

def sinc(x):
    return np.sinc(x / PI)


def multi_sinc(x, n):
    return np.prod([sinc(x / (2 * k + 1)) for k in range(n)])


def get_sinc_tex(k=1):
    div_k = f"/ {k}" if k > 1 else ""
    return Rf"{{\sin(x {div_k}) \over x {div_k}}}"


def get_multi_sinc_integral(ks=[1], dots_at=None, rhs="", insertion=""):
    result = OldTex(
        R"\int_{-\infty}^\infty",
        insertion,
        *(
            get_sinc_tex(k) if k != dots_at else R"\dots"
            for k in ks
        ),
        "dx",
        rhs,
    )
    t2c = {
        R"\sin": BLUE,
        "x / 3": TEAL,
        "x / 5": GREEN_B,
        "x / 7": GREEN_C,
        "x / 9": interpolate_color(GREEN, YELLOW, 1 / 3),
        "x / 11": interpolate_color(GREEN, YELLOW, 2 / 3),
        "x / 13": YELLOW,
        "x / 15": RED_B,
    }
    for tex, color in t2c.items():
        result.set_color_by_tex(tex, color)
    return result


class InsertTwoCos(InteractiveScene):
    dx = 0.025

    def construct(self):
        # Formulas
        n_range = list(range(3, 17, 2))
        integrals = VGroup(
            get_multi_sinc_integral([1], rhs=R"= \pi"),
            *(
                get_multi_sinc_integral(range(1, n, 2), insertion=R"2\cos(x)", rhs=R"= \pi")
                for n in n_range
            )
        )
        integrals.scale(0.75)
        for inter in integrals:
            inter.to_edge(UP)

        self.add(integrals[0])

        # Graphs
        axes = Axes((-4 * PI, 4 * PI, PI), (-2, 2, 1), width=FRAME_WIDTH + 1, height=6)
        axes.to_edge(DOWN, buff=SMALL_BUFF)
        axes.x_axis.add_numbers(unit_tex=R"\pi", unit=PI)

        graphs = VGroup(
            axes.get_graph(sinc),
            *(
                axes.get_graph(
                    lambda x, n=n: 2 * math.cos(x) * multi_sinc(x, n + 1),
                    x_range=(-4 * PI, 4 * PI, 0.01)
                )
                for n in range(len(n_range))
            )
        )
        graphs.set_stroke(WHITE, 2)

        areas = VGroup(*(
            axes.get_riemann_rectangles(
                graph,
                dx=self.dx,
                colors=(BLUE_D, BLUE_D),
                fill_opacity=1
            )
            for graph in graphs
        ))

        self.add(areas[0], axes, graphs[0])

        # Progress
        for i in range(len(integrals) - 1):
            self.play(
                # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
                TransformMatchingShapes(integrals[i], integrals[i + 1]),
                ReplacementTransform(graphs[i], graphs[i + 1]),
                ReplacementTransform(areas[i], areas[i + 1]),
            )
            self.add(areas[i + 1], axes, graphs[i + 1])
            if i == 0:
                self.play(FlashAround(integrals[i + 1][1], run_time=2, time_width=1))
            self.wait()
