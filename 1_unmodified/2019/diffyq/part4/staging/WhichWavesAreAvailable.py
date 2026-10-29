# ==============================================================================
# Scene:      WhichWavesAreAvailable
# Source:     videos/_2019/diffyq/part4/staging.py (lines 213-317)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhichWavesAreAvailable.py WhichWavesAreAvailable -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhichWavesAreAvailable(Scene):
    CONFIG = {
        "axes_config": {
            "x_min": 0,
            "x_max": TAU,
            "y_min": -1.5,
            "y_max": 1.5,
            "x_axis_config": {
                "tick_frequency": PI / 2,
                "unit_size": 1,
                "include_tip": False,
            },
            "y_axis_config": {
                "unit_size": 1,
                "tick_frequency": 0.5,
                "include_tip": False,
            },
        },
        "n_axes": 5,
        "trig_func": np.cos,
        "trig_func_tex": "\\cos",
        "bc_words": "Restricted by\\\\boundary conditions",
    }

    def construct(self):
        self.setup_little_axes()
        self.show_cosine_waves()

    def setup_little_axes(self):
        axes_group = VGroup(*[
            Axes(**self.axes_config)
            for n in range(self.n_axes)
        ])
        axes_group.set_stroke(width=2)
        axes_group.arrange(DOWN, buff=1)
        axes_group.set_height(FRAME_HEIGHT - 1.25)
        axes_group.to_edge(RIGHT)
        axes_group.to_edge(UP, buff=MED_SMALL_BUFF)
        dots = OldTexText("\\vdots")
        dots.next_to(axes_group, DOWN)
        dots.shift_onto_screen()

        self.add(axes_group)
        self.add(dots)

        self.axes_group = axes_group

    def show_cosine_waves(self):
        axes_group = self.axes_group
        colors = [BLUE, GREEN, RED, YELLOW, PINK]

        graphs = VGroup()
        h_lines = VGroup()
        func_labels = VGroup()
        for k, axes, color in zip(it.count(1), axes_group, colors):
            L = axes.x_max
            graph = axes.get_graph(
                lambda x: self.trig_func(x * k * PI / L),
                color=color
            )
            graph.set_stroke(width=2)
            graphs.add(graph)

            func_label = OldTex(
                self.trig_func_tex + "\\left(",
                str(k),
                "(\\pi / L)x\\right)",
                tex_to_color_map={
                    str(k): color,
                }
            )
            func_label.scale(0.7)
            func_label.next_to(axes, LEFT)
            func_labels.add(func_label)

            hl1 = DashedLine(LEFT, RIGHT)
            hl1.set_width(0.5)
            hl1.set_stroke(WHITE, 2)
            hl1.move_to(graph.get_start())
            hl2 = hl1.copy()
            hl2.move_to(graph.get_end())
            h_lines.add(hl1, hl2)

        words = OldTexText(self.bc_words)
        words.next_to(axes_group, LEFT)
        words.to_edge(UP)

        self.play(
            FadeIn(words),
            LaggedStartMap(
                ShowCreation, graphs,
            )
        )
        self.play(Write(h_lines))
        self.play(FadeOut(h_lines))
        self.wait()
        self.play(
            words.next_to, func_labels, LEFT,
            words.to_edge, UP,
            LaggedStartMap(
                FadeInFrom, func_labels,
                lambda m: (m, RIGHT)
            )
        )
        self.wait()
