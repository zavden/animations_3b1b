# ==============================================================================
# Scene:      PureMathEquation
# Source:     videos/_2025/laplace/prequel_equations.py (lines 942-978)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PureMathEquation.py PureMathEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PureMathEquation(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"x''(t)": RED, "x(t)": TEAL, R"\omega": PINK}
        physics_eq = Tex(R"m x''(t) + k x(t) = 0", t2c=t2c, font_size=72)
        math_eq = Tex(R"a_2 x''(t) + a_0 x(t) = 0", t2c=t2c, font_size=72)

        self.add(physics_eq)
        self.play(LaggedStart(
            *(
                ReplacementTransform(physics_eq[tex][0], math_eq[tex][0])
                for tex in ["x''(t) +", "x(t) = 0"]
            ),
            FadeOut(physics_eq["m"], 0.5 * UP),
            FadeIn(math_eq["a_2"], 0.5 * UP),
            FadeOut(physics_eq["k"], 0.5 * UP),
            FadeIn(math_eq["a_0"], 0.5 * UP),
            run_time=2,
            lag_ratio=0.15
        ))
        self.wait()

        # Show solution
        implies = Tex(R"\Downarrow", font_size=72)
        answer = Tex(R"e^{\pm i\omega t}", font_size=90, t2c=t2c)
        answer.next_to(implies, DOWN, MED_LARGE_BUFF)
        omega_eq = Tex(R"\text{Where } \omega = \sqrt{a_2 / a_0}", t2c=t2c)
        omega_eq.next_to(answer, DOWN, MED_LARGE_BUFF)

        self.play(LaggedStart(
            math_eq.animate.next_to(implies, UP, MED_LARGE_BUFF),
            Write(implies),
            FadeIn(answer, DOWN),
            lag_ratio=0.25
        ))
        self.play(FadeIn(omega_eq))
        self.wait()
