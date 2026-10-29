# ==============================================================================
# Scene:      QuantumCompilation
# Source:     videos/_2025/grover/runtime.py (lines 1118-1293)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl QuantumCompilation.py QuantumCompilation -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/BinaryFunctionCircuit.svg  (substitute: copy of the repo's circuit.svg, printed-circuit tracks)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/state_vectors.py -----

class BitString(VGroup):
    def __init__(self, value, length=4, buff=SMALL_BUFF):
        self.length = length
        bit_mob = Integer(0)
        super().__init__(bit_mob.copy() for n in range(length))
        self.arrange(RIGHT, buff=buff)
        self.set_value(value)

    def set_value(self, value):
        bits = bin(value)[2:].zfill(self.length)
        for mob, bit in zip(self, bits):
            mob.set_value(int(bit))


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


def get_key_icon(height=0.5):
    key_icon = SVGMobject("key").rotate(135 * DEG)
    key_icon.set_fill(YELLOW)
    key_icon.set_height(height)
    return key_icon



# ----- From _2025/grover/runtime.py -----

class QuantumCompilation(InteractiveScene):
    def construct(self):
        # Show circuitry
        machine = get_blackbox_machine()
        label = machine.submobjects[0]
        machine.remove(label)
        circuit = SVGMobject("BinaryFunctionCircuit")
        circuit.flip(RIGHT)
        circuit.set_stroke(width=0)
        circuit.set_fill(BLUE_B, 1)
        circuit.set_height(machine.get_height() * 0.8)
        circuit.move_to(machine).shift(0.25 * RIGHT)
        circuit.scale(2, about_point=ORIGIN)
        circuit.sort(lambda p: np.dot(p, DR))

        self.add(machine, label)

        self.wait()
        self.play(
            machine.animate.scale(2, about_point=ORIGIN).set_fill(GREY_E),
            FadeOut(label, scale=2),
        )
        self.play(Write(circuit, lag_ratio=0.05))
        self.wait()

        # Show binary input
        number = Integer(13, font_size=72, edge_to_fix=ORIGIN)
        bit_string = BitString(number.get_value())
        bit_string.next_to(machine, LEFT)
        number.next_to(machine, LEFT, MED_LARGE_BUFF)

        bit_string.set_z_index(-1)
        output = BitString(0, length=1).scale(1.5)
        output.set_z_index(-1)
        output.next_to(machine, RIGHT, MED_LARGE_BUFF)

        self.play(FadeIn(number, RIGHT))
        self.play(
            number.animate.next_to(bit_string, UP, MED_LARGE_BUFF),
            TransformFromCopy(number.replicate(5), bit_string, lag_ratio=0.01),
        )
        self.wait()

        self.play(
            FadeOut(bit_string.copy(), 2 * RIGHT, lag_ratio=0.05, path_arc=45 * DEG),
            FadeIn(output, RIGHT, time_span=(0.75, 1.5))
        )
        self.play(
            ChangeDecimalToValue(number, 5),
            UpdateFromFunc(bit_string, lambda m: m.set_value(number.get_value())),
            run_time=1
        )
        output.set_value(1)
        self.wait()

        # Show quantum case
        c_machine = VGroup(machine, circuit)
        c_machine.target = c_machine.generate_target()
        c_machine.target.scale(0.5).to_edge(UP)

        q_machine = Square().match_style(machine).set_height(0.5 * machine.get_height())
        lines = Line(ORIGIN, 0.75 * RIGHT).get_grid(4, 1, v_buff=0.25)
        lines.next_to(q_machine, LEFT, buff=0)
        q_machine.add(lines)
        q_machine.add(lines.copy().next_to(q_machine, RIGHT, buff=0))
        q_machine.to_edge(DOWN, buff=1.5)

        q_label = Text("Quantum\nGates")  # If I were ambitious, I'd show the proper quantum circuit here
        q_label.set_color(TEAL)
        q_label.set_height(q_machine.get_height() * 0.4)
        q_label.move_to(q_machine)

        arrow = Arrow(c_machine.target, q_machine, thickness=5)

        self.play(
            MoveToTarget(c_machine),
            bit_string.animate.next_to(c_machine.target, LEFT),
            output.animate.next_to(c_machine.target, RIGHT, MED_LARGE_BUFF),
            FadeOut(number, UP),
        )
        self.play(GrowArrow(arrow))
        self.play(
            FadeTransform(c_machine[0].copy(), q_machine),
            TransformFromCopy(c_machine[1], q_label, lag_ratio=0.01, run_time=2),
        )
        self.wait()

        # Map to quantum input
        q_input = KetGroup(bit_string.copy())
        q_input.next_to(q_machine, LEFT)
        q_output = q_input.copy()
        neg = Tex(R"-").next_to(q_output, LEFT, SMALL_BUFF)
        q_output.add(neg)
        q_output.next_to(q_machine, RIGHT)

        input_rect = SurroundingRectangle(bit_string)
        input_rect.set_stroke(YELLOW, 2)
        output_rect = SurroundingRectangle(output)
        output_rect.set_stroke(GREEN, 2)
        check = Checkmark()
        check.match_height(output)
        check.set_color(GREEN)
        check.next_to(output, RIGHT)

        self.play(ShowCreation(input_rect))
        self.play(TransformFromCopy(input_rect, output_rect, path_arc=-45 * DEG))
        self.play(
            FadeOut(output_rect),
            Write(check[0], run_time=1)
        )
        self.wait()
        self.play(
            input_rect.animate.surround(q_input),
            TransformFromCopy(VGroup(VectorizedPoint(bit_string.get_center()), bit_string), q_input)
        )
        self.play(
            FadeOut(input_rect),
            FadeOut(q_input.copy(), 3 * RIGHT),
            FadeIn(q_output, 3 * RIGHT, time_span=(0.5, 1.5))
        )
        self.wait()

        # Show False inputs
        flipped_input = q_input.copy()
        flipped_output = q_output.copy()

        input_value_tracker = ValueTracker(number.get_value())
        ex = Exmark()
        ex.set_color(RED)
        ex.replace(check, 1)

        self.remove(q_output, check)
        self.add(ex)
        output.set_value(0)

        input_value_tracker.increment_value(1)
        self.play(
            input_value_tracker.animate.set_value(13).set_anim_args(rate_func=linear),
            UpdateFromFunc(bit_string, lambda m: m.set_value(int(input_value_tracker.get_value()))),
            UpdateFromFunc(q_input[1], lambda m: m.set_value(int(input_value_tracker.get_value()))),
            run_time=2
        )
        self.wait()

        q_output2 = q_input.copy()
        q_output2.next_to(q_machine, RIGHT, MED_LARGE_BUFF)
        self.play(TransformFromCopy(q_input, q_output2, path_arc=45 * DEG))
        self.wait()

        # Show combination
        combined_input = VGroup(q_input.copy(), Tex(R"+"), flipped_input)
        combined_input.arrange(DOWN, buff=SMALL_BUFF)
        combined_input.next_to(q_machine, LEFT)
        key_icon = get_key_icon()
        key_icon.match_height(q_input)
        key_icon.next_to(combined_input[2], LEFT, SMALL_BUFF)

        combined_output = VGroup(q_output2.copy(), Tex(R"+"), flipped_output)
        combined_output.arrange(DOWN, buff=SMALL_BUFF)
        combined_output.next_to(q_machine, RIGHT)

        self.play(
            ReplacementTransform(q_input, combined_input[0]),
            Write(combined_input[1:]),
            ReplacementTransform(q_output2, combined_output[0]),
            Write(combined_output[1:]),
            FadeIn(key_icon)
        )
        self.play(
            input_value_tracker.animate.set_value(5).set_anim_args(rate_func=linear),
            UpdateFromFunc(bit_string, lambda m: m.set_value(int(input_value_tracker.get_value()))),
        )
        output.set_value(1)
        self.remove(ex)
        self.add(check)
        self.wait()
