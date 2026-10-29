# ==============================================================================
# Scene:      ReasonForSolution
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 177-309)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part1/shared_constructs.py
#
# Run from this folder:
#     manimgl ReasonForSolution.py ReasonForSolution -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part1/shared_constructs.py -----

def get_ode():
    tex_config = {
        "tex_to_color_map": {
            "{\\theta}": BLUE,
            "{\\dot\\theta}": RED,
            "{\\ddot\\theta}": YELLOW,
            "{t}": WHITE,
            "{\\mu}": WHITE,
        }
    }
    ode = OldTex(
        "{\\ddot\\theta}({t})", "=",
        "-{\\mu} {\\dot\\theta}({t})",
        "-{g \\over L} \\sin\\big({\\theta}({t})\\big)",
        **tex_config,
    )
    return ode



# ----- From _2019/diffyq/part1/wordy_scenes.py -----

class ReasonForSolution(Scene):
    def construct(self):
        # Words
        eq_word = OldTexText("Differential\\\\Equation")
        s_word = OldTexText("Solution")
        u_word = OldTexText("Understanding")
        c_word = OldTexText("Computation")
        cu_group = VGroup(u_word, c_word)
        cu_group.arrange(DOWN, buff=2)
        group = VGroup(eq_word, s_word, cu_group)
        group.arrange(RIGHT, buff=2)
        # words = VGroup(eq_word, s_word, u_word, c_word)

        # Arrows
        arrows = VGroup(
            Arrow(eq_word.get_right(), s_word.get_left()),
            Arrow(s_word.get_right(), u_word.get_left()),
            Arrow(s_word.get_right(), c_word.get_left()),
        )
        arrows.set_color(GREY_B)
        new_arrows = VGroup(
            Arrow(
                eq_word.get_corner(UR),
                u_word.get_left(),
                path_arc=-60 * DEGREES,
            ),
            Arrow(
                eq_word.get_corner(DR),
                c_word.get_left(),
                path_arc=60 * DEGREES,
            ),
        )
        new_arrows.set_color(BLUE)

        # Define first examples
        t2c = {
            "{x}": BLUE,
            "{\\dot x}": RED,
        }
        equation = OldTex(
            "{\\dot x}(t) = k {x}(t)",
            tex_to_color_map=t2c,
        )
        equation.next_to(eq_word, DOWN)
        solution = OldTex(
            "{x}(t) = x_0 e^{kt}",
            tex_to_color_map=t2c,
        )
        solution.next_to(s_word, DOWN, MED_LARGE_BUFF)
        equation.align_to(solution, DOWN)

        axes = Axes(
            x_min=-1,
            x_max=5.5,
            y_min=-1,
            y_max=4.5,
            y_axis_config={"unit_size": 0.5}
        )
        axes.set_stroke(width=2)
        graph_line = axes.get_graph(
            lambda x: np.exp(0.4 * x)
        )
        graph_line.set_stroke(width=2)
        graph = VGroup(axes, graph_line)
        graph.scale(0.5)
        graph.next_to(u_word, UP)

        computation = OldTex(
            # "\\displaystyle "
            "e^x = \\sum_{n=0}^\\infty "
            "\\frac{x^n}{n!}"
        )
        computation.next_to(c_word, DOWN)

        first_examples = VGroup(
            equation, solution, graph, computation
        )

        # Second example
        ode = get_ode()
        ode.scale(0.75)
        second_examples = VGroup(
            ode,
            OldTex("???").set_color(GREY_B),
            ScreenRectangle(
                height=2,
                stroke_width=1,
            ),
        )
        for fe, se in zip(first_examples, second_examples):
            se.move_to(fe, DOWN)

        ode.shift(2 * SMALL_BUFF * DOWN)
        ode.add_to_back(BackgroundRectangle(ode[-4:]))

        self.add(eq_word)
        self.add(equation)
        self.play(
            FadeIn(s_word, LEFT),
            GrowArrow(arrows[0]),
            TransformFromCopy(equation, solution)
        )
        self.wait()
        self.play(
            FadeIn(c_word, UL),
            GrowArrow(arrows[2]),
            FadeIn(computation, UP)
        )
        self.wait()
        self.play(
            FadeIn(u_word, DL),
            GrowArrow(arrows[1]),
            FadeInFromDown(graph)
        )
        self.wait(2)

        self.play(
            FadeOut(first_examples),
            FadeIn(second_examples[:2])
        )
        self.wait()
        self.play(
            arrows.fade, 0.75,
            s_word.fade, 0.75,
            second_examples[1].fade, 0.75,
            ShowCreation(new_arrows[0]),
            FadeIn(second_examples[2])
        )
        self.play(
            ShowCreation(new_arrows[1]),
            Animation(second_examples),
        )
        self.wait()
