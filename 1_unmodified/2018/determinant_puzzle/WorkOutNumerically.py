# ==============================================================================
# Scene:      WorkOutNumerically
# Source:     videos/_2018/determinant_puzzle.py (lines 4-142)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WorkOutNumerically.py WorkOutNumerically -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WorkOutNumerically(Scene):
    CONFIG = {
        "M1_COLOR": TEAL,
        "M2_COLOR": PINK,
    }

    def construct(self):
        self.add_question()
        self.add_example()
        self.compute_rhs()
        self.compute_lhs()

    def add_question(self):
        equation = self.original_equation = OldTex(
            "\\det(", "M_1", "M_2", ")", "=",
            "\\det(", "M_1", ")",
            "\\det(", "M_2", ")",
        )
        equation.set_color_by_tex_to_color_map({
            "M_1": self.M1_COLOR,
            "M_2": self.M2_COLOR,
        })
        challenge = OldTexText("Explain in one sentence")
        challenge.set_color(YELLOW)
        group = VGroup(challenge, equation)
        group.arrange(DOWN)
        group.to_edge(UP)

        self.add(equation)
        self.play(Write(challenge))
        self.wait()

    def add_example(self):
        M1 = self.M1 = Matrix([[2, -1], [1, 1]])
        M1.set_color(self.M1_COLOR)
        self.M1_copy = M1.copy()
        M2 = self.M2 = Matrix([[-1, 4], [1, 1]])
        M2.set_color(self.M2_COLOR)
        self.M2_copy = M2.copy()
        eq_parts = OldTex(
            "\\det", "\\big(", "\\big)", "=",
            "\\det", "\\big(", "\\big)",
            "\\det", "\\big(", "\\big)",
        )
        for part in eq_parts.get_parts_by_tex("\\big"):
            part.scale(2)
            part.stretch(1.5, 1)
        i1, i2, i3 = [
            eq_parts.index_of_part(part) + 1
            for part in eq_parts.get_parts_by_tex("\\big(")
        ]
        equation = self.equation_with_numbers = VGroup(*it.chain(
            eq_parts[:i1], [M1, M2],
            eq_parts[i1:i2], [self.M1_copy],
            eq_parts[i2:i3], [self.M2_copy],
            eq_parts[i3:],
        ))
        equation.arrange(RIGHT, buff=SMALL_BUFF)
        eq_parts.get_part_by_tex("=").shift(0.2 * SMALL_BUFF * DOWN)
        equation.set_width(FRAME_WIDTH - 2 * LARGE_BUFF)
        equation.next_to(self.original_equation, DOWN, MED_LARGE_BUFF)

        self.play(LaggedStartMap(FadeIn, equation))

    def compute_rhs(self):
        M1, M2 = self.M1_copy, self.M2_copy

        line1 = VGroup(
            OldTex(
                "\\big(", "2", "\\cdot", "2", "-",
                "(-1)", "\\cdot", "1", "\\big)"
            ),
            OldTex(
                "\\big(", "-1", "\\cdot", "1", "-",
                "4", "\\cdot", "1", "\\big)"
            ),
        )
        line1.arrange(RIGHT, buff=SMALL_BUFF)
        line1[0].set_color(self.M1_COLOR)
        line1[1].set_color(self.M2_COLOR)
        indices = [1, 3, 5, 7]

        line2 = OldTex("(3)", "(-5)")
        line2.match_style(line1)
        line3 = OldTex("-15")
        arrows = [Tex("\\downarrow") for x in range(2)]
        lines = VGroup(line1, arrows[0], line2, arrows[1], line3)
        lines.arrange(DOWN, buff=MED_SMALL_BUFF)
        lines.next_to(self.equation_with_numbers, DOWN, buff=MED_LARGE_BUFF)
        lines.to_edge(RIGHT)

        for matrix, det in zip([M1, M2], line1):
            numbers = VGroup(*[det[i] for i in indices])
            numbers_iter = iter(numbers)
            non_numbers = VGroup(*[m for m in det if m not in numbers])
            matrix_numbers = VGroup(*[
                matrix.mob_matrix[i][j].copy()
                for i, j in ((0, 0), (1, 1), (0, 1), (1, 0))
            ])
            self.play(
                LaggedStartMap(FadeIn, non_numbers, run_time=1),
                LaggedStartMap(
                    ReplacementTransform,
                    matrix_numbers,
                    lambda m: (m, next(numbers_iter)),
                    path_arc=TAU / 6
                ),
            )
        self.play(LaggedStartMap(FadeIn, lines[1:], run_time=3))

    def compute_lhs(self):
        matrix = Matrix([[-3, 7], [0, 5]])
        matrix.set_color(BLUE)
        matrix.scale(0.8)
        empty_det_tex = OldTex("\\det", "\\big(", "\\big)")
        empty_det_tex[1:].scale(1.5)
        empty_det_tex[1:].match_height(matrix, stretch=True)
        det_tex = VGroup(empty_det_tex[:2], matrix, *empty_det_tex[2:])
        det_tex.arrange(RIGHT, buff=SMALL_BUFF)

        group = VGroup(
            det_tex,
            OldTex("\\downarrow"),
            OldTex("(-3)(5) - (7)(0)").scale(0.8),
            OldTex("\\downarrow"),
            OldTex("-15"),
        )
        group.arrange(DOWN, buff=2 * SMALL_BUFF)
        # group.set_height(0.4*FRAME_HEIGHT)
        group.next_to(self.equation_with_numbers, DOWN)
        group.shift(FRAME_WIDTH * LEFT / 4)

        self.play(FadeIn(empty_det_tex))
        self.play(*[
            ReplacementTransform(M.copy(), matrix)
            for M in (self.M1, self.M2)
        ])
        self.play(LaggedStartMap(FadeIn, group[1:]))
        self.wait()
