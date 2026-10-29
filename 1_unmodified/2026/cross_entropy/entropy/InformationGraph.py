# ==============================================================================
# Scene:      InformationGraph
# Source:     videos/_2026/cross_entropy/entropy.py (lines 1149-1515)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InformationGraph.py InformationGraph -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import math
import numpy as np
from scipy.special import gamma

class ProbIcon(VGroup):
    def __init__(
        self,
        prob,
        radius=0.5,
        color=GREEN,
        label_font_size=24,
    ):
        super().__init__()
        self.sector_color = color
        self.label_font_size = label_font_size

        border = Circle(radius=radius).set_stroke(WHITE, 1)
        self.border = border
        self.add(border)

        self.sector = self.get_sector(prob)
        self.label = self.get_label(prob)

        self.add(self.border, self.sector, self.label)

    def set_value(self, value):
        self.label.set_value(100 * value)
        self.sector.become(self.get_sector(value))
        return self

    def get_sector(self, prob):
        radius = self.border.get_width() / 2
        sector = Sector(angle=-prob * TAU, start_angle=TAU / 4, radius=radius)
        sector.set_fill(self.sector_color, 1, border_width=1)
        sector.shift(self.border.get_center())
        return sector

    def get_label(self, prob):
        ndp = 0
        if prob < 0.01:
            ndp = 2
        elif (100 * prob) % 1 == 0.5:
            ndp = 1
        label = DecimalNumber(
            100 * prob,
            unit="%",
            font_size=self.label_font_size,
            num_decimal_places=ndp
        )
        label.next_to(self.border, DOWN, SMALL_BUFF)
        return label


class InformationGraph(InteractiveScene):
    # prob_color = TEAL_D
    prob_color = WHITE
    info_color = BLUE
    input_var = "x"

    def construct(self):
        # Add split diagrams
        frame = self.frame
        diagrams = VGroup(
            Square().get_grid(*dims, buff=0).set_shape(2, 2).set_stroke(WHITE, 2)
            for dims in [(1, 2), (2, 2), (2, 4), (4, 4)]
        )
        for diagram in diagrams:
            diagram[0].set_fill(self.prob_color, 1)

        diagrams.arrange(RIGHT, buff=LARGE_BUFF)

        stacks = VGroup()
        for n, diagram in enumerate(diagrams, start=1):
            power_eq = Tex(
                Rf"\left({{1 \over 2}} \right)^{n} = {{1 \over {2**n}}}",
                t2c={Rf"{{1 \over {2**n}}}": self.prob_color},
                font_size=30
            )
            log_eq = Tex(
                Rf"-\log_2(1 / {2**n}) = {n}",
                t2c={Rf"1 / {2**n}": self.prob_color},
                font_size=30
            )
            equiv = Tex(R"\Leftrightarrow").rotate(90 * DEG)
            stack = VGroup(power_eq, equiv, log_eq)
            stack.arrange(DOWN)
            stack.next_to(diagram, UP)
            stacks.add(stack)

        self.add(diagrams[0])
        self.add(stacks[0])
        frame.match_x(stacks[0])
        self.wait()
        for n in range(1, len(stacks)):
            self.play(
                frame.animate.match_x(stacks[:n + 1]),
                FadeIn(diagrams[n]),
                FadeIn(stacks[n]),
            )
            self.wait()

        # Prepare axes
        max_y = 6
        axes = Axes(
            (0, 1, 1 / 16),
            (0, max_y),
            width=8,
            height=5
        )
        axes.x_axis.add_numbers([0, 1], font_size=36, num_decimal_places=1)
        axes.x_axis.numbers[0].next_to(axes.get_origin(), DL, SMALL_BUFF)
        bit_lines = VGroup(
            Line(axes.c2p(0, y), axes.c2p(1, y)).set_stroke(GREY_B, 1)
            for y in range(1, max_y + 1)
        )
        bit_labels = VGroup(
            Text(f"{n} bits", font_size=24).set_fill(GREY_C).next_to(line, LEFT)
            for n, line in zip(it.count(1), bit_lines)
        )
        axes.add(bit_lines, bit_labels)

        p_label = Tex(self.input_var).set_color(self.prob_color)
        p_label.next_to(axes.x_axis.get_end(), RIGHT)
        axes.add(p_label)

        info_label = Tex(
            Rf"-\log_2({self.input_var})",
            t2c={R"-\log_2": self.info_color, self.input_var: self.prob_color}
        )
        info_label.next_to(axes.c2p(0, max_y), UR)

        # Add bars to graph
        bars = VGroup(
            Rectangle(
                width=0.25,
                height=axes.y_axis.get_unit_size() * n
            ).move_to(axes.c2p(0.5**n, 0), DOWN)
            for n in range(1, 5)
        )
        bars.set_stroke(WHITE, 1).set_fill(self.info_color, 1)

        bar_labels = VGroup(
            Tex(Rf"1 \over {2**n}", font_size=30).next_to(bar, DOWN).set_color(self.prob_color)
            for n, bar in enumerate(bars, start=1)
        )

        self.play(
            LaggedStart(*(
                TransformFromCopy(stack[2][f"1 / {2**n}"][0], label, run_time=2)
                for stack, label, n in zip(stacks, bar_labels, it.count(1))
            )),
            LaggedStart(*(
                TransformFromCopy(diagram[0], bar)
                for diagram, bar in zip(diagrams, bars)
            )),
            Write(info_label),
            FadeOut(diagrams),
            FadeOut(stacks),
            FadeIn(axes, time_span=(1, 3)),
            FadeIn(bars, time_span=(1, 3)),
        )
        self.wait()

        # Add graph indicator
        graph = axes.get_graph(
            lambda p: -np.log2(p),
            x_range=(1e-5, 1, 1e-2)
        )
        graph.set_stroke(self.info_color, 3)

        p_tracker = ValueTracker(0.5)
        get_p = p_tracker.get_value

        graph_dot = Group(TrueDot().make_3d(), GlowDot())
        graph_dot.set_color(TEAL)
        graph_dot.add_updater(
            lambda m: m.move_to(axes.i2gp(get_p(), graph))
        )

        p_tip = ArrowTip(90 * DEG).set_height(0.15)
        p_tip.set_color(self.prob_color)
        p_tip.add_updater(lambda m: m.move_to(axes.x_axis.n2p(get_p()), UP))

        bit_tip = ArrowTip().set_width(0.15)
        bit_tip.set_color(self.info_color)
        bit_tip.add_updater(lambda m: m.move_to(axes.y_axis.n2p(-math.log2(get_p())), RIGHT))

        p_dec = DecimalNumber(font_size=36, fill_color=self.prob_color, num_decimal_places=2)
        p_dec.add_updater(lambda m: m.set_value(get_p()).next_to(p_tip, DOWN, SMALL_BUFF))

        equals = Tex(R"=")
        equals.always.next_to(info_label, RIGHT, SMALL_BUFF)
        log_p_dec = DecimalNumber(font_size=48, fill_color=self.info_color)
        log_p_dec.add_updater(lambda m: m.set_value(-math.log2(get_p())).next_to(equals, RIGHT, SMALL_BUFF))

        v_line = always_redraw(
            lambda: DashedLine(
                p_tip.get_top(),
                graph_dot.get_center(),
                dash_length=0.05,
                stroke_width=1,
                stroke_color=WHITE
            )
        )
        h_line = always_redraw(
            lambda: DashedLine(
                bit_tip.get_right(),
                graph_dot.get_center(),
                dash_length=0.05,
                stroke_width=1,
                stroke_color=WHITE
            )
        )

        self.play(ShowCreation(graph))
        self.wait()
        self.play(
            FadeIn(p_tip),
            FadeIn(bit_tip),
            FadeIn(graph_dot),
            FadeIn(v_line),
            FadeIn(h_line),
            FadeIn(p_dec),
            FadeIn(equals),
            FadeIn(log_p_dec),
            FadeOut(bars),
            FadeOut(bar_labels),
        )
        self.wait()

        # Play with values
        self.play_with_prob(p_tracker, [0.2, 0.9, 0.1])

        # Show as information definition
        # lhs = Tex(R"\text{Information} :=")
        lhs = Tex(R"\text{Loss} =")
        lhs["Loss"].set_color(RED)
        lhs.move_to(info_label, UL)
        lhs.shift((equals.get_y() - lhs["="].get_y()) * UP)

        self.play(FlashAround(info_label, run_time=2))
        self.play(
            Write(lhs),
            info_label.animate.next_to(lhs, RIGHT, SMALL_BUFF, UP)
        )
        self.wait()

        # Play some more
        self.play_with_prob(p_tracker, [0.5, 0.9, 0.02, 0.5], run_time_each=4)

        # Add prob and entropy indicators
        frame = self.frame

        info_bar = Rectangle(0.5, 3)
        info_bar.set_fill(self.info_color, 1)
        info_bar.set_stroke(WHITE, 1)
        info_bar.next_to(axes.c2p(1, 0), RIGHT, buff=1.5, aligned_edge=DOWN)
        info_bar.add_updater(lambda m: m.match_height(v_line, stretch=True).align_to(v_line, DOWN))

        brace = always_redraw(lambda: Brace(info_bar, RIGHT, SMALL_BUFF))
        log_label = Tex(Rf"-\log_2({self.input_var})")
        log_label.always.next_to(brace, RIGHT, SMALL_BUFF)

        prob_icon = ProbIcon(p_tracker.get_value(), radius=0.5)
        prob_icon.next_to(info_bar, DOWN)
        prob_icon.add_updater(lambda m: m.set_value(get_p()))

        self.play(
            frame.animate.reorient(0, 0, 0, (2.56, -0.52, 0.0), 9.20),
            FadeIn(prob_icon),
            VFadeIn(info_bar),
            VFadeIn(brace, suspend_mobject_updating=True),
            VFadeIn(log_label),
        )
        self.wait()

        # Play with values more
        self.play_with_prob(p_tracker, [0.25, 0.1, 0.01])
        self.wait()
        self.play(p_tracker.animate.set_value(0.9), run_time=5)
        self.wait()

        # Compare to other graphs
        log_graph = graph
        top_to_fade = VGroup(lhs, equals, log_p_dec)
        value_indicators = Group(p_tip, bit_tip, graph_dot, v_line, h_line, p_dec)
        side_to_fade = VGroup(info_bar, brace, log_label, prob_icon)
        side_to_fade.clear_updaters()

        x_range = (1e-2, 1, 1e-2)
        alt_graphs = VGroup(
            axes.get_graph(lambda x: (1.0 / (x)) - 1, x_range=x_range),
            axes.get_graph(lambda x: np.tan((PI / 2) * (1 - x)), x_range=x_range),
            axes.get_graph(lambda x: gamma(x) - 1, x_range=x_range),
        )
        alt_graph_labels = VGroup(
            Tex(R"{1 \over x} - 1"),
            Tex(R"\tan\left({\pi \over 2}(1 - x)\right)"),
            Tex(R"\Gamma(x) - 1"),
        )
        colors = [YELLOW, GREEN, RED]
        xs = [0.15, 0.2, 0.3]
        for label, alt_graph, color, x in zip(alt_graph_labels, alt_graphs, colors, xs):
            alt_graph.set_color(color)
            label.set_color(color)
            label.next_to(axes.i2gp(x, alt_graph), UR, buff=0.05)
            label.set_z_index(1)

        self.play(
            frame.animate.to_default_state(),
            FadeOut(top_to_fade),
            FadeOut(value_indicators),
            FadeOut(side_to_fade),
            info_label.animate.set_x(axes.y_axis.get_x(), RIGHT).shift(SMALL_BUFF * UP),
        )

        curr_graphs = VGroup(log_graph)
        curr_labels = VGroup(info_label)
        for label, alt_graph in zip(alt_graph_labels, alt_graphs):
            self.play(
                curr_graphs.animate.set_stroke(opacity=0.2),
                curr_labels.animate.set_fill(opacity=0.2),
                ShowCreation(alt_graph),
                FadeIn(label, 0.5 * UP)
            )
            self.wait()
            curr_graphs.add(alt_graph)
            curr_labels.add(label)
        self.wait()
        self.play(
            log_graph.animate.set_stroke(opacity=1),
            info_label.animate.set_fill(opacity=1),
            curr_graphs[1:].animate.set_stroke(opacity=0.2),
            curr_labels[1:].animate.set_fill(opacity=0.2),
        )
        self.wait()

        # Contrast with natural log
        info_label.save_state()
        ln_graph = axes.get_graph(lambda x: -math.log(x), x_range=(1e-4, 1, 1e-2))
        ln_graph.set_stroke(GREEN, 3)
        ln_label = Tex(R"-\ln(x)", t2c={self.input_var: self.prob_color, R"-\ln": GREEN})
        ln_label.next_to(info_label, DOWN, MED_LARGE_BUFF)

        equation = Tex(
            R"-\log_2(x) \cdot \ln(2) = -\ln(x)",
            t2c={R"-\log_2": BLUE, R"-\ln": GREEN}
        )
        equation.to_edge(UP)
        equation.next_to(info_label, RIGHT, buff=2)

        deriv_arrow = Vector(DOWN)
        deriv_arrow.next_to(equation[ln_label.get_tex()], DOWN, SMALL_BUFF)
        deriv_arrow_label = Tex(R"d / dx", font_size=36)
        deriv_arrow_label.next_to(deriv_arrow.get_center(), RIGHT, SMALL_BUFF)
        deriv_value = Tex(R"1 / x")
        deriv_value.next_to(deriv_arrow, DOWN, SMALL_BUFF)

        self.play(
            TransformFromCopy(log_graph, ln_graph),
            TransformMatchingTex(info_label.copy(), ln_label, run_time=1),
            FadeOut(curr_labels[1:]),
            FadeOut(bit_labels),
        )
        self.wait()
        self.play(
            info_label.animate.set_fill(opacity=0.1),
            ln_label.animate.set_fill(opacity=0.1),
            *(
                TransformFromCopy(label, equation[label.get_tex()][0], path_arc=30 * DEG)
                for label in [info_label, ln_label]
            ),
            Write(equation[R"\cdot \ln(2) ="][0], time_span=(0.5, 1.5))
        )
        self.wait()
        self.play(
            GrowArrow(deriv_arrow),
            FadeIn(deriv_arrow_label, DOWN),
        )
        self.play(
            TransformFromCopy(equation["x"][-1], deriv_value["x"][0]),
            Write(deriv_value["1 / "][0])
        )
        self.wait()
        self.play(
            Restore(info_label),
            FadeOut(VGroup(ln_graph, ln_label, equation, deriv_arrow, deriv_arrow_label, deriv_value))
        )

        # Cycle between graph shapes
        self.remove(alt_graphs, alt_graph_labels, info_label)
        graph.save_state()
        f_name = Tex(R"f(x)", font_size=72)
        f_name.move_to(axes.c2p(0.3, 5.5))

        n_iterations = 100

        for n in range(n_iterations):
            new_graph = random.choice(alt_graphs)
            graph.restore()
            graph.align_data_and_family(new_graph)
            graph.interpolate(graph, new_graph, random.random())
            graph.stretch(random.uniform(0.5, 1), 1, about_edge=DR)
            graph.set_stroke(BLUE, 3, 1)
            self.wait(0.1)
        graph.restore()
        self.play(FadeIn(f_name))
        self.wait()

        # More ambient motion to discuss generality
        self.add(p_tracker, *value_indicators)
        p_tracker.set_value(0.5)

        for value in [0.02, 0.9, 0.5]:
            self.play(p_tracker.animate.set_value(value), run_time=6)
        self.wait()

    def play_with_prob(self, p_tracker, values, run_time_each=3):
        for value in values:
            self.play(p_tracker.animate.set_value(value), run_time=run_time_each)
