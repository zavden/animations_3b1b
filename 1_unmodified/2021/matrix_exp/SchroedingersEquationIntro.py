# ==============================================================================
# Scene:      SchroedingersEquationIntro
# Source:     videos/_2021/matrix_exp.py (lines 2642-2758)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SchroedingersEquationIntro.py SchroedingersEquationIntro -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SchroedingersEquationIntro(Scene):
    def construct(self):
        # Show equation
        title = Text("Schrödinger equation", font_size=72)
        title.to_edge(UP)
        self.add(title)

        t2c = {
            "|\\psi \\rangle": BLUE,
            "{H}": GREY_A,
            "=": WHITE,
            "i\\hbar": WHITE,
        }
        original_equation = OldTex(
            "i\\hbar \\frac{\\partial}{\\partial t} |\\psi \\rangle = {H} |\\psi \\rangle",
            tex_to_color_map=t2c
        )
        equation = OldTex(
            "\\frac{\\partial}{\\partial t} |\\psi \\rangle = \\frac{1}{i\\hbar} {H} |\\psi \\rangle",
            tex_to_color_map=t2c
        )
        VGroup(original_equation, equation).scale(1.5)

        psis = original_equation.get_parts_by_tex("\\psi")
        state_label = OldTexText("State of a system \\\\ as a vector", font_size=36)
        state_label.next_to(psis, DOWN, buff=1.5)
        state_label.shift(0.5 * RIGHT)
        state_arrows = VGroup(*(Arrow(state_label, psi) for psi in psis))
        state_label.match_color(psis[0])
        state_arrows.match_color(psis[0])
        psis.set_color(WHITE)

        randy = Randolph(height=2.0, color=BLUE_C)
        randy.to_corner(DL)
        randy.set_opacity(0)

        self.play(Write(original_equation, run_time=3))
        self.wait()
        self.play(
            randy.animate.set_opacity(1).change("horrified", original_equation)
        )
        self.play(Blink(randy))
        self.play(
            randy.change("pondering", state_label),
            psis.animate.match_color(state_label),
            FadeIn(state_label, 0.25 * DOWN),
            *map(GrowArrow, state_arrows),
        )
        self.wait()
        self.play(Blink(randy))
        self.wait()

        self.play(
            ReplacementTransform(original_equation[1:4], equation[0:3]),
            Write(equation[3]),
            ReplacementTransform(original_equation[0], equation[4], path_arc=90 * DEGREES),
            ReplacementTransform(original_equation[4:], equation[5:]),
            state_arrows.animate.become(
                VGroup(*(Arrow(state_label, psi) for psi in equation.get_parts_by_tex("\\psi")))
            ),
            randy.change("hesitant", equation)
        )
        self.play(FlashAround(equation[0], time_width=2, run_time=2))
        self.play(Blink(randy))

        mat_rect = SurroundingRectangle(equation[3:6], buff=0.05, color=TEAL)
        mat_label = Text("A certain matrix", font_size=36)
        mat_label.next_to(mat_rect, UP)
        mat_label.match_color(mat_rect)
        self.play(
            ShowCreation(mat_rect),
            FadeIn(mat_label, 0.25 * UP),
        )
        self.wait()
        self.play(randy.change("confused", equation))
        self.play(Blink(randy))
        self.wait()

        # Complicating factors
        psi_words = OldTexText(
            "Often this is a function.\\\\",
            "(But whatever functions are really\\\\just infinite-dimensional vectors)"
        )
        psi_words[0].match_width(psi_words[1], about_edge=DOWN)
        psi_words[1].shift(0.1 * DOWN)
        psi_words.scale(0.75)
        psi_words.move_to(state_label, UP)
        psi_words[0].set_color(RED)
        psi_words[1].set_color(RED_D)

        mat_line = Line(LEFT, RIGHT)
        mat_line.set_stroke(RED, 5)
        mat_line.replace(mat_label.get_part_by_text("matrix"), dim_to_match=0)

        operator_word = Text("operator", font_size=36)
        operator_word.next_to(mat_label, UP, buff=SMALL_BUFF)
        operator_word.align_to(mat_line, LEFT)
        operator_word.set_color(RED)

        complex_valued = Text("Complex-valued", font_size=30)
        complex_valued.set_color(RED)
        complex_valued.next_to(equation, RIGHT)
        complex_valued.to_edge(RIGHT)
        cv_arrow = Arrow(complex_valued, equation, fill_color=RED)

        self.play(LaggedStart(
            FadeOut(state_label),
            FadeIn(psi_words),
            ShowCreation(mat_line),
            Write(operator_word, run_time=1),
            GrowArrow(cv_arrow),
            FadeIn(complex_valued),
            randy.change("horrified", equation),
            lag_ratio=0.5
        ))
        self.play(Blink(randy))
        self.wait()
