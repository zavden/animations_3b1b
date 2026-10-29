# ==============================================================================
# Scene:      FourierSeriesIllustraiton
# Source:     videos/_2019/diffyq/part3/staging.py (lines 233-406)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FourierSeriesIllustraiton.py FourierSeriesIllustraiton -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FourierSeriesIllustraiton(Scene):
    CONFIG = {
        "n_range": range(1, 31, 2),
        "axes_config": {
            "axis_config": {
                "include_tip": False,
            },
            "x_axis_config": {
                "tick_frequency": 1 / 4,
                "unit_size": 4,
            },
            "x_min": 0,
            "x_max": 1,
            "y_min": -1,
            "y_max": 1,
        },
        "colors": [BLUE, GREEN, RED, YELLOW, PINK],
    }

    def construct(self):
        aaa_group = self.get_axes_arrow_axes()
        aaa_group.shift(2 * UP)
        aaa_group.shift_onto_screen()
        axes1, arrow, axes2 = aaa_group

        axes2.add(self.get_target_func_graph(axes2))

        sine_graphs = self.get_sine_graphs(axes1)
        partial_sums = self.get_partial_sums(axes1, sine_graphs)

        sum_tex = self.get_sum_tex()
        sum_tex.next_to(axes1, DOWN, LARGE_BUFF)
        sum_tex.shift(RIGHT)
        eq = OldTex("=")
        target_func_tex = self.get_target_func_tex()
        target_func_tex.next_to(axes2, DOWN)
        target_func_tex.match_y(sum_tex)
        eq.move_to(midpoint(
            target_func_tex.get_left(),
            sum_tex.get_right()
        ))

        range_words = OldTexText(
            "For $0 \\le x \\le 1$"
        )
        range_words.next_to(
            VGroup(sum_tex, target_func_tex),
            DOWN,
        )

        rects = it.chain(
            [
                SurroundingRectangle(piece)
                for piece in self.get_sum_tex_pieces(sum_tex)
            ],
            it.cycle([None])
        )

        self.add(axes1, arrow, axes2)
        self.add(sum_tex, eq, target_func_tex)
        self.add(range_words)

        curr_partial_sum = axes1.get_graph(lambda x: 0)
        curr_partial_sum.set_stroke(width=1)
        for sine_graph, partial_sum, rect in zip(sine_graphs, partial_sums, rects):
            anims1 = [
                ShowCreation(sine_graph)
            ]
            partial_sum.set_stroke(BLACK, 4, background=True)
            anims2 = [
                curr_partial_sum.set_stroke,
                {"width": 1, "opacity": 0.5},
                curr_partial_sum.set_stroke,
                {"width": 0, "background": True},
                ReplacementTransform(
                    sine_graph, partial_sum,
                    remover=True
                ),
            ]
            if rect:
                rect.match_style(sine_graph)
                anims1.append(ShowCreation(rect))
                anims2.append(FadeOut(rect))
            self.play(*anims1)
            self.play(*anims2)
            curr_partial_sum = partial_sum

    def get_axes_arrow_axes(self):
        axes1 = Axes(**self.axes_config)
        axes1.x_axis.add_numbers(
            0.5, 1,
            num_decimal_places=1
        )
        axes1.y_axis.add_numbers(
            -1, 1,
            direction=LEFT,
            num_decimal_places=1,
        )
        axes2 = axes1.deepcopy()

        arrow = Arrow(LEFT, RIGHT, color=WHITE)
        group = VGroup(axes1, arrow, axes2)
        group.arrange(RIGHT, buff=MED_LARGE_BUFF)
        return group

    def get_sine_graphs(self, axes):
        sine_graphs = VGroup(*[
            axes.get_graph(self.generate_nth_func(n))
            for n in self.n_range
        ])
        sine_graphs.set_stroke(width=3)
        for graph, color in zip(sine_graphs, it.cycle(self.colors)):
            graph.set_color(color)
        return sine_graphs

    def get_partial_sums(self, axes, sine_graphs):
        partial_sums = VGroup(*[
            axes.get_graph(self.generate_kth_partial_sum_func(k + 1))
            for k in range(len(self.n_range))
        ])
        partial_sums.match_style(sine_graphs)
        return partial_sums

    def get_sum_tex(self):
        return OldTex(
            "\\frac{4}{\\pi} \\left(",
            "\\frac{\\cos(\\pi x)}{1}",
            "-\\frac{\\cos(3\\pi x)}{3}",
            "+\\frac{\\cos(5\\pi x)}{5}",
            "- \\cdots \\right)"
        ).scale(0.75)

    def get_sum_tex_pieces(self, sum_tex):
        return sum_tex[1:4]

    def get_target_func_tex(self):
        step_tex = OldTex(
            """
            1 \\quad \\text{if $x < 0.5$} \\\\
            0 \\quad \\text{if $x = 0.5$} \\\\
            -1 \\quad \\text{if $x > 0.5$} \\\\
            """
        )
        lb = Brace(step_tex, LEFT, buff=SMALL_BUFF)
        step_tex.add(lb)
        return step_tex

    def get_target_func_graph(self, axes):
        step_func = axes.get_graph(
            lambda x: (1 if x < 0.5 else -1),
            discontinuities=[0.5],
            color=YELLOW,
            stroke_width=3,
        )
        dot = Dot(axes.c2p(0.5, 0), color=step_func.get_color())
        dot.scale(0.5)
        step_func.add(dot)
        return step_func

    # def generate_nth_func(self, n):
    #     return lambda x: (4 / n / PI) * np.sin(TAU * n * x)

    def generate_nth_func(self, n):
        return lambda x: np.prod([
            (4 / PI),
            (1 / n) * (-1)**((n - 1) / 2),
            np.cos(PI * n * x)
        ])

    def generate_kth_partial_sum_func(self, k):
        return lambda x: np.sum([
            self.generate_nth_func(n)(x)
            for n in self.n_range[:k]
        ])
