# ==============================================================================
# Scene:      SimplifyFormula
# Source:     videos/_2026/print_gallery/supplements.py (lines 645-713)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplifyFormula.py SimplifyFormula -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimplifyFormula(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.to_edge(DOWN)
        randy.body.insert_n_curves(1000)

        kw = dict(t2c={"{c}": YELLOW, "{w}": PINK}, font_size=72)
        eq1 = Tex(R"e^{{c} \cdot \ln({w})}", **kw)
        eq2 = Tex(R"=\left(e^{\ln({w})}\right)^{c}", **kw)
        eq3 = Tex(R"=\left({w}\right)^{c}", **kw)
        eq4 = Tex(R"={w}^{c}", **kw)
        eq1.next_to(randy.get_corner(UL), UP, MED_LARGE_BUFF)
        for eq in [eq2, eq3, eq4]:
            eq.next_to(eq1, RIGHT, MED_SMALL_BUFF)

        self.play(
            randy.change("raise_left_hand", eq1),
            Write(eq1[R"\ln({w})"])
        )
        self.play(Write(eq1[R"{c} \cdot"]))
        self.play(Write(eq1[R"e"]), randy.change("pondering", eq1))
        self.play(Blink(randy))
        self.wait(2)

        # Simplify
        self.play(
            randy.change("raise_right_hand", eq2),
            TransformMatchingTex(eq1.copy(), eq2)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(TransformMatchingTex(eq2, eq3))
        self.play(
            TransformMatchingTex(eq3, eq4),
            randy.change("tease")
        )
        self.play(Blink(randy))
        self.wait()

        # Add constants
        new_eq1 = Tex(R"e^{{c} \cdot \left(\ln({w}) - z_0\right) + z_0}", **kw)
        new_eq1.move_to(eq1, RIGHT)
        new_eq2 = Tex(R"= A {w}^{c}", **kw)
        new_eq2.move_to(eq2, LEFT)

        self.play(
            randy.change("pondering", new_eq1),
            TransformMatchingTex(eq1, new_eq1),
            TransformMatchingTex(eq4, new_eq2),
        )
        self.play(Blink(randy))
        self.play(randy.animate.look_at(new_eq2))
        self.wait()

        # Highlight
        rect = SurroundingRectangle(new_eq2[1:], buff=0.2)
        rect.set_stroke(TEAL, 2)
        self.play(
            randy.change("raise_right_hand"),
            ShowCreation(rect),
            new_eq1.animate.set_opacity(0.5),
        )
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("confused", new_eq2))
        self.wait()
        self.play(randy.change("maybe", eq2))
        self.wait()
