# ==============================================================================
# Scene:      CompareWaysToWriteExponentials
# Source:     videos/_2017/eoc/chapter5.py (lines 1521-1580)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CompareWaysToWriteExponentials.py CompareWaysToWriteExponentials -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Python 3 zip is not subscriptable
# ==============================================================================

from manim_imports_ext import *

class CompareWaysToWriteExponentials(GraphScene):
    CONFIG = {
        "y_max" : 50,
        "y_tick_frequency" : 5,
        "x_max" : 7,
    }
    def construct(self):
        self.setup_axes()
        bases = list(range(2, 7))
        graphs = [
            self.get_graph(lambda t : base**t, color = GREEN)
            for base in bases
        ]
        graph = graphs[0]

        a_to_t = OldTex("a^t")
        a_to_t.move_to(self.coords_to_point(6, 45))

        cross = OldTex("\\times")
        cross.set_color(RED)
        cross.replace(a_to_t, stretch = True)
        e_to_ct = OldTex("e^", "{c", "t}")
        e_to_ct.set_color_by_tex("c", BLUE)
        e_to_ct.scale(1.5)
        e_to_ct.next_to(a_to_t, DOWN)

        equations = VGroup()
        for base in bases:
            log_str =  "%.4f\\dots"%np.log(base)
            equation = OldTex(
                str(base), "^t", "=",
                "e^", "{(%s)"%log_str, "t}", 
            )
            equation.set_color_by_tex(log_str, BLUE)
            equation.scale(1.2)
            equations.add(equation)

        equation = equations[0]
        equations.next_to(e_to_ct, DOWN, LARGE_BUFF, LEFT)

        self.play(
            ShowCreation(graph),
            Write(
                a_to_t,
                rate_func = squish_rate_func(smooth, 0.5, 1) 
            ),
            run_time = 2
        )
        self.play(Write(cross, run_time = 2))
        self.play(Write(e_to_ct, run_time = 2))
        self.wait(2)
        self.play(Write(equation))
        self.wait(2)
        # CHANGE: Python 3 zip is not subscriptable
        for new_graph, new_equation in list(zip(graphs, equations))[1:]:
            self.play(
                Transform(graph, new_graph),
                Transform(equation, new_equation)
            )
            self.wait(2)
        self.wait()
