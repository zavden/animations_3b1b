# ==============================================================================
# Scene:      AskAreYouSure
# Source:     videos/_2025/grover/qc_supplements.py (lines 1047-1089)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl AskAreYouSure.py AskAreYouSure -w -m --fps 15
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


class AskAreYouSure(InteractiveScene):
    def construct(self):
        # Test
        randy = Randolph()
        randy.to_edge(LEFT).shift(2 * DOWN)

        number = Integer(random.randint(0, int(1e6)))
        answer = KetGroup(number)
        answer.set_width(2)
        answer.move_to(4 * RIGHT)

        self.add(answer)
        self.add(randy)
        self.play(randy.change('pondering', answer))
        self.wait()
        self.play(randy.says("Are we...sure?", "hesitant"))
        self.play(Blink(randy))
        self.wait()

        # Show the machine
        machine = get_blackbox_machine()
        machine.to_edge(UP)
        output = Text("True", font_size=60)
        output.set_color(GREEN)
        output.next_to(machine, RIGHT, MED_LARGE_BUFF)

        self.play(
            randy.debubble("pondering", machine),
            FadeOut(answer[0]),
            number.animate.scale(1.5).next_to(machine, LEFT).set_anim_args(path_arc=-45 * DEG),
            FadeIn(machine),
        )

        self.add(number.copy().set_opacity(0.5))
        self.play(
            FadeOutToPoint(number, machine.get_center(), path_arc=-45 * DEG, lag_ratio=0.01)
        )
        self.play(
            FadeIn(output, 2 * RIGHT),
            randy.change("well", output),
        )
        self.play(Blink(randy))
        self.wait(2)
