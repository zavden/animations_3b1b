# ==============================================================================
# Scene:      ShowGaussianConvolutionsAsEquations
# Source:     videos/_2023/convolutions2/gauss_example_supplements.py (lines 728-821)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/clt/main.py
#
# Run from this folder:
#     manimgl ShowGaussianConvolutionsAsEquations.py ShowGaussianConvolutionsAsEquations -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2023/clt/main.py -----

def gauss_func(x, mu, sigma):
    pre_factor = 1 / (sigma * math.sqrt(2 * PI))
    return pre_factor * np.exp(-0.5 * ((x - mu) / sigma)**2)



# ----- From _2023/convolutions2/gauss_example_supplements.py -----

class ShowGaussianConvolutionsAsEquations(InteractiveScene):
    def construct(self):
        # Add axes
        axes = VGroup(*(
            NumberPlane(
                (-3, 3), (0, 2),
                width=3, height=1,
                background_line_style=dict(stroke_width=1, stroke_color=GREY_D),
                faded_line_style=dict(stroke_width=1, stroke_opacity=0.2, stroke_color=GREY_D)
            )
            for x in range(6)
        ))
        axes.set_height(1.25)
        axes.arrange_in_grid(2, 3, h_buff=0.75, v_buff=3.0)
        for ax in axes[2::3]:
            ax.shift(0.75 * RIGHT)
        axes.center()

        stars = Tex("*", font_size=72).replicate(2)
        eqs = Tex("=", font_size=72).replicate(2)
        stars[0].move_to(axes[0:2])
        eqs[0].move_to(axes[1:3])
        stars[1].move_to(axes[3:5])
        eqs[1].move_to(axes[4:6])

        self.add(axes)
        self.add(stars, eqs)

        # Equations
        kw = dict(
            font_size=30,
            t2c={"x": BLUE, "y": YELLOW, "{s}": TEAL, R"\sigma": RED}
        )
        equations = VGroup(
            Tex(R"e^{-x^2}", **kw),
            Tex(R"e^{-y^2}", **kw),
            Tex(R"\sqrt{\frac{\pi}{2}} e^{-{s}^2 / 2}", **kw),
            Tex(R"\frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2} x^2 / \sigma^2}", **kw),
            Tex(R"\frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2} y^2 / \sigma^2}", **kw),
            Tex(R"\frac{1}{\sqrt{2}\sigma \sqrt{2\pi}} e^{-\frac{1}{2} {s}^2 / 2 \sigma^2}", **kw),
        )
        normal_annotations = VGroup(
            Tex(R"\mathcal{N}\left(0, \sigma^2\right)", **kw),
            Tex(R"\mathcal{N}\left(0, \sigma^2\right)", **kw),
            Tex(R"\mathcal{N}\left(0, 2\sigma^2\right)", **kw),
        )
        normal_annotations.scale(1.25)

        for eq, ax in zip(equations, axes):
            eq.next_to(ax, UP, MED_SMALL_BUFF)
        for ann, eq in zip(normal_annotations, equations[3:]):
            ann.next_to(eq, UP, MED_LARGE_BUFF)

        # Graphs
        sigma = 0.35
        graphs = VGroup(
            axes[0].get_graph(lambda x: np.exp(-x**2)),
            axes[1].get_graph(lambda y: np.exp(-y**2)),
            axes[2].get_graph(lambda s: np.exp(-s**2 / 2) * math.sqrt(PI / 2)),
            axes[3].get_graph(lambda x: gauss_func(x, 0, sigma)),
            axes[4].get_graph(lambda y: gauss_func(y, 0, sigma)),
            axes[5].get_graph(lambda s: gauss_func(s, 0, math.sqrt(2) * sigma)),
        )
        colors = [BLUE, YELLOW, TEAL]
        for graph, color in zip(graphs, it.cycle(colors)):
            graph.set_stroke(color, 2)

        # Animations
        self.add(equations[:3])
        self.add(graphs[:3])
        self.wait()
        self.play(
            LaggedStart(*(
                FadeTransform(eq1.copy(), eq2)
                for eq1, eq2 in zip(equations[:3], equations[3:])
            ), lag_ratio=0.15),
            LaggedStart(*(
                TransformFromCopy(graph1, graph2)
                for graph1, graph2 in zip(graphs[:3], graphs[3:])
            ), lag_ratio=0.15),
            LaggedStartMap(
                FadeIn, normal_annotations[:2],
                shift=0.5 * DOWN,
                lag_ratio=0.25,
                run_time=1
            )
        )
        self.wait()
        self.play(
            FadeTransform(normal_annotations[0].copy(), normal_annotations[2]),
            FadeTransform(normal_annotations[1].copy(), normal_annotations[2]),
            run_time=1
        )
        self.wait()
