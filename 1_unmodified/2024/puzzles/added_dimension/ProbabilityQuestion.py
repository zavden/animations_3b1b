# ==============================================================================
# Scene:      ProbabilityQuestion
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2886-2991)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProbabilityQuestion.py ProbabilityQuestion -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ProbabilityQuestion(InteractiveScene):
    N = 6

    def construct(self):
        # Number lines and trackers
        trackers = Group(ValueTracker(np.random.uniform(-1, 1)) for x in range(self.N))
        lines = VGroup(
            self.get_uniform_random_indicator(tracker, n)
            for n, tracker in enumerate(trackers, start=1)
        )
        lines.arrange(DOWN, buff=0.35)
        lines.to_corner(DL)

        self.add(lines)

        # Add x_i distribution label
        dist_label = TexText("$x_i$ uniform in [-1, 1]")
        dist_label.match_x(lines).to_edge(UP)

        self.add(dist_label)

        # Add question label
        # lhs = Tex(R"P\left(\sum_{i=0}^7 x_i^2 \le 1 \right) = ")
        lhs = Tex(R"P\left(x_1^2 + x_2^2 + x_3^2 + x_4^2 + x_5^2 + x_6^2 \le 1 \right)")
        rhs = Tex(R"\frac{\pi^3}{6} \cdot \frac{1}{2^6}")
        eq = VGroup(lhs, Tex("=").rotate(PI / 2), rhs)
        eq.arrange(DOWN)
        eq.center().to_edge(RIGHT)

        self.add(eq)

        # Add brace
        def get_sum():
            return sum(t.get_value()**2 for t in trackers)

        brace = Brace(lhs[R"x_1^2 + x_2^2 + x_3^2 + x_4^2 + x_5^2 + x_6^2"], UP)
        brace.set_color(BLUE_D)
        sum_value = DecimalNumber()
        sum_value.set_color(BLUE_D)
        sum_value.next_to(brace, UP)
        sum_value.f_always.set_value(get_sum)

        symbols = VGroup(Checkmark().set_color(GREEN), Exmark().set_color(RED))
        symbols.set_height(0.5)
        symbols.match_x(lhs["1"][-1]).align_to(sum_value, UP)

        def update_symbols(syms):
            if get_sum() < 1:
                syms[0].set_opacity(1)
                syms[1].set_opacity(0)
            else:
                syms[1].set_opacity(1)
                syms[0].set_opacity(0)

        symbols.add_updater(update_symbols)

        self.add(brace, sum_value, symbols)

        # Animate in 6D label
        rect = SurroundingRectangle(rhs[R"\frac{\pi^3}{6}"])
        rect.set_stroke(TEAL, 2)
        label = Text("Volume of a \n 6D unit ball")
        label.next_to(rect, DOWN)
        label.set_color(TEAL)

        self.play(ShowCreation(rect))
        self.play(Write(label))
        self.wait()

        # Go over many random values
        time_per_state = 0.2
        total_time = 25
        for _ in range(int(total_time / time_per_state)):
            for tracker in trackers:
                tracker.set_value(np.random.uniform(-1, 1))
            self.wait(time_per_state)


    def get_uniform_random_indicator(self, value_tracker, n):
        line = NumberLine((-1, 1, 0.1), width=4, big_tick_spacing=1, tick_size=0.05)
        line.set_stroke(width=2)
        line.add_numbers(
            np.arange(-1, 1.5, 0.5),
            font_size=12,
            num_decimal_places=1,
            buff=0.15
        )

        tip = ArrowTip(angle=-90 * DEGREES)
        tip.set_height(0.15)
        tip.set_fill(YELLOW, 1)
        tip.add_updater(lambda m: m.move_to(line.n2p(value_tracker.get_value()), DOWN))
        tip.add_updater(lambda m: m.set_fill(self.value_to_color(value_tracker.get_value())))

        x_label = Tex(Rf"x_{n}", font_size=30)
        x_label.always.next_to(tip, UP, buff=0.05)
        x_label.always.match_color(tip)

        return VGroup(line, tip, x_label)

    def value_to_color(self, value):
        return interpolate_color_by_hsl(
            GREY_B,
            BLUE if value > 0 else RED,
            abs(value)
        )
