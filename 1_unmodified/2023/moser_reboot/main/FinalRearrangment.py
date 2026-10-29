# ==============================================================================
# Scene:      FinalRearrangment
# Source:     videos/_2023/moser_reboot/main.py (lines 1043-1151)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FinalRearrangment.py FinalRearrangment -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FinalRearrangment(InteractiveScene):
    def construct(self):
        # Add equations
        top_eq = Tex("F = E - V + 1")
        top_eq.to_edge(UP, buff=LARGE_BUFF)

        V_rhs = R"n + {n \choose 4}"
        E_rhs = R"{n \choose 2} + 2{n \choose 4} + n"
        V_eq = Tex(Rf"V = {V_rhs}")
        E_eq = Tex(Rf"E = {E_rhs}")
        V_eq.next_to(top_eq, DOWN, buff=1.5)
        E_eq.next_to(top_eq, DOWN, buff=1.5)

        V_eq.set_color(TEAL)
        E_eq.set_color(BLUE_B)
        t2c = {
            Rf"\left({V_rhs}\right)": TEAL,
            Rf"\left({E_rhs}\right)": BLUE_B,
        }

        self.play(FadeIn(top_eq, UP))
        self.wait()

        # Substitute V
        top_eq2 = Tex(Rf"F = E - \left({V_rhs}\right) + 1", t2c=t2c)
        top_eq2.move_to(top_eq)

        self.play(
            top_eq["V"][0].animate.set_color(TEAL),
            FadeTransform(top_eq["V"][0].copy(), V_eq[0]),
            Write(V_eq[1:], run_time=1)
        )
        self.wait()
        self.play(
            FadeTransform(V_eq[2:].copy(), top_eq2[Rf"\left({V_rhs}\right)"]),
            FadeOut(top_eq["V"][0], UP),
            ReplacementTransform(
                top_eq["F = E - "],
                top_eq2["F = E - "],
            ),
            ReplacementTransform(
                top_eq[-2:],
                top_eq2[-2:],
            ),
        )
        self.wait()

        # Substitute E
        E_eq.set_color(BLUE_B)
        top_eq3 = Tex(
            Rf"F = \left({E_rhs}\right) - \left({V_rhs}\right) + 1",
            t2c=t2c
        )
        top_eq3.move_to(top_eq)

        self.play(
            top_eq2[2].animate.set_color(BLUE_B),
            # top_eq2[3:].animate.set_color(WHITE),
            FadeTransform(top_eq2[2].copy(), E_eq[0]),
            Write(E_eq[1:], run_time=1),
            V_eq.animate.shift(2.0 * DOWN),
        )
        self.wait()
        self.play(
            FadeTransform(E_eq[2:].copy(), top_eq3[Rf"\left({E_rhs}\right)"]),
            FadeOut(top_eq2[2], UP),
            ReplacementTransform(top_eq2[:2], top_eq3[:2]),
            ReplacementTransform(top_eq2[-11:], top_eq3[-11:]),
        )

        # Show cancellation
        final_eq = Tex(R"F = 1 + {n \choose 2} + {n \choose 4}")
        final_eq.move_to(top_eq)

        self.play(LaggedStart(
            FadeOut(E_eq, DOWN),
            FadeOut(V_eq, DOWN),
        ))
        self.play(
            # Ns
            FlashAround(top_eq3[14], color=RED),
            FlashAround(top_eq3[18], color=RED),
        )
        self.play(
            FadeOut(top_eq3[13:15], DOWN),
            FadeOut(top_eq3[18:20], DOWN),
        )
        self.play(
            # Ns
            FlashAround(top_eq3[9:13], color=RED),
            FlashAround(top_eq3[20:24], color=RED),
        )
        self.play(
            # N choose 4s
            FadeOut(top_eq3[8], DOWN),
            FadeOut(top_eq3[20:24], DOWN),
        )
        kw = dict(path_arc=90 * DEGREES)
        self.play(LaggedStart(
            Transform(top_eq3[:2], final_eq[:2], **kw),
            Transform(top_eq3[26], final_eq[2], **kw),
            Transform(top_eq3[25], final_eq[3], **kw),
            Transform(top_eq3[3:7], final_eq[4:8], **kw),
            Transform(top_eq3[7], final_eq[8], **kw),
            Transform(top_eq3[9:13], final_eq[9:13], **kw),
            *(FadeOut(top_eq3[i], DOWN) for i in [2, 15, 16, 17, 24]),
            run_time=2,
        ))
        self.wait()
