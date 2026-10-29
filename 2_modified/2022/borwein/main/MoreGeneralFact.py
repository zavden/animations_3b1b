# ==============================================================================
# Scene:      MoreGeneralFact
# Source:     videos/_2022/borwein/main.py (lines 1064-1151)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MoreGeneralFact.py MoreGeneralFact -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - TransformMatchingTex -> TransformMatchingShapes (TransformMatchingTex requires a StringMobject and OldTex is not one; it matches glyphs by shape)
#   - brace.get_tex(...)[0] -> brace.get_tex(...): the new Tex is made of loose glyphs and the [0] left only the first one (IndexError in sum_tex[-2])
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


class MoreGeneralFact(InteractiveScene):
    dx = 0.025

    def construct(self):
        # Equation
        inters = VGroup(*(
            get_multi_sinc_integral(range(1, n, 2), rhs=R"= \pi")
            for n in range(3, 11, 2)
        ))
        inters.scale(0.75)
        inters.to_edge(UP)

        # Graph
        axes = Axes((-4 * PI, 4 * PI, PI), (-0.5, 1, 0.5), width=FRAME_WIDTH + 1, height=4)
        axes.x_axis.add_numbers(unit=PI, unit_tex=R"\pi")
        axes.to_edge(DOWN)

        graphs = VGroup(*(
            axes.get_graph(lambda x, n=n: multi_sinc(x, n))
            for n in range(1, 5)
        ))
        graphs.set_stroke(WHITE, 2)
        areas = VGroup(*(
            axes.get_riemann_rectangles(
                graph, colors=(BLUE_D, BLUE_D), dx=self.dx, fill_opacity=1,
            )
            for graph in graphs
        ))
        for area in areas:
            area.sort(lambda p: abs(p[0]))

        self.add(areas[0], axes, graphs[0], inters[0])

        for i in range(3):
            self.play(
                ReplacementTransform(areas[i], areas[i + 1]),
                # CHANGE: TransformMatchingTex only accepts StringMobject (new Tex); with OldTex TransformMatchingShapes is used (it matches glyphs by shape)
                TransformMatchingShapes(inters[i], inters[i + 1]),
                ReplacementTransform(graphs[i], graphs[i + 1]),
            )
            self.add(areas[i + 1], axes, graphs[i + 1], inters[i + 1])
        self.wait()

        # Generalize
        inner_group = inters[-1][2:5]
        rect = SurroundingRectangle(inner_group, buff=SMALL_BUFF).set_stroke(YELLOW, 1)
        brace = Brace(rect)
        brace_text = brace.get_text("Nothing special", font_size=36)

        general_group = OldTex(
            R"\frac{\sin(a_1 x)}{a_1 x}",
            R"\cdots",
            R"\frac{\sin(a_n x)}{a_n x}",
        )
        general_group.set_submobject_colors_by_gradient(TEAL, GREEN)
        general_group.match_height(inner_group)
        general_group.move_to(inner_group, LEFT)

        self.play(
            ShowCreation(rect),
            GrowFromCenter(brace),
            FadeIn(brace_text, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            FadeOut(inner_group, UP),
            FadeIn(general_group, UP),
            rect.animate.match_points(SurroundingRectangle(general_group, buff=SMALL_BUFF)),
            brace.animate.become(Brace(general_group, DOWN, buff=MED_SMALL_BUFF)),
            FadeOut(brace_text),
            inters[-1][5:].animate.next_to(general_group, RIGHT, SMALL_BUFF),
        )
        self.wait()

        # Sum condition
        # CHANGE: Brace.get_tex now returns a new Tex of loose glyphs: the [0] (which used to be the whole formula) left only the first letter
        sum_tex = brace.get_tex(R"a_1 + \cdots + a_n < 1")
        lt = OldTex("<")
        eq = inters[-1][-1][0]
        lt.move_to(eq)

        self.play(FadeIn(sum_tex, 0.5 * DOWN))
        self.play(FlashAround(inters[-1][-1], run_time=2, time_width=1))
        self.wait()
        self.play(Rotate(sum_tex[-2], PI))
        self.play(
            FadeOut(eq, 0.5 * UP),
            FadeIn(lt, 0.5 * UP),
        )
        self.wait()
