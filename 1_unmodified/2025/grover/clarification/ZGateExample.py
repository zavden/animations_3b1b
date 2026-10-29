# ==============================================================================
# Scene:      ZGateExample
# Source:     videos/_2025/grover/clarification.py (lines 1046-1115)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl ZGateExample.py ZGateExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

class Ket(Tex):
    def __init__(self, mobject, height_scale_factor=1.25, buff=SMALL_BUFF):
        super().__init__(R"| \rangle")
        self.set_height(height_scale_factor * mobject.get_height())
        self[0].next_to(mobject, LEFT, buff)
        self[1].next_to(mobject, RIGHT, buff)


class KetGroup(VGroup):
    def __init__(self, mobject, **kwargs):
        ket = Ket(mobject, **kwargs)
        super().__init__(ket, mobject)



# ----- From _2025/grover/qc_supplements.py -----

def get_blackbox_machine(height=2, color=GREY_D, label_tex="f(n)", label_height_ratio=0.25):
    square = Square(height)
    in_tri = ArrowTip().set_height(0.5 * height)
    out_tri = in_tri.copy().rotate(PI)
    in_tri.move_to(square.get_left())
    out_tri.move_to(square.get_right())
    machine = Union(square, in_tri, out_tri)
    machine.set_fill(color, 1)
    machine.set_stroke(WHITE, 2)

    label = Tex(label_tex)
    label.set_height(label_height_ratio * height)
    label.move_to(machine)
    machine.add(label)

    machine.output_group = VGroup()

    return machine



# ----- From _2025/grover/clarification.py -----

class ZGateExample(InteractiveScene):
    def construct(self):
        # Test
        z_gates = VGroup(get_blackbox_machine(label_tex="Z") for n in range(3))
        z_gates.scale(0.35)
        z_gates.arrange(DOWN, buff=LARGE_BUFF)
        z_gates.move_to(4 * LEFT + UP)
        for gate in z_gates:
            gate[-1].set_color(TEAL)
            gate[-1].scale(1.5)

        zero, one = kets = VGroup(
            KetGroup(Integer(0)),
            KetGroup(Integer(1)),
        )
        gen_input = VGroup(Tex(R"x"), zero.copy(), Tex(R"+"), Tex(R"y"), one.copy())
        gen_input.arrange(RIGHT, buff=SMALL_BUFF)
        inputs = VGroup(zero, one, gen_input)
        for in_group, gate in zip(inputs, z_gates):
            in_group.next_to(gate, LEFT)

        # Act on zero, then one
        outputs = VGroup(
            zero.copy().next_to(z_gates[0], RIGHT),
            VGroup(Tex("-"), one.copy()).arrange(RIGHT, buff=SMALL_BUFF).next_to(z_gates[1], RIGHT)
        )

        self.play(FadeIn(z_gates[0]))
        self.wait()
        self.play(FadeIn(zero, RIGHT))
        self.play(LaggedStart(
            FadeOutToPoint(zero.copy(), z_gates[0].get_center(), lag_ratio=0.05),
            FadeInFromPoint(outputs[0], z_gates[0].get_center(), lag_ratio=0.05),
            lag_ratio=0.5
        ))
        self.wait()
        self.play(
            TransformFromCopy(*z_gates[:2]),
            TransformFromCopy(*kets),
        )
        self.play(LaggedStart(
            FadeOutToPoint(one.copy(), z_gates[1].get_center(), lag_ratio=0.05),
            FadeInFromPoint(outputs[1], z_gates[1].get_center(), lag_ratio=0.05),
            lag_ratio=0.5
        ))
        self.wait()

        # General input
        self.play(
            TransformFromCopy(*z_gates[1:3]),
            TransformFromCopy(kets, gen_input[1::3]),
            *(FadeIn(gen_input[i]) for i in [0, 2, 3])
        )
        self.wait()

        rhss = VGroup(
            Tex(R"xZ|0\rangle + y Z|1\rangle ", t2c={"Z": TEAL}),
            Tex(R"x |0\rangle - y |1\rangle"),
        )
        rhss[0].next_to(z_gates[2], RIGHT)
        rhss[1].next_to(rhss[0], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(LaggedStart(
            FadeOutToPoint(gen_input.copy(), z_gates[2].get_center(), lag_ratio=0.01),
            FadeInFromPoint(rhss[0], z_gates[2].get_center(), lag_ratio=0.01),
            lag_ratio=0.5
        ))
        self.wait()
        self.play(FadeIn(rhss[1], DOWN))
        self.wait()
