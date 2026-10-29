# ==============================================================================
# Scene:      Amplitude
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1075-1109)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Amplitude.py Amplitude -w -m --fps 15
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


class Amplitude(InteractiveScene):
    def construct(self):
        # Show equation with annotations
        equation = Tex(R"""
            \text{Layer wiggle amplitude} = 
            \frac{q ||\vec{\textbf{E}}_0||}{m\left(\omega_r^2-\omega_l^2\right)}
        """, t2c=EQUATION_T2C)
        equation.to_corner(UL)

        lf_rect = SurroundingRectangle(equation[R"\omega_l"])
        rf_rect = SurroundingRectangle(equation[R"\omega_r"])

        lf_words = Text("Light frequency", font_size=36)
        rf_words = Text("Resonant frequency", font_size=36)
        lf_words.next_to(lf_rect, DOWN)
        rf_words.next_to(rf_rect, DOWN)

        VGroup(lf_rect, rf_rect).set_stroke(width=2)
        VGroup(lf_rect, lf_words).set_color(EQUATION_T2C[R"\omega_l"])
        VGroup(rf_rect, rf_words).set_color(EQUATION_T2C[R"\omega_r"])

        self.add(equation)
        self.wait()
        self.play(
            ShowCreation(lf_rect),
            FadeIn(lf_words, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            ReplacementTransform(lf_rect, rf_rect),
            FadeTransform(lf_words, rf_words),
        )
        self.wait()
        self.play(FadeOut(rf_rect), FadeOut(rf_words))
        self.wait()
