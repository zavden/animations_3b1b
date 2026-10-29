# ==============================================================================
# Scene:      LogTable
# Source:     videos/_2025/grover/runtime.py (lines 669-737)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LogTable.py LogTable -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LogTable(InteractiveScene):
    def construct(self):
        # Set up table
        n_samples = 9
        line_width = 8
        line_buff = 0.75

        h_line = Line(LEFT, RIGHT).set_width(line_width)
        h_lines = h_line.get_grid(n_samples, 1, buff=line_buff)
        h_lines.set_stroke(WHITE, 1)
        h_lines.shift(0.25 * DOWN)

        v_line = Line(UP, DOWN).set_height(7)
        v_line.set_stroke(WHITE, 2)

        N_title, logN_title = titles = VGroup(
            Tex("N"),
            Tex(R"\log_2(N)"),
        )
        titles.scale(1.25)
        for sign, title in zip([-1, 1], titles):
            title.set_x(sign * 2)
            title.to_edge(UP)

        self.add(h_lines, v_line)
        self.add(titles)

        # Fill with numbers
        N_values = VGroup()
        logN_values = VGroup()

        for n, line in enumerate(h_lines[1:]):
            N = 10**(n + 1)
            N_value = Integer(N)
            logN_value = DecimalNumber(np.log2(N))
            N_value.next_to(line, UP, SMALL_BUFF).match_x(N_title)
            logN_value.next_to(line, UP, SMALL_BUFF).match_x(logN_title)
            N_value.align_to(logN_value, UP)
            N_values.add(N_value)
            logN_values.add(logN_value)

        self.add(N_values[0], logN_values[0])
        for index in range(len(N_values) - 1):
            self.play(
                TransformMatchingShapes(N_values[index].copy(), N_values[index + 1]),
                FadeIn(logN_values[index + 1], shift=0.5 * DOWN),
                run_time=1
            )
        self.add(N_values)
        self.add(logN_values)

        # Show addition
        all_arrows = VGroup()
        for line in h_lines[1:-1]:
            arrow = Arrow(
                logN_values[0].get_right(),
                logN_values[1].get_right(),
                path_arc=-PI,
                buff=0
            )
            arrow.scale(0.8)
            arrow.next_to(line, RIGHT, SMALL_BUFF)
            plus_label = Tex(R"+\log_2(10)", font_size=24)
            plus_label.set_color(BLUE)
            plus_label.next_to(arrow, RIGHT, SMALL_BUFF)

            all_arrows.add(VGroup(arrow, plus_label))

        self.play(LaggedStartMap(FadeIn, all_arrows, lag_ratio=0.25), run_time=3)
