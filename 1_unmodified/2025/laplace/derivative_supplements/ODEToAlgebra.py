# ==============================================================================
# Scene:      ODEToAlgebra
# Source:     videos/_2025/laplace/derivative_supplements.py (lines 432-462)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ODEToAlgebra.py ODEToAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_lt_group(src, trg, arrow_length=1.5, arrow_thickness=4, buff=MED_SMALL_BUFF, label_font_size=48):
    arrow = Vector(arrow_length * RIGHT, thickness=arrow_thickness)
    arrow.next_to(src, RIGHT, buff=buff)
    trg.next_to(arrow, RIGHT, buff=buff)

    label = Tex(R"\mathcal{L}", font_size=label_font_size)
    label.next_to(arrow, UP, buff=SMALL_BUFF)

    return VGroup(src, arrow, label, trg)


class ODEToAlgebra(InteractiveScene):
    def construct(self):
        # Test
        arrow_config = dict(arrow_length=2.5, buff=0.75)
        ode_group = get_lt_group(
            Text("Differential\nEquation"),
            Text("Algebra"),
            **arrow_config
        )
        ode_group.center()

        deriv_group = get_lt_group(
            Tex("d / dt", t2c={"t": BLUE}, font_size=72),
            Tex(R"\times s", t2c={"s": YELLOW}, font_size=72),
            **arrow_config
        )
        deriv_group.next_to(ode_group, DOWN, LARGE_BUFF)

        self.animate_group(ode_group)
        self.wait()
        self.animate_group(deriv_group)
        self.wait()

    def animate_group(self, group):
        src, arrow, label, trg = group
        self.play(FadeIn(src))
        self.play(LaggedStart(
            GrowArrow(arrow),
            FadeIn(label, 0.5 * arrow.get_vector()),
            FadeIn(trg, arrow.get_vector())
        ))
