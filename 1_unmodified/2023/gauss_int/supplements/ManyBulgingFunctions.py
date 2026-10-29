# ==============================================================================
# Scene:      ManyBulgingFunctions
# Source:     videos/_2023/gauss_int/supplements.py (lines 306-358)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ManyBulgingFunctions.py ManyBulgingFunctions -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ManyBulgingFunctions(InteractiveScene):
    def construct(self):
        # Test
        axes = Axes((-3, 3), (0, 1), width=3, height=1, axis_config=dict(tick_size=0.05))
        all_axes = axes.get_grid(3, 2, h_buff=LARGE_BUFF, v_buff=1.5)
        all_axes.to_edge(RIGHT)

        ie = math.exp(-1)
        eem1 = math.exp(-math.exp(-1))
        functions = [
            lambda x: (1 / (1 + x**2)),
            lambda x: (1 / (1 + x**4)),
            lambda x: np.exp(-x**2),
            lambda x: np.exp(-x**4),
            lambda x: eem1 * (np.abs(x) + ie)**(-np.abs(x) - ie),
            lambda x: np.sinc(x)**2,
        ]

        func_labels = VGroup(
            Tex(R"\frac{1}{1 + x^2}"),
            Tex(R"\frac{1}{1 + x^4}"),
            Tex(R"e^{-x^2}", font_size=60),
            Tex(R"e^{-x^4}", font_size=60),
            Tex(R"e^{-1/e} \left(\left|x\right|+\frac{1}{e}\right)^{-\left(\left|x\right|+\frac{1}{e}\right)}", font_size=36),
            Tex(R"\left(\frac{\sin(\pi x)}{\pi x} \right)^2"),
        )

        colors = [TEAL_C, TEAL_D, BLUE_C, BLUE_D, RED_C, RED_D]

        plots = VGroup()
        for axes, func, label, color in zip(all_axes, functions, func_labels, colors):
            label.scale(0.5)
            label.move_to(axes.get_corner(UR))
            label.shift_onto_screen()
            graph = axes.get_graph(func)
            graph.set_stroke(color, 3)
            graph.move_to(axes.get_top(), UP)

            plots.add(VGroup(axes, graph, label))

        key_plot = plots[2]
        plots.remove(key_plot)

        self.play(
            FadeIn(key_plot[0]),
            ShowCreation(key_plot[1]),
            Write(key_plot[2]),
        )
        self.wait()
        self.play(LaggedStartMap(FadeIn, plots, lag_ratio=0.5))
        self.wait()
        self.play(plots.animate.fade(0.5))
        self.wait()
