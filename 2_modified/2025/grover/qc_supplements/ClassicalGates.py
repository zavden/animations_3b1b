# ==============================================================================
# Scene:      ClassicalGates
# Source:     videos/_2025/grover/qc_supplements.py (lines 662-724)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ClassicalGates.py ClassicalGates -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/and_gate.svg  (generated placeholder: ANSI AND gate with terminals)
#   - _lib/assets/svg_images/or_gate.svg  (generated placeholder: ANSI OR gate with terminals)
#   - _lib/assets/svg_images/not_gate.svg  (generated placeholder: ANSI NOT gate with terminals)
#   - _lib/assets/svg_images/Four_bit_adder_with_carry_lookahead.svg  (generated placeholder: diagram of a 4-bit carry-lookahead adder, 158 strokes)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

class ClassicalGates(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Logic Gates", font_size=60)
        title.to_edge(UP)
        self.add(title)

        # Basic gates
        gates = VGroup(
            SVGMobject("and_gate"),
            SVGMobject("or_gate"),
            SVGMobject("not_gate"),
        )
        gates.get_width()
        gates.set_width(2.0)
        gates.set_fill(GREY_B)
        gates.arrange(RIGHT, buff=2)
        gates.set_y(0)

        gate_names = VGroup(map(Text, ["AND", "OR", "NOT"]))
        for name, gate in zip(gate_names, gates):
            name.set_color(GREY_B)
            name.next_to(gate, DOWN)

        self.play(
            LaggedStartMap(Write, gates, lag_ratio=0.5),
            LaggedStartMap(Write, gate_names, lag_ratio=0.5),
        )

        # Bit examples
        inputs = VGroup(Text("01"), Text("01"), Text("0"))
        outputs = VGroup(Text("0"), Text("1"), Text("1"))
        for in_bits, out_bit, gate in zip(inputs, outputs, gates):
            in_bits.arrange(DOWN)
            in_bits.arrange_to_fit_height(1)
            in_bits.next_to(gate, LEFT, buff=SMALL_BUFF)
            out_bit.next_to(gate, RIGHT, buff=SMALL_BUFF)

        self.play(LaggedStartMap(FadeIn, inputs, shift=0.5 * RIGHT, lag_ratio=0.2, run_time=1.0)),
        self.play(LaggedStart(
            *(FadeOut(in_bit.copy(), RIGHT) for in_bit in inputs),
            *(FadeIn(out_bit, 0.5 * RIGHT) for out_bit in outputs),
            lag_ratio=0.2
        ))
        self.add(inputs, outputs)

        # Show full circuit
        gate_groups = VGroup(
            VGroup(gate, name, in_bits, out_bits)
            for gate, name, in_bits, out_bits in zip(gates, gate_names, inputs, outputs)
        )

        circuit = SVGMobject("Four_bit_adder_with_carry_lookahead")
        circuit.set_height(5)
        circuit.to_edge(DOWN, buff=0.25)
        circuit.set_fill(opacity=0)
        circuit.set_stroke(WHITE, 1)

        self.play(
            gate_groups.animate.scale(0.35).space_out_submobjects(0.9).next_to(title, DOWN, MED_LARGE_BUFF),
            Write(circuit, run_time=3)
        )
        self.wait()
