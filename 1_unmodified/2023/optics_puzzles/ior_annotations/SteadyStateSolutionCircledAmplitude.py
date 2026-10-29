# ==============================================================================
# Scene:      SteadyStateSolutionCircledAmplitude
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1395-1412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SteadyStateSolutionCircledAmplitude.py SteadyStateSolutionCircledAmplitude -w -m --fps 15
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


class SteadyStateSolutionCircledAmplitude(InteractiveScene):
    def construct(self):
        equation = Tex(
            R"""
                \vec{\textbf{x}}(t) = 
                \cos(\omega_l t) \cdot
                \frac{q ||\vec{\textbf{E}}_0||}{m\left(\omega_r^2-\omega_l^2\right)}
            """,
            t2c=EQUATION_T2C
        )
        equation.set_backstroke(BLACK, 5)

        rect = SurroundingRectangle(equation[R"\frac{q ||\vec{\textbf{E}}_0||}{m\left(\omega_r^2-\omega_l^2\right)}"])
        rect.set_stroke(TEAL)

        self.add(equation)
        self.play(ShowCreation(rect))
        self.wait()
