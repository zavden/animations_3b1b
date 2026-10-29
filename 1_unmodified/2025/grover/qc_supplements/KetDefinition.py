# ==============================================================================
# Scene:      KetDefinition
# Source:     videos/_2025/grover/qc_supplements.py (lines 596-659)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl KetDefinition.py KetDefinition -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)



# ----- From _2025/grover/qc_supplements.py -----

class KetDefinition(InteractiveScene):
    def construct(self):
        # Test
        square = Rectangle(1, 0.75)
        dots = Tex(R"\cdots")
        dots.space_out_submobjects(0.5)
        dots.replace(square, 0).scale(0.75)
        ket = VGroup(Ket(square), dots)
        ket.set_stroke(WHITE, 3)

        ket_name = TexText(R"``ket''", font_size=60)
        ket_name.next_to(ket, UP, buff=MED_LARGE_BUFF)

        self.add(ket)
        self.play(Write(ket_name))
        self.wait()

        # Show unit vector
        arrow = Tex(R"\longrightarrow", font_size=90)

        vector = Vector(2 * UP + RIGHT, thickness=6, fill_color=TEAL)
        vector.next_to(arrow, RIGHT, MED_LARGE_BUFF)
        brace = LineBrace(vector, DOWN, buff=SMALL_BUFF)
        brace_label = brace.get_tex("1")

        self.play(
            ket.animate.next_to(arrow, LEFT, MED_LARGE_BUFF),
            MaintainPositionRelativeTo(ket_name, ket),
            Write(arrow),
        )
        self.play(GrowArrow(vector))
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_label)
        )
        self.wait()

        # Show examples of what goes inside it
        examples = VGroup(
            Tex(tex)
            for tex in [
                R"0",
                R"1",
                "+z",
                "-z",
                R"\updownarrow",
                R"E",
                R"\text{Dead}",
                R"\text{Alive}",
                R"\psi",
            ]
        )
        last = dots
        for example in examples:
            example.scale(2)
            example.set_max_width(dots.get_width())
            example.move_to(last)
            self.play(
                FadeOut(last, 0.5 * UP),
                FadeIn(example, 0.5 * UP),
                rate_func=linear,
                run_time=0.5
            )
            last = example
