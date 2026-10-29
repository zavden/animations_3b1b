# ==============================================================================
# Scene:      ContrstClassicalAndQuantum
# Source:     videos/_2025/grover/state_vectors.py (lines 53-419)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl ContrstClassicalAndQuantum.py ContrstClassicalAndQuantum -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#   - _lib/assets/svg_images/BitCircuit.svg  (generated placeholder: wire with a switch and two terminals)
#
# Notes:
#   The grover SVGs (computer_chip, and/or/not_gate, 4-bit adder, BitCircuit, light_switch, QR, sudoku, magnifying_glass2, BinaryFunctionCircuit) are not in the public repo (Grant's Dropbox). Three were replaced with similar assets from the repo (computer_chip <- gpu.svg, magnifying_glass2 <- magnifying_glass.svg, which has the same 2nd lens subpath that get_magnifying_glass() indexes, and BinaryFunctionCircuit <- circuit.svg) and the rest were generated with _lib/assets/generated/2025/grover/make_grover_svgs.py, respecting the parts the code indexes (sudoku: 81 cells, 9 boxes, border and digits; QR: data modules and, at the end, 6 position-eye pieces; BitCircuit: the last 2 submobjects are the dots).
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/grover/qc_supplements.py -----

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


def get_classical_computer_symbol(height=2, color=GREY_B, symbol_tex=R"\mathcal{C}", symbol_color=YELLOW):
    return get_quantum_computer_symbol(height, color, symbol_tex, symbol_color)


def get_bit_circuit(n_bits=4):
    circuit = SVGMobject("BitCircuit")
    circuit.set_stroke(WHITE, 2)
    circuit[-2:].set_fill(WHITE, 1)
    result = circuit.get_grid(1, n_bits, buff=0)
    return result



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


class RandomSampling(Animation):
    def __init__(
        self,
        mobject: Mobject,
        samples: list,
        weights: list[float] | None = None,
        **kwargs
    ):
        self.samples = samples
        self.weights = weights
        super().__init__(mobject, **kwargs)

    def interpolate(self, alpha: float) -> None:
        if self.weights is None:
            target = random.choice(self.samples)
        else:
            target = random.choices(self.samples, self.weights)[0]
        self.mobject.set_submobjects(target.submobjects)


class ContrstClassicalAndQuantum(InteractiveScene):
    def construct(self):
        # Titles
        classical, quantum = symbols = VGroup(
            get_classical_computer_symbol(),
            get_quantum_computer_symbol(),
        )
        for symbol, vect in zip(symbols, [LEFT, RIGHT]):
            symbol.set_height(1)
            symbol.move_to(vect * FRAME_WIDTH / 4)
            symbol.to_edge(UP, buff=MED_SMALL_BUFF)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        v_line.set_stroke(WHITE, 1)

        self.add(symbols)
        self.add(v_line)

        # Bits
        frame = self.frame
        value = ord('C')
        short_boxed_bits = self.get_boxed_bits(12, 4)
        boxed_bits = self.get_boxed_bits(value, 8)
        for group in short_boxed_bits, boxed_bits:
            group.match_x(classical)
        boxes, bits = boxed_bits

        self.add(short_boxed_bits)
        self.wait()
        self.play(
            FadeOut(v_line, shift=2 * RIGHT),
            FadeOut(quantum, shift=RIGHT),
            ReplacementTransform(short_boxed_bits, boxed_bits),
            frame.animate.match_x(classical),
        )
        self.wait()

        # Draw layers of abstraction
        layers = Rectangle(8.0, 1.5).replicate(3)
        layers.arrange(UP, buff=0)
        layers.set_stroke(width=0)
        layers.set_fill(opacity=0.5)
        layers.set_submobject_colors_by_gradient(BLUE_E, BLUE_D, BLUE_C)
        layers.set_z_index(-1)
        layers.move_to(boxes)

        layers_name = Text("Layers\nof\nAbstraction", alignment="LEFT")
        layers_name.next_to(layers, RIGHT)

        layer_names = VGroup(
            Text("Hardware"),
            Text("Bits"),
            Text("Data types"),
        )
        layer_names.set_fill(GREY_B)
        layer_names.scale(0.6)
        for name, layer in zip(layer_names, layers):
            name.next_to(layer, LEFT, MED_SMALL_BUFF)

        num_mob = Integer(value)
        num_mob.move_to(layers[2])
        character = Text(f"'{chr(value)}'")
        character.move_to(layers[2]).shift(0.75 * RIGHT)

        circuitry = get_bit_circuit(4)
        circuitry.set_height(layers[2].get_height() * 0.7)
        circuitry.move_to(layers[0])

        self.play(
            LaggedStartMap(FadeIn, layers, lag_ratio=0.25, run_time=1),
            FadeIn(layers_name, lag_ratio=1e-2),
            Write(layer_names[1]),
        )
        self.play(
            LaggedStart(
                (TransformFromCopy(bit, num_mob)
                for bit in bits),
                lag_ratio=0.02,
            ),
            FadeIn(layer_names[2], UP),
        )
        self.wait()
        self.play(
            num_mob.animate.shift(0.75 * LEFT),
            FadeIn(character, 0.5 * RIGHT)
        )
        self.wait()
        self.play(
            Write(circuitry),
            FadeIn(layer_names[0], DOWN)
        )
        self.wait()

        # Extend layers to the quantum case
        new_layers_name = Text("Layers of Abstraction")
        new_layers_name.next_to(layers, DOWN)
        new_layers_name.match_x(quantum)

        layers.target = layers.generate_target()
        layers.target.set_width(FRAME_WIDTH, stretch=True)
        layers.target.set_x(0)

        layer_names.generate_target()
        for name, layer in zip(layer_names.target, layers.target):
            name.next_to(layer.get_left(), RIGHT, MED_SMALL_BUFF)

        self.play(
            LaggedStart(
                frame.animate.set_x(0),
                MoveToTarget(layer_names),
                FadeIn(quantum, RIGHT),
                ShowCreation(v_line),
                Transform(layers_name, new_layers_name),
                Group(num_mob, character, boxed_bits).animate.shift(RIGHT),
                circuitry.animate.scale(0.8).shift(RIGHT)
            ),
            MoveToTarget(layers, lag_ratio=0.01),
        )
        self.wait()

        # Show quantum material
        qubit_string = BitString(0, length=8)
        qubit_string.set_value(ord("Q"))
        qubit_ket = Ket(qubit_string)
        qubits = VGroup(qubit_ket, qubit_string)

        qunit_num = Integer(ord("Q"))
        qunit_ket = Ket(qunit_num)
        qunit = VGroup(qunit_ket, qunit_num)

        ion = Group(
            GlowDot(color=RED, radius=0.5),
            Dot(radius=0.1).set_fill(RED, 0.5),
            Tex(R"+", font_size=14).set_fill(border_width=1)
        )
        trapped_ions = Group(ion.copy().shift(x * RIGHT) for x in np.linspace(0, 4, 8))

        for mob, layer in zip([trapped_ions, qubits, qunit], layers):
            mob.move_to(layer).match_x(quantum)

        for ion, bit in zip(trapped_ions, qubit_string):
            if bit.get_value() == 1:
                ion[0].set_opacity(0)

        self.play(LaggedStartMap(FadeIn, trapped_ions))
        self.wait()
        self.play(FadeIn(qubits, UP))
        self.wait()
        self.play(
            TransformFromCopy(qubits, qunit)
        )
        self.wait()
        value_tracker = ValueTracker(ord("Q"))
        for value in [ord('C'), ord('Q')]:
            self.play(
                value_tracker.animate.set_value(value),
                UpdateFromFunc(qunit_num, lambda m: m.set_value(int(value_tracker.get_value()))),
                UpdateFromFunc(qubit_string, lambda m: m.set_value(int(value_tracker.get_value()))),
                rate_func=linear,
                run_time=1.0
            )
            self.wait(0.25)

        # Show some measurements
        lasers = VGroup()
        for ion in trapped_ions:
            point = ion.get_center()
            laser = Line(point + 0.5 * DL, point)
            laser.insert_n_curves(20)
            laser.set_stroke(RED, [1, 3, 3, 3, 1])
            lasers.add(laser)

        for value in [*np.random.randint(0, 2**8, 4), ord("Q")]:
            qubit_string.generate_target()
            qunit_num.generate_target()
            trapped_ions.generate_target()
            qunit_num.target.set_value(value)
            qubit_string.target.set_value(value)
            for ion, bit in zip(trapped_ions.target, qubit_string.target):
                ion[0].set_opacity(1.0 - bit.get_value())
            self.play(
                LaggedStartMap(VShowPassingFlash, lasers, lag_ratio=0.1, time_width=2.0, run_time=2),
                MoveToTarget(trapped_ions, lag_ratio=0.1, time_span=(0.5, 2.0)),
                MoveToTarget(qubit_string, lag_ratio=0.1, time_span=(0.5, 2.0)),
                MoveToTarget(qunit_num, time_span=(1.0, 1.25)),
                Transform(qunit_ket, Ket(qunit_num.target), time_span=(1.0, 1.5)),
            )

        # Describe a ket
        morty = Mortimer(height=5)
        morty.move_to(np.array([13., -6., 0.]))
        big_ket = Ket(Square(1))
        big_ket.set_fill(border_width=3)
        big_ket.next_to(morty.get_corner(UL), UP, MED_LARGE_BUFF)
        big_ket_name = TexText("``ket''", font_size=96)
        big_ket_name.next_to(big_ket, UP, MED_LARGE_BUFF)

        self.play(
            frame.animate.reorient(0, 0, 0, (4.66, -2.55, 0.0), 13.19),
            morty.change("raise_right_hand", big_ket),
            VFadeIn(morty),
            *(
                TransformFromCopy(src, big_ket)
                for src in [qubit_ket, qunit_ket]
            ),
        )
        self.play(
            Write(big_ket_name, time_span=(0.75, 2.0)),
            FlashAround(big_ket, time_width=1.5, run_time=2)
        )
        self.wait()

        # Refocus
        self.remove(big_ket)
        self.play(LaggedStart(
            FadeOut(VGroup(morty, big_ket, big_ket_name)),
            TransformFromCopy(big_ket, qubit_ket),
            TransformFromCopy(big_ket, qunit_ket),
            frame.animate.to_default_state(),
        ))

        # Expand mid layer
        mid_layer = layers[1]
        mid_layer.set_z_index(-2)
        mid_layer.generate_target()
        mid_layer.target.set_height(7, stretch=True)
        mid_layer.target.move_to(layers, UP)
        mid_layer.target.set_fill(opacity=0.25)

        target_y = -1.0

        self.play(
            FadeOut(
                VGroup(layers[2], num_mob, character, qunit, layer_names[2]),
                UP,
            ),
            FadeOut(
                Group(layers[0], circuitry, trapped_ions, layer_names[0]),
                DOWN,
            ),
            FadeOut(layers_name, DOWN),
            qubits.animate.set_y(target_y),
            boxed_bits.animate.match_x(classical).set_y(target_y),
            layer_names[1].animate.set_y(target_y),
            MoveToTarget(mid_layer, time_span=(0.5, 2.0)),
            run_time=2
        )
        self.play(
            FadeOut(layers[1]),
            FadeOut(layer_names[1]),
            run_time=3
        )

        # Show state vs. what you read, classical
        contrast = VGroup(
            Text("State"),
            Tex(R"=", font_size=72),
            Text("What you see"),
        )
        contrast.arrange(RIGHT)
        contrast[2].align_to(contrast[0], UP)
        contrast.match_x(classical)
        contrast.set_y(0.5)
        contrast.shift(0.5 * RIGHT)

        boxed_bits_copy = boxed_bits.copy()
        boxed_bits_copy.scale(0.7)
        boxed_bits_copy.stretch(0.8, 0)
        for bit in boxed_bits_copy[1]:
            bit.stretch(1 / 0.8, 0)
        boxed_bits_copy.next_to(contrast[2], DOWN, buff=0.75)
        boxed_bits_copy[0].set_stroke(WHITE, 1)

        boxed_bits.target = boxed_bits_copy.copy()
        boxed_bits.target.match_x(contrast[0])

        self.play(
            FadeIn(contrast[::2]),
            MoveToTarget(boxed_bits),
        )
        self.play(
            Write(contrast[1]),
            TransformFromCopy(boxed_bits, boxed_bits_copy, path_arc=30 * DEG),
        )
        self.wait()
        self.play(*(
            LaggedStart(
                (bit.animate.set_stroke(YELLOW, 3).set_anim_args(rate_func=there_and_back)
                for bit in group[1]),
                lag_ratio=0.25,
                run_time=4
            )
            for group in [boxed_bits, boxed_bits_copy]
        ))
        self.wait()

        # Show state vs. what you read, quantum
        q_contrast = contrast.copy()
        q_contrast.match_x(quantum)
        ne = Tex(R"\ne", font_size=72)
        ne.move_to(q_contrast[1])
        ne.set_color(RED)
        q_contrast[1].become(ne)

        state_vector = Vector(UR, thickness=4)
        state_vector.set_color(TEAL)
        state_vector.next_to(q_contrast[0], DOWN, MED_LARGE_BUFF)
        state_vector.set_opacity(0)  # Going to overlap something else instead

        state_vector_outline = state_vector.copy().set_fill(opacity=0)
        state_vector_outline.set_stroke(BLUE_A, 3)
        state_vector_outline.insert_n_curves(100)

        qubits.generate_target()
        qubits.target[1].space_out_submobjects(0.8)
        qubits.target[0].become(Ket(qubits.target[1]))
        qubits.target.match_x(q_contrast[2]).match_y(state_vector)

        moving_rect = SurroundingRectangle(state_vector)
        moving_rect.set_stroke(YELLOW, 3, 0)

        self.play(LaggedStart(
            TransformFromCopy(contrast, q_contrast, path_arc=-45 * DEG),
            MoveToTarget(qubits),
            GrowArrow(state_vector),
        ))
        self.wait()
        self.play(moving_rect.animate.surround(qubits).set_stroke(YELLOW, 3, 1))
        self.play(FadeOut(moving_rect))
        self.play(
            value_tracker.animate.set_value(0).set_anim_args(rate_func=there_and_back, run_time=4),
            UpdateFromFunc(qubit_string, lambda m: m.set_value(int(value_tracker.get_value()))),
        )
        self.wait()

        # Show randomness
        qubit_samples = list()
        for n in range(2**8):
            sample = qubits.copy()
            sample[1].set_value(n)
            sample.shift(np.random.uniform(-0.05, 0.05, 3))
            sample.set_stroke(TEAL, 1)
            qubit_samples.append(sample)

        labels = VGroup(Text("Random"), Text("Deterministic"))
        for label, mob, color in zip(labels, [qubits, boxed_bits_copy], [TEAL, YELLOW]):
            label.scale(0.75)
            label.next_to(mob, DOWN, buff=MED_LARGE_BUFF)
            label.set_color(color)

        self.play(
            FadeIn(labels),
            RandomSampling(qubits, qubit_samples),
        )
        self.wait()
        for _ in range(8):
            self.play(RandomSampling(qubits, qubit_samples))
            self.wait()

    def get_boxed_bits(self, value, length, height=0.5):
        boxes = Square().get_grid(1, length, buff=0)
        boxes.set_height(height)
        boxes.set_stroke(WHITE, 2)
        bits = BitString(value, length)
        for bit, box in zip(bits, boxes):
            bit.move_to(box)
        return VGroup(boxes, bits)
