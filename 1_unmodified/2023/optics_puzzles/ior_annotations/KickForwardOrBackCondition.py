# ==============================================================================
# Scene:      KickForwardOrBackCondition
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1427-1490)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KickForwardOrBackCondition.py KickForwardOrBackCondition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

EQUATION_T2C = {
    R"\vec{\textbf{x}}(t)": RED,
    R"\vec{\textbf{F}}(t)": YELLOW,
    R"\vec{\textbf{a}}(t)": YELLOW,
    R"\frac{d^2 \vec{\textbf{x}}}{dt^2}(t) ": YELLOW,
    R"\vec{\textbf{E}}_0": BLUE,
    R"\omega_r": PINK,
    R"\omega_l": TEAL,
}


class KickForwardOrBackCondition(InteractiveScene):
    def construct(self):
        # First statement
        words = VGroup(
            TexText("If this $< 0$"),
            TexText("Refractive Index $< 1$", font_size=48),
        )
        rect = Rectangle(2, 1)
        rect.next_to(LEFT, LEFT, buff=MED_LARGE_BUFF).set_y(1.9)
        words[0].next_to(rect, UP, MED_SMALL_BUFF)
        words[1].set_y(1.5)
        words[1].set_x(FRAME_WIDTH / 4)

        arrow = Arrow(words[0].get_right(), words[1].get_left())
        arrow.set_stroke(YELLOW, 6)

        self.play(Write(words[0]))
        self.play(
            GrowArrow(arrow),
            FadeIn(words[1], RIGHT)
        )
        self.wait()

        # Freq reference
        freq_ineq = Tex(R"\text{If } \omega_l > \omega_r", t2c=EQUATION_T2C)
        freq_ineq.move_to(words[0])

        lf_rect = SurroundingRectangle(freq_ineq[R"\omega_l"])
        rf_rect = SurroundingRectangle(freq_ineq[R"\omega_r"])

        lf_words = Text("Light frequency", font_size=36)
        rf_words = Text("Resonant frequency", font_size=36)
        lf_words.next_to(lf_rect, UP)
        rf_words.next_to(rf_rect, UP)

        VGroup(lf_rect, rf_rect).set_stroke(width=2)
        VGroup(lf_rect, lf_words).set_color(EQUATION_T2C[R"\omega_l"])
        VGroup(rf_rect, rf_words).set_color(EQUATION_T2C[R"\omega_r"])

        words[0].generate_target()
        words[0].target.next_to(rect, RIGHT, SMALL_BUFF)

        self.play(
            # MoveToTarget(words[0]),
            # arrow.animate.put_start_and_end_on(
            #     words[0].target.get_right() + SMALL_BUFF * RIGHT,
            #     arrow.get_end(),
            # ),
            FadeOut(words[0], 0.5 * UP),
            FadeIn(freq_ineq, 0.5 * UP),
        )
        self.wait()
        self.play(
            FadeIn(lf_rect),
            FadeIn(lf_words, shift=0.25 * UP),
        )
        self.wait()
        self.play(
            ReplacementTransform(lf_rect, rf_rect),
            FadeTransform(lf_words, rf_words),
        )
        self.wait()
        self.play(FadeOut(rf_words), FadeOut(rf_rect))
        self.wait()
