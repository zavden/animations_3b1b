# ==============================================================================
# Scene:      BitExamples
# Source:     videos/_2025/grover/qc_supplements.py (lines 553-593)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BitExamples.py BitExamples -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/BitCircuit.svg  (generated placeholder: wire with a switch and two terminals)
#   - _lib/assets/svg_images/light_switch.svg  (generated placeholder: light switch)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *

def get_bit_circuit(n_bits=4):
    circuit = SVGMobject("BitCircuit")
    circuit.set_stroke(WHITE, 2)
    circuit[-2:].set_fill(WHITE, 1)
    result = circuit.get_grid(1, n_bits, buff=0)
    return result


class BitExamples(InteractiveScene):
    def construct(self):
        # All bits
        circuit = get_bit_circuit(1)
        circuit.to_edge(LEFT, buff=0.75).to_edge(DOWN, buff=0.25)

        switch = SVGMobject("light_switch")
        switch.set_height(1.5)
        switch.to_corner(UL)
        switch.match_x(circuit)
        switch.set_fill(GREY_B)
        switch.flip(RIGHT)

        coins = Circle(radius=0.5).replicate(2)
        for coin, color, letter in zip(coins, [RED_E, BLUE_E], "TH"):
            coin.set_fill(color, 1)
            coin.set_stroke(WHITE, 2)
            coin.add(Text(letter).move_to(coin))
        coins.set_y(0).match_x(circuit)
        coins[1].flip(RIGHT)
        coins.apply_depth_test()
        op_tracker = ValueTracker(0)

        def update_coins(coins):
            index = int(op_tracker.get_value() > 0.5)
            coins[index].set_opacity(1)
            coins[1 - index].set_opacity(0)

        coins.add_updater(update_coins)

        self.play(
            Write(circuit, lag_ratio=1e-2),
            Write(switch, lag_ratio=1e-2),
            FadeIn(coins),
        )
        switch.flip(RIGHT)
        self.play(
            Rotate(coins, PI, axis=RIGHT),
            op_tracker.animate.set_value(1),
        )
        self.wait()
