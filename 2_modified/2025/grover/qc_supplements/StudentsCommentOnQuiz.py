# ==============================================================================
# Scene:      StudentsCommentOnQuiz
# Source:     videos/_2025/grover/qc_supplements.py (lines 222-276)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl StudentsCommentOnQuiz.py StudentsCommentOnQuiz -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

def get_quantum_computer_symbol(height=2, color=GREY_B, symbol_tex=R"|Q\rangle", symbol_color=TEAL):
    chip = SVGMobject("computer_chip")
    chip.set_height(height)
    chip.to_edge(RIGHT)
    chip.set_fill(GREY_C)
    chip.set_shading(0.7, 0, 0)
    symbol = Tex(symbol_tex)
    symbol.set_fill(symbol_color)
    symbol.set_stroke(symbol_color, 1)
    symbol.set_height(0.4 * chip.get_height())
    symbol.move_to(chip)

    result = VGroup(chip, symbol)
    return result


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


class StudentsCommentOnQuiz(TeacherStudentsScene):
    def construct(self):
        # Ask about quantum computer
        morty = self.teacher
        for pi in self.pi_creatures:
            pi.body.insert_n_curves(100)

        qc = get_quantum_computer_symbol(height=1.5)
        qc.move_to(self.hold_up_spot, DOWN)
        qc_outline = qc.copy()
        qc_outline.set_fill(opacity=0).set_stroke(TEAL, 2)

        q_marks = VGroup(
            Text("?!?", font_size=72).next_to(std, UP)
            for std in self.students
        )

        self.play(
            morty.change("raise_right_hand"),
            FadeIn(qc, UP),
            self.change_students("confused", "horrified", "angry"),
            LaggedStartMap(FadeIn, q_marks, shift=0.25 * UP),
        )
        self.play(
            VShowPassingFlash(qc_outline, time_width=2, run_time=3),
            Blink(morty),
        )
        self.wait(4)

        # Reference alternate version of blackbox function
        std = self.students[2]
        machine = get_blackbox_machine(height=1.0)
        machine.next_to(std.get_corner(UR), UP)
        arrow = Tex(R"\updownarrow").set_height(1)
        arrow.next_to(machine, UP)

        self.play(LaggedStart(
            FadeOut(q_marks[:2], lag_ratio=0.1),
            self.change_students("pondering", "erm", "raise_right_hand"),
            morty.change("tease"),
            qc.animate.next_to(arrow, UP),
            FadeIn(machine),
            q_marks[2].animate.next_to(arrow, LEFT),
            Write(arrow),
        ))
        self.wait(5)

        # Thought bubble
        bubble = ThoughtBubble().pin_to(std)
        self.play(
            self.change_students("pondering", "pondering", "thinking", look_at=self.screen, lag_ratio=0.1),
            FadeIn(bubble, lag_ratio=0.2),
            LaggedStartMap(FadeOut, VGroup(machine, arrow, q_marks[2], qc), shift=LEFT, lag_ratio=0.1, run_time=1)
        )
        self.wait(3)
