# ==============================================================================
# Scene:      DivergenceTheorem
# Source:     videos/_2026/hairy_ball/supplements.py (lines 633-664)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DivergenceTheorem.py DivergenceTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DivergenceTheorem(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        div_theorem = Tex(R"""
            \displaystyle \iiint_V(\nabla \cdot \mathbf{F}) \mathrm{d} V
            = \oiint_S(\mathbf{F} \cdot \hat{\mathbf{n}}) \mathrm{d} S
        """, t2c={R"\mathbf{F}": BLUE})
        div_theorem.next_to(morty, UP, buff=1.5)
        div_theorem.to_edge(RIGHT)

        div_theorem_name = Text("Divergence Theorem", font_size=72)
        div_theorem_name.next_to(div_theorem, UP, buff=0.5)

        for pi in self.pi_creatures:
            pi.body.insert_n_curves(200)

        self.play(
            self.change_students("pondering", "confused", "tease", look_at=self.screen),
            morty.change("tease"),
        )
        self.wait(3)
        self.play(
            morty.change("raise_right_hand", div_theorem),
            FadeIn(div_theorem, shift=UP),
            self.change_students("thinking", "confused", "happy", look_at=div_theorem),
        )
        self.wait()
        self.play(Write(div_theorem_name))
        self.wait(3)
