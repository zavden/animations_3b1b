# ==============================================================================
# Scene:      InvestmentGrowth
# Source:     videos/_2019/diffyq/part3/staging.py (lines 677-796)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InvestmentGrowth.py InvestmentGrowth -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InvestmentGrowth(Scene):
    CONFIG = {
        "output_tex": "{M}",
        "output_color": GREEN,
        "initial_value": 1,
        "initial_value_tex": "{M_0}",
        "k": 0.05,
        "k_tex": "0.05",
        "total_time": 43,
        "time_rate": 3,
    }

    def construct(self):
        # Axes
        axes = Axes(
            x_min=0,
            x_max=self.total_time,
            y_min=0,
            y_max=6,
            x_axis_config={
                "unit_size": 0.3,
                "tick_size": 0.05,
                "big_tick_numbers": range(
                    0, self.total_time, 5
                )
            }
        )
        axes.to_corner(DL, buff=LARGE_BUFF)

        time_label = OldTexText("Time")
        time_label.next_to(
            axes.x_axis.get_right(),
            UP, MED_LARGE_BUFF
        )
        time_label.shift_onto_screen()
        axes.x_axis.add(time_label)
        money_label = OldTex(self.output_tex)
        money_label.set_color(self.output_color)
        money_label.next_to(
            axes.y_axis.get_top(),
            UP,
        )
        axes.y_axis.add(money_label)

        # Graph
        graph = axes.get_graph(
            lambda x: self.initial_value * np.exp(self.k * x)
        )
        graph.set_color(self.output_color)
        full_graph = graph.copy()
        time_tracker = self.get_time_tracker()
        graph.add_updater(lambda m: m.pointwise_become_partial(
            full_graph, 0,
            np.clip(
                time_tracker.get_value() / self.total_time,
                0, 1,
            )
        ))

        # Equation
        tex_kwargs = {
            "tex_to_color_map": {
                self.output_tex: self.output_color,
                self.initial_value_tex: BLUE,
            }
        }
        ode = OldTex(
            "{d",
            "\\over dt}",
            self.output_tex,
            "(t)",
            "=", self.k_tex,
            "\\cdot", self.output_tex, "(t)",
            **tex_kwargs
        )
        ode.to_edge(UP)
        exp = OldTex(
            self.output_tex,
            "(t) =", self.initial_value_tex,
            "e^{", self.k_tex, "t}",
            **tex_kwargs
        )
        exp.next_to(ode, DOWN, LARGE_BUFF)

        M0_part = exp.get_part_by_tex(self.initial_value_tex)
        exp_part = exp[-3:]
        M0_label = M0_part.copy()
        M0_label.next_to(
            axes.c2p(0, self.initial_value),
            LEFT
        )
        M0_part.set_opacity(0)
        exp_part.save_state()
        exp_part.align_to(M0_part, LEFT)

        self.add(axes)
        self.add(graph)
        self.add(time_tracker)

        self.play(FadeInFromDown(ode))
        self.wait(6)
        self.play(FadeIn(exp, UP))
        self.wait(2)
        self.play(
            Restore(exp_part),
            M0_part.set_opacity, 1,
        )
        self.play(TransformFromCopy(
            M0_part, M0_label
        ))
        self.wait(5)

    def get_time_tracker(self):
        time_tracker = ValueTracker(0)
        time_tracker.add_updater(
            lambda m, dt: m.increment_value(
                self.time_rate * dt
            )
        )
        return time_tracker
