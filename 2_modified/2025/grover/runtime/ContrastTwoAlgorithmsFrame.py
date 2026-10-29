# ==============================================================================
# Scene:      ContrastTwoAlgorithmsFrame
# Source:     videos/_2025/grover/runtime.py (lines 1053-1115)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py, _2025/grover/state_vectors.py
#
# Run from this folder:
#     manimgl ContrastTwoAlgorithmsFrame.py ContrastTwoAlgorithmsFrame -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
#   - _lib/assets/svg_images/magnifying_glass2.svg  (substitute: copy of the repo's magnifying_glass.svg)
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


class DisectAQuantumComputer(InteractiveScene):
    def construct(self):
        # Set up the machine with a random pile of gates
        wires = Line(4 * LEFT, 4 * RIGHT).replicate(4)
        wires.arrange(DOWN, buff=0.5)
        wires.shift(LEFT)

        gates = VGroup(
            self.get_labeled_box(wires[0], 0.1),
            self.get_cnot(wires[1], wires[0], 0.2),
            self.get_cnot(wires[3], wires[1], 0.3),
            self.get_cnot(wires[2], wires[3], 0.4),
            self.get_labeled_box(wires[3], 0.5, "X"),
            self.get_labeled_box(wires[1], 0.5, "Z"),
            self.get_cnot(wires[2], wires[1], 0.6),
            self.get_labeled_box(wires[1], 0.7),
            self.get_cnot(wires[3], wires[1], 0.8),
            self.get_cnot(wires[0], wires[1], 0.9),
        )
        mes_gates = VGroup(
            self.get_measurement(wires[0], 1),
            self.get_measurement(wires[1], 1),
            self.get_measurement(wires[2], 1),
            self.get_measurement(wires[3], 1),
        )

        circuit = Group(wires, Point(), gates, mes_gates)
        machine_rect = SurroundingRectangle(circuit)
        machine_rect.set_stroke(TEAL, 2)
        qc_label = get_quantum_computer_symbol(height=1)
        qc_label.next_to(machine_rect, UP)

        self.add(circuit, machine_rect, qc_label)

        # Show a program running through quantum wires (TODO< show the results)
        n_repetitions = 25

        wire_glows = Group(
            GlowDot(wire.get_start(), color=TEAL, radius=0.25)
            for wire in wires
        )
        wire_glows.set_z_index(-1)
        gate_glows = gates.copy()
        gate_glows.set_stroke(TEAL, 1)
        gate_glows.set_fill(opacity=0)
        for glow in gate_glows:
            glow.add_updater(lambda m: m.set_stroke(width=4 * np.exp(
                -(0.5 * (m.get_x() - wire_glows.get_x()))**2
            )))

        output = self.get_random_qubits()
        output.next_to(machine_rect, RIGHT, buff=LARGE_BUFF)

        for n in range(n_repetitions):
            self.add(gate_glows)
            wire_glows.set_x(wires.get_x(LEFT))
            wire_glows.set_opacity(1)
            self.play(
                wire_glows.animate.match_x(mes_gates),
                rate_func=linear,
                run_time=1
            )
            output_value = random.randint(0, 15)
            output[0].set_value(output_value)
            for mes_gate, bit in zip(mes_gates, output[0]):
                mes_gate[-1].set_stroke(opacity=0)
                mes_gate[-1][bit.get_value()].set_stroke(opacity=1)
            self.add(output)
            wire_glows.set_opacity(0)
            self.play(wire_glows.animate.shift(6 * RIGHT), rate_func=linear)

        self.remove(wire_glows, gate_glows)

        # Setup all 16 outputs
        machine = Group(circuit, machine_rect, qc_label)
        all_qubits = output.replicate(16)
        for n, qubits in enumerate(all_qubits):
            qubits[0].set_value(n)
        all_qubits.arrange(DOWN)
        all_qubits.set_height(FRAME_HEIGHT - 1)
        all_qubits.move_to(machine, RIGHT)
        all_qubits.set_y(0)

        all_qubit_rects = VGroup(
            SurroundingRectangle(qubits, buff=0.05).set_stroke(YELLOW, 1, 0.5)
            for qubits in all_qubits
        )
        output_rect = SurroundingRectangle(output)

        brace = Brace(all_qubit_rects, RIGHT, SMALL_BUFF)
        brace_label = brace.get_tex("2^4 = 16")
        brace_label.shift(0.2 * RIGHT + 0.05 * UP)

        self.play(ShowCreation(output_rect))
        self.wait()
        self.remove(output, output_rect)
        self.play(
            machine.animate.to_edge(LEFT),
            TransformFromCopy(VGroup(output), all_qubits),
            TransformFromCopy(VGroup(output_rect), all_qubit_rects),
        )
        self.play(
            GrowFromCenter(brace),
            Write(brace_label),
        )
        self.wait()

        # Show probability distribution
        qc_label.generate_target()
        qc_label.target.set_y(0).scale(1.5)
        comp_to_dist_arrow = Arrow(qc_label.target, all_qubits, buff=1.0, thickness=6)

        dists = [
            np.random.randint(1, 8, 16).astype(float),
            np.random.random(16) + 10 * np.eye(16)[10],
            np.random.random(16) + 5,
            np.random.randint(1, 8, 16).astype(float),
        ]
        for dist in dists:
            dist /= dist.sum()

        all_dist_rects = VGroup(
            self.get_dist_bars(dist, all_qubits, width_ratio=6)
            for dist in dists
        )
        dist_rects = all_dist_rects[0]

        dist_rect_labels = VGroup(
            Integer(100 * prob, unit=R"\%", font_size=24, num_decimal_places=1).next_to(rect, RIGHT, SMALL_BUFF)
            for prob, rect in zip(dists[0], dist_rects)
        )

        self.play(
            FadeOut(machine_rect, DOWN),
            FadeOut(circuit, DOWN),
            MoveToTarget(qc_label)
        )
        self.play(
            GrowArrow(comp_to_dist_arrow),
            ReplacementTransform(all_qubit_rects, dist_rects, lag_ratio=0.1),
            FadeOut(brace, RIGHT),
            FadeOut(brace_label, RIGHT),
        )
        self.wait()
        self.play(LaggedStartMap(FadeIn, dist_rect_labels, shift=0.25 * RIGHT, lag_ratio=0.1, run_time=2))
        self.wait(2)
        self.play(FadeOut(dist_rect_labels))
        self.wait()
        for new_rects in all_dist_rects[1:]:
            self.play(Transform(dist_rects, new_rects, run_time=2))
            self.wait()

        # Show magnifying glass
        if False:
            # This is just ment for an insertion
            dist = VGroup(all_qubits, dist_rects)
            dist.shift(0.25 * LEFT)
            qc_label.scale(1.5).next_to(comp_to_dist_arrow, LEFT, MED_LARGE_BUFF)
            glass = get_magnifying_glass()
            glass.next_to(qc_label, UL).to_edge(UP)
            glass.save_state()
            dist_rects.save_state()

            wigglers = Superposition(
                VGroup(VGroup(qb, bar) for qb, bar in zip(all_qubits, dist_rects)).copy(),
                max_rot_vel=8,
                glow_stroke_opacity=0
            )

            index = 7
            new_dist = np.zeros(16)
            new_dist[index] = 7
            choice_rect = SurroundingRectangle(all_qubits[index])

            new_bars = self.get_dist_bars(new_dist, all_qubits, width_ratio=3)
            new_bars.set_stroke(width=0)
            new_bars[index].set_stroke(WHITE, 1)

            self.play(FadeIn(glass))
            for _ in range(2):
                self.play(
                    glass.animate.shift(qc_label.get_center() - glass[0].get_center()).set_anim_args(path_arc=-45 * DEG),
                    Transform(dist_rects, new_bars, time_span=(1.25, 1.5)),
                    FadeIn(choice_rect, time_span=(1.25, 1.5)),
                    run_time=2
                )
                self.wait()
                self.play(
                    Restore(glass, path_arc=45 * DEG),
                    FadeOut(choice_rect, time_span=(0.25, 0.5)),
                    run_time=1.5
                )
                self.wait()

            # Delicate state
            wigglers.set_offset_multiple(0)
            self.play(FadeOut(dist), FadeIn(wigglers))
            self.play(wigglers.animate.set_offset_multiple(0.05))
            self.wait(8)

            # For the chroma key
            qubits = all_qubits[index].copy()
            qubits.set_width(0.7 * qc_label.get_width()).move_to(qc_label)
            qubits.set_fill(border_width=3)

            self.clear()
            self.add(qubits)

        # Label it as 4 qubit
        title = Text("4 qubit quantum computer")
        title.next_to(qc_label, UP, buff=LARGE_BUFF)
        title.set_backstroke(BLACK, 3)
        underline = Underline(title, buff=-0.05)

        self.play(
            ShowCreation(underline, time_span=(1, 2)),
            Write(title, run_time=2),
        )
        self.wait()

        # k qubit case
        last_sym = title["4"][0]
        last_qubits = all_qubits
        last_dist_rects = dist_rects
        for k in [5, 6, "k"]:
            k_sym = Tex(str(k))
            k_sym.move_to(last_sym)
            k_sym.set_color(YELLOW)

            n_bits = k if isinstance(k, int) else 7

            multi_bitstrings = VGroup(
                BitString(n, length=n_bits)
                for n in range(2**n_bits)
            )
            new_qubits = VGroup(
                VGroup(bits, Ket(bits))
                for bits in multi_bitstrings
            )
            new_qubits.arrange(DOWN)
            new_qubits.set_height(FRAME_HEIGHT - 1)
            new_qubits.move_to(all_qubits)
            big_dist_rects = self.get_dist_bars(np.random.random(2**n_bits)**2, new_qubits)

            self.play(
                FadeOut(last_sym, 0.25 * UP),
                FadeIn(k_sym, 0.25 * UP),
                FadeOut(last_qubits),
                FadeOut(last_dist_rects),
                FadeIn(new_qubits),
                FadeIn(big_dist_rects),
            )
            self.wait()

            last_sym = k_sym
            last_qubits = new_qubits
            last_dist_rects = big_dist_rects

        # Count all outputs
        brace = Brace(last_dist_rects, RIGHT, SMALL_BUFF)
        brace_label = Tex(R"2^k", t2c={"k": YELLOW})
        brace_label.next_to(brace, RIGHT)

        bits = BitString(70, length=7)
        longer_example = last_qubits[100].copy().set_width(2.0)
        longer_example.next_to(brace_label, DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)

        down_brace = Brace(longer_example[0], DOWN, SMALL_BUFF)
        down_brace_label = down_brace.get_tex("k").set_color(YELLOW)

        self.play(
            GrowFromCenter(brace),
            TransformFromCopy(last_sym, brace_label),
        )
        self.play(
            TransformFromCopy(last_qubits[70], longer_example),
        )
        self.play(
            GrowFromCenter(down_brace),
            TransformFromCopy(brace_label[1], down_brace_label)
        )
        self.wait()

        # Highlight the word qubit
        word_rect = SurroundingRectangle(title["qubit"], buff=0.1)
        word_rect.set_stroke(YELLOW, 2)
        self.play(ReplacementTransform(underline, word_rect))
        self.wait()
        title[0].set_opacity(0)
        self.play(
            FadeOut(title),
            FadeOut(word_rect),
            FadeOut(last_sym),
            LaggedStartMap(FadeOut, VGroup(brace, brace_label, longer_example, down_brace, down_brace_label)),
            FadeOut(last_qubits),
            FadeOut(last_dist_rects),
            FadeIn(all_qubits),
            FadeIn(dist_rects),
        )
        self.wait()

        # Emphasize you see only one
        frame = self.frame

        dist_rect = SurroundingRectangle(VGroup(comp_to_dist_arrow, all_qubits, dist_rects), buff=0.25)
        dist_rect.set_stroke(BLUE, 2)
        dist_rect.stretch(1.2, 0)
        output.set_width(2)
        output.next_to(dist_rect, RIGHT, buff=2.5)
        output.align_to(all_qubits, UP)

        dist_words = Text("Implicit", font_size=72)
        dist_words.next_to(dist_rect, UP)
        output_words = Text("What you see", font_size=72)
        output_words.next_to(output, UP).match_y(dist_words)

        sample_rects = VGroup(
            SurroundingRectangle(qb, buff=0.05)
            for qb, bar in zip(all_qubits, dist_rects)
        )
        sample_rects.set_stroke(YELLOW, 1)
        sample = 6
        output[0].set_value(sample)

        self.play(LaggedStart(
            frame.animate.reorient(0, 0, 0, (4.2, 0.7, 0.0), 9.86),
            FadeIn(dist_rect),
            FadeIn(dist_words, lag_ratio=0.1),
            FadeIn(output),
            FadeIn(output_words, lag_ratio=0.1),
            FadeIn(sample_rects[sample]),
            lag_ratio=0.2
        ))

        # Don't see multiple at once
        superposition_pieces = all_qubits.copy()
        superposition_pieces.set_width(1.5)
        superposition_pieces.space_out_submobjects(0.5)
        superposition_pieces.move_to(output, UP)
        superposition = Superposition(superposition_pieces)
        big_cross = Cross(superposition, stroke_width=[0, 15, 15, 15, 0])

        self.play(
            FadeIn(superposition),
            FadeOut(output),
            ShowCreation(big_cross)
        )
        self.wait(6)
        self.play(
            FadeOut(superposition),
            FadeOut(big_cross),
        )

        # Show some random samples
        n_samples = 8
        output_choices = output.replicate(16)
        for n, choice, sample_rect in zip(it.count(), output_choices, sample_rects):
            choice[0].set_value(n)
            choice.shift(np.random.uniform(-0.1, 0.1, 3))
            choice.set_backstroke(TEAL, 2)
            choice.add(sample_rect)

        self.remove(output, sample_rects)
        selection = VGroup()
        for _ in range(n_samples):
            self.play(RandomSampling(selection, list(output_choices), weights=dists[-1]))
            self.wait()

        # Concentrate probability to one value
        conc_dist = np.zeros(16)
        num = 7
        conc_dist[num] = 1
        new_rects = self.get_dist_bars(conc_dist, all_qubits, width_ratio=2.0)
        self.play(
            FadeOut(selection),
            Transform(dist_rects, new_rects),
            dist_rect.animate.stretch(1.2, 0, about_edge=LEFT),
            UpdateFromFunc(dist_words, lambda m: m.match_x(dist_rect)),
            output_words.animate.shift(RIGHT),
        )
        self.wait()
        self.play(ShowCreation(sample_rects[num]))
        output[0].set_value(num)
        output.match_x(output_words)
        self.play(TransformFromCopy(all_qubits[num], output))
        self.wait()

        # Back to another distribution
        point1_index = 2
        point5_index = 3
        new_dist = np.random.random(16)
        new_dist[point1_index] = new_dist[point5_index] = 0
        new_dist *= (1.0 - 0.25 - 0.01) / new_dist.sum()
        new_dist[point1_index] = 0.01
        new_dist[point5_index] = 0.25

        self.play(Transform(dist_rects, self.get_dist_bars(new_dist, all_qubits)))
        self.remove(output, selection, sample_rects)
        VGroup(choice[:-1] for choice in output_choices).match_x(output_words)
        self.play(RandomSampling(selection, list(output_choices), weights=new_dist))
        self.remove(selection)
        self.add(output, sample_rects[num])
        self.wait()

        # Ask where the distribution comes from
        q_marks = Tex(R"???", font_size=96)
        dist_group = VGroup(all_qubits, dist_rects)
        q_marks.next_to(dist_group, UP, MED_LARGE_BUFF)

        self.play(
            dist_rect.animate.surround(dist_group),
            FadeTransformPieces(dist_words, q_marks),
        )
        self.wait()

        dist_group.add(dist_rect)

        # Introduce the state vector
        state = np.array([random.choice([-1, 1]) * np.sqrt(p) for p in new_dist])
        state[point5_index] = 0.5
        state[point1_index] = -0.1
        state_vector = DecimalMatrix(np.zeros((16, 1)), decimal_config=dict(include_sign=True, edge_to_fix=LEFT))
        for value, elem in zip(state, state_vector.elements):
            elem.set_value(value)
        state_vector.match_height(all_qubits)
        state_vector.next_to(qc_label, RIGHT, LARGE_BUFF)

        vector_title = Text("State Vector", font_size=60)
        vector_title.set_color(TEAL)
        vector_title.next_to(state_vector, UP, MED_LARGE_BUFF)

        comp_to_dist_arrow.target = comp_to_dist_arrow.generate_target()
        comp_to_dist_arrow.target.next_to(state_vector, RIGHT)

        vect_lines = self.get_connecting_lines(qc_label, state_vector, from_buff=-0.1, to_buff=0.1)

        self.play(LaggedStart(
            ShowCreation(vect_lines, lag_ratio=0),
            FadeInFromPoint(state_vector, qc_label.get_right()),
            MoveToTarget(comp_to_dist_arrow),
            dist_group.animate.next_to(comp_to_dist_arrow.target, RIGHT),
            MaintainPositionRelativeTo(sample_rects[num], dist_group),
            MaintainPositionRelativeTo(q_marks, dist_group),
            VGroup(output, output_words).animate.shift(0.5 * RIGHT),
        ))
        self.play(Write(vector_title))
        self.wait()

        # Label the positions of the vector
        pre_indices = VGroup(qb[0] for qb in all_qubits)
        indices = pre_indices.copy()
        indices.scale(0.75)
        indices.set_color(GREY_C)
        for bits, entry in zip(indices, state_vector.get_entries()):
            bits.next_to(state_vector, LEFT, buff=0.2)
            bits.match_y(entry)

        self.play(
            VGroup(qc_label, vect_lines).animate.shift(0.75 * LEFT),
            LaggedStart(
                (TransformFromCopy(pre_bits, bits, path_arc=30 * DEG)
                for pre_bits, bits in zip(pre_indices, indices)),
                lag_ratio=0.25,
                run_time=6
            ),
        )
        self.wait()

        # Fundamental rule
        ne_sign = Tex(R"\ne", font_size=120)
        ne_sign.move_to(comp_to_dist_arrow)
        ne_sign.set_color(RED)

        rule = Tex(R"x \rightarrow |x|^2", font_size=42)
        rule.next_to(comp_to_dist_arrow, UP, buff=SMALL_BUFF)

        template_eq = Tex(R"(+0.50)^2 = 0.25", font_size=20)
        entry_template = template_eq.make_number_changeable("+0.50", include_sign=True)
        percent_template = template_eq.make_number_changeable("0.25")

        vector_entries = state_vector.get_entries()

        bar_values = VGroup()
        for bar, entry in zip(dist_rects, vector_entries):
            entry_template.set_value(entry.get_value())
            percent_template.set_value(entry.get_value()**2)
            template_eq.next_to(bar, RIGHT, SMALL_BUFF)
            bar_values.add(template_eq.copy())

        self.play(
            FadeOut(comp_to_dist_arrow),
            FadeIn(ne_sign),
        )
        self.wait()
        self.play(
            FadeIn(comp_to_dist_arrow),
            FadeOut(ne_sign),
        )
        self.play(
            ReplacementTransform(q_marks, rule, path_arc=90 * DEG, run_time=1.5),
        )
        self.wait()
        self.play(
            dist_rect.animate.stretch(1.5, 0, about_edge=LEFT).set_anim_args(time_span=(1, 2)),
            FadeOut(sample_rects[num]),
            LaggedStart(
                (TransformFromCopy(entry, value[1], path_arc=-30 * DEG)
                for entry, value in zip(vector_entries, bar_values)),
                lag_ratio=0.5,
            ),
            LaggedStart(
                (FadeIn(value[0])
                for value in bar_values),
                lag_ratio=0.5,
                time_span=(2, 6)
            ),
            LaggedStart(
                (FadeIn(value[2:])
                for value in bar_values),
                lag_ratio=0.5,
                time_span=(2, 6)
            ),
            frame.animate.reorient(0, 0, 0, (2.15, 0.04, 0.0), 7.64),
            run_time=6,
        )
        self.remove(vector_title, output_words, output)
        self.wait()

        # Process the vector
        alt_states = [normalize(np.random.uniform(-1, 1, 16)) for x in range(2)]
        label_line = Line(UP, DOWN).set_height(1.0).next_to(qc_label.get_right(), LEFT, SMALL_BUFF)
        entries = state_vector.get_entries()
        comp_lines = VGroup(
            Line(
                label_line.pfp(alpha),
                entry.get_center(),
            ).insert_n_curves(20).set_stroke(
                color=random_bright_color(hue_range=(0.3, 0.5)),
                width=(0, 3, 3, 3, 0),
            )
            for alpha, entry in zip(np.linspace(0, 1, len(entries)), entries)
        )
        comp_lines.shuffle()

        self.play(FlashAround(rule, time_width=1.5, run_time=2))
        self.play(FadeOut(bar_values))
        for new_state in [*alt_states, state]:
            comp_lines.shuffle()
            self.play(
                LaggedStartMap(VShowPassingFlash, comp_lines, time_width=2.0, lag_ratio=0.02),
                Transform(dist_rects, self.get_dist_bars(new_state**2, all_qubits), time_span=(0.75, 1.75)),
                *(
                    ChangeDecimalToValue(entry, value, time_span=(0.75, 1.75))
                    for entry, value in zip(entries, new_state)
                ),
                run_time=2
            )

        # Highlight a few examples
        highlight_rect = SurroundingRectangle(
            VGroup(indices[point5_index], bar_values[point5_index])
        )
        highlight_rect.set_stroke(YELLOW, 2, 0)
        groups = [vector_entries, all_qubits, dist_rects, bar_values]
        bar_values.set_opacity(0)

        for index in [point5_index, point1_index]:
            self.play(
                frame.animate.reorient(0, 0, 0, (3.36, 0.87, 0.0), 5.60),
                dist_rect.animate.set_stroke(opacity=0),
                highlight_rect.animate.set_stroke(opacity=1).match_y(all_qubits[index]),
                *(
                    group[slc].animate.set_opacity(0.25)
                    for group in groups
                    for slc in [slice(0, index), slice(index + 1, None)]
                ),
                *(
                    group[index].animate.set_opacity(1)
                    for group in groups
                ),
                run_time=2,
            )
            self.play(
                FlashAround(indices[index], buff=SMALL_BUFF, color=RED, time_width=1.5),
                WiggleOutThenIn(indices[index]),
                run_time=2
            )
            self.wait()
            self.play(TransformFromCopy(vector_entries[index], bar_values[index][1], run_time=2, path_arc=-45 * DEG))
            self.play(FlashAround(bar_values[index][-1], buff=SMALL_BUFF, color=RED, time_width=1.5))
            self.wait()

        self.play(
            frame.animate.reorient(0, 0, 0, (2.13, 1.33, 0.0), 10.48),
            FadeOut(highlight_rect, time_span=(0, 1)),
            FadeIn(vector_title),
            *(
                group.animate.set_opacity(1)
                for group in groups
            ),
            FadeOut(bar_values, lag_ratio=0.01),
            run_time=4
        )

        # Concentrate value
        if False:  # Only used for an insertion
            # Concentrate onto one value
            og_state = state
            frame.reorient(0, 0, 0, (0.94, 0.34, 0.0), 9.20)
            target_state = np.zeros(16)
            key = 5
            target_state[key] = 1
            for alpha in [0.1, 0.1, 0.2, 0.25, 0.25, 0.25, 0.25, 1.0]:
                new_state = normalize(interpolate(state, target_state, alpha))

                self.play(
                    Transform(dist_rects, self.get_dist_bars(new_state**2, all_qubits, width_ratio=4), time_span=(0.5, 1.5)),
                    LaggedStartMap(VShowPassingFlash, comp_lines, time_width=2.0, lag_ratio=0.01, run_time=2.0),
                    *(
                        ChangeDecimalToValue(entry, value, time_span=(0.5, 1.5))
                        for entry, value in zip(state_vector.elements, new_state)
                    ),
                )

                state = new_state

            # Comment on the value
            rect = SurroundingRectangle(all_qubits[key])
            self.play(ShowCreation(rect, run_time=2))

        # Show the squares of all the values
        sum_expr = Tex(
            R"x_{0}^2 + x_{1}^2 + x_{2}^2 + x_{3}^2 + \cdots + x_{14}^2 + x_{15}^2 = 1",
            font_size=60
        )
        sum_expr.next_to(vector_title, UP, LARGE_BUFF)
        sum_expr.match_x(frame)

        self.play(
            LaggedStart(
                (FadeTransform(vector_entries[n].copy(), sum_expr[fR"x_{{{n}}}^2"])
                for n in [0, 1, 2, 3, 14, 15]),
                lag_ratio=0.05,
                run_time=2
            ),
            FadeTransformPieces(vector_entries[4:14].copy(), sum_expr[R"\cdots"][0], time_span=(0.5, 2.0)),
            Write(sum_expr["+"], time_span=(0.5, 1.5)),
            Write(sum_expr["= 1"], time_span=(1, 2)),
        )
        self.wait()
        self.play(FadeOut(sum_expr))

        # Flip some signs
        top_eq = Tex(R"(+0.50)^2 = 0.25", font_size=60)
        top_eq.move_to(sum_expr)
        top_value = top_eq.make_number_changeable("+0.50", include_sign=True)

        entry = vector_entries[point5_index]
        entry_rect = SurroundingRectangle(entry, buff=0.1)
        entry_rect.set_stroke(YELLOW, 1)
        value_rect = SurroundingRectangle(top_value)
        value_rect.set_stroke(YELLOW, 2)

        lines = VGroup(
            Line(entry_rect.get_corner(UL), value_rect.get_corner(DL)),
            Line(entry_rect.get_corner(UR), value_rect.get_corner(DR)),
        )
        lines.set_stroke(YELLOW, 1)

        self.play(ShowCreation(entry_rect))
        self.play(
            TransformFromCopy(entry_rect, value_rect),
            TransformFromCopy(entry, top_value),
            ShowCreation(lines, lag_ratio=0),
            FadeOut(vector_title),
        )
        self.wait()
        self.play(
            entry.animate.set_value(-0.5),
            top_value.animate.set_value(-0.5),
        )
        self.wait()
        self.play(
            Write(top_eq[0]),
            Write(top_eq[2:]),
            FadeOut(value_rect)
        )
        self.wait()
        self.play(
            entry.animate.set_value(0.5),
            top_value.animate.set_value(0.5),
        )
        self.wait()
        self.play(
            Uncreate(lines, lag_ratio=0),
            ReplacementTransform(top_value, entry),
            FadeOut(top_eq[0]),
            FadeOut(top_eq[2:]),
            FadeOut(entry_rect),
            FadeIn(vector_title),
            frame.animate.reorient(0, 0, 0, (0.45, 0.46, 0.0), 8.70),
        )

        # Flip some more signs
        signs = VGroup(entry[0] for entry in vector_entries)
        vector_entries.save_state()
        sign_choice = VGroup(Tex("+").set_color(BLUE), Tex("-").set_color(RED))
        sign_choice.set_width(1.2 * signs[0].get_width())
        sign_choices = VGroup(
            sign_choice.copy().move_to(sign, RIGHT)
            for sign in signs
        )

        for n in range(3):
            self.play(LaggedStart(*(
                Transform(sign, random.choice(choice), path_arc=PI)
                for sign, choice in zip(signs, sign_choices)),
                lag_ratio=0.15,
                run_time=2
            ))
        self.play(
            Restore(vector_entries),
        )

        # Go down to two dimensions
        small_state = normalize([1, 2])
        small_state_vector = DecimalMatrix(small_state.reshape([2, 1]), v_buff=1.0)
        small_state_vector.set_height(2.0)
        small_state_vector.move_to(state_vector, RIGHT)

        bits = VGroup(Integer(0), Integer(0))
        bits.arrange(DOWN, MED_LARGE_BUFF)
        qubits = VGroup(
            VGroup(bit, Ket(bit))
            for bit in bits
        )
        qubits.scale(1.5)
        qubits.arrange_to_fit_height(small_state_vector.get_entries().get_height())
        qubits.next_to(comp_to_dist_arrow, RIGHT, MED_LARGE_BUFF)
        qubits.reverse_submobjects()
        qubits[1][0].set_value(1)

        small_dist_bars = self.get_dist_bars(small_state**2, qubits, width_ratio=2)

        small_vect_lines = self.get_connecting_lines(qc_label, small_state_vector, from_buff=-0.1, to_buff=0.1)

        self.remove(state_vector, all_qubits, dist_rects, vect_lines)
        self.play(LaggedStart(
            FadeOut(indices, scale=0.25),
            TransformFromCopy(vect_lines, small_vect_lines),
            TransformFromCopy(state_vector.get_brackets(), small_state_vector.get_brackets()),
            TransformFromCopy(state_vector.get_entries(), small_state_vector.get_entries()),
            vector_title.animate.next_to(small_state_vector, UP, MED_LARGE_BUFF),
            FadeTransformPieces(all_qubits.copy(), qubits),
            TransformFromCopy(dist_rects, small_dist_bars),
            lag_ratio=0.1,
            run_time=3
        ))
        self.add(small_state_vector)
        self.wait()

        self.play(
            FadeOut(VGroup(small_vect_lines, small_state_vector, qubits, small_dist_bars)),
            FadeIn(VGroup(vect_lines, indices, state_vector, all_qubits, dist_rects)),
            vector_title.animate.next_to(state_vector, UP, MED_LARGE_BUFF),
        )

        # Apply Grover's
        self.play(
            frame.animate.reorient(0, 0, 0, (2, 0.45, 0.0), 9),
            qc_label[1].animate.set_color(BLUE),
        )
        key = 12
        state0 = np.sqrt(1.0 / 16) * np.ones(16)
        new_states = [state0]
        for n in range(3):
            state = new_states[-1].copy()
            state[key] *= -1
            new_states.append(state)
            new_states.append(2 * np.dot(state0, state) * state0 - state)

        key_icon = get_key_icon()
        key_entry_rect = SurroundingRectangle(VGroup(indices[key], vector_entries[key]))
        key_entry_rect.stretch(1.25, 0, about_edge=RIGHT)
        key_entry_rect.set_stroke(YELLOW, 2)

        for n, state in enumerate(new_states):
            anims = [Transform(
                dist_rects, self.get_dist_bars(state**2, all_qubits, width_ratio=4.0),
                time_span=(1, 2)
            )]
            if n == 1:
                # Highlight the outcomes
                entry_rects = VGroup(SurroundingRectangle(e, buff=0.05) for e in vector_entries)
                qubit_rects = VGroup(
                    SurroundingRectangle(VGroup(*pair), buff=0.05)
                    for pair in zip(all_qubits, dist_rects)
                )
                VGroup(entry_rects, qubit_rects).set_stroke(YELLOW, 2)
                self.play(
                    LaggedStartMap(VFadeInThenOut, entry_rects, lag_ratio=0.1),
                    LaggedStartMap(VFadeInThenOut, qubit_rects, lag_ratio=0.1),
                    run_time=6
                )
                self.wait()

                # Show the key
                bits = indices[key]
                bits.save_state()
                self.play(bits.animate.scale(2).set_color(WHITE).move_to(8 * RIGHT))

                key_icon.set_height(1.5 * bits.get_height())
                key_icon.next_to(bits, LEFT, SMALL_BUFF)
                self.play(Write(key_icon))
                self.wait()

                self.play(
                    Restore(bits),
                    key_icon.animate.scale(0.5).next_to(bits.saved_state, LEFT, buff=SMALL_BUFF),
                )

            if n % 2 == 1:
                neg1 = Tex(R"\times -1")
                neg1.next_to(key_entry_rect, RIGHT)
                neg1.set_color(YELLOW)
                anims.append(VFadeInThenOut(neg1, run_time=2))
                anims.append(VFadeInThenOut(key_entry_rect, run_time=2))
                anims.append(ChangeDecimalToValue(vector_entries[key], state[key], time_span=(0.5, 1.5)))
            else:
                anims.append(
                    LaggedStartMap(VShowPassingFlash, comp_lines, time_width=2.0, lag_ratio=0.005, run_time=2)
                )
                anims.extend([
                    ChangeDecimalToValue(entry, value, time_span=(1, 2))
                    for entry, value in zip(vector_entries, state)
                ])
            self.play(*anims)
            self.wait()

        # Read out from memory
        glass = get_magnifying_glass()
        glass.next_to(qc_label, UP, MED_LARGE_BUFF)
        glass.scale(0.75)
        glass.to_edge(LEFT, buff=0).shift(frame.get_x() * RIGHT)

        self.play(FadeIn(glass))
        self.play(
            glass.animate.shift(qc_label.get_center() - glass[0].get_center()).set_anim_args(path_arc=-45 * DEG),
            rate_func=there_and_back_with_pause,
            run_time=6
        )
        self.wait()

        qubits = all_qubits[key].copy()
        qubits.move_to(qc_label)
        qubits.scale(1.25)
        black_rect = FullScreenRectangle().set_fill(BLACK, 1)
        black_rect.fix_in_frame()
        self.add(black_rect, qubits)
        self.wait()

    def get_labeled_box(self, wire, alpha, label="H", size=0.5):
        box = Square(size)
        box.set_stroke(WHITE, 1)
        box.set_fill(BLACK, 1)
        box.move_to(wire.pfp(alpha))

        vect = rotate_vector(UP, PI / 8)
        arrow = VGroup(
            Vector(size * vect, thickness=1).center(),
            Vector(-size * vect, thickness=1).center(),
        )
        arrow.move_to(box)

        label = Tex(label)
        label.set_height(0.5 * size)
        label.move_to(box)

        return VGroup(box, label)

    def get_cnot(self, wire1, wire2, alpha):
        oplus = Tex(R"\oplus")
        dot = Dot()
        oplus.move_to(wire1.pfp(alpha))
        dot.move_to(wire2.pfp(alpha))
        connector = Line(dot, oplus, buff=0)
        connector.set_stroke(WHITE, 1)
        return VGroup(oplus, connector, dot)

    def get_measurement(self, wire, alpha, size=0.5):
        box = Square(size)
        box.set_stroke(WHITE, 1)
        box.set_fill(BLACK, 1)
        box.move_to(wire.pfp(alpha))
        arc = Arc(PI / 4, PI / 2)
        arc.set_width(0.7 * box.get_width())
        arc.move_to(box)
        arc.set_stroke(WHITE, 1)
        lines = VGroup(Line(ORIGIN, 0.2 * vect) for vect in [UL, UR])
        lines.move_to(box)
        lines.set_stroke(WHITE, 1)
        lines[1].set_stroke(opacity=0)
        return VGroup(box, arc, lines)

    def get_random_qubits(self):
        bits = BitString(random.randint(0, 15))
        ket = Ket(bits)
        return VGroup(bits, ket)

    def get_connecting_lines(self, from_mob, to_mob, from_buff=0, to_buff=0, stroke_color=TEAL_A, stroke_width=2):
        l_ur = from_mob.get_corner(UR) + from_buff * UR
        l_dr = from_mob.get_corner(DR) + from_buff * DR
        v_ul = to_mob.get_corner(UL) + to_buff * UL
        v_dl = to_mob.get_corner(DL) + to_buff * DL

        lines = VGroup(
            CubicBezier(l_ur, l_ur + RIGHT, v_ul + LEFT, v_ul),
            CubicBezier(l_dr, l_dr + RIGHT, v_dl + LEFT, v_dl),
        )
        lines.set_stroke(TEAL_A, 2)
        return lines

    def get_dist_bars(
        self,
        dist,
        objs,
        height_ratio=0.8,
        width_ratio=8,
        fill_colors=(BLUE_D, GREEN),
        stroke_color=WHITE,
        stroke_width=1,
    ):
        normalized_dist = np.array(dist) / sum(dist)
        height = objs[0].get_height() * height_ratio
        rects = VGroup(
            Rectangle(width_ratio * p, height).next_to(obj)
            for p, obj in zip(normalized_dist, objs)
        )
        rects.set_fill(opacity=1)
        rects.set_submobject_colors_by_gradient(*fill_colors)
        rects.set_stroke(stroke_color, stroke_width)
        return rects



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


def get_magnifying_glass(height=3.0, color=GREY_D):
    glass = SVGMobject("magnifying_glass2")
    glass.set_fill(GREY_D)
    glass.set_shading(0.35, 0.15, 0.5)
    circle = VMobject().set_points(glass[0].get_subpaths()[1])
    circle.set_fill(GREEN_SCREEN, 1, border_width=3)
    circle.set_stroke(width=0)
    glass.add_to_back(circle)
    glass.set_height(height)
    return glass


def get_key_icon(height=0.5):
    key_icon = SVGMobject("key").rotate(135 * DEG)
    key_icon.set_fill(YELLOW)
    key_icon.set_height(height)
    return key_icon


class Superposition(Group):
    def __init__(
        self,
        pieces,
        offset_multiple=0.2,
        max_rot_vel=3,
        glow_color=TEAL,
        glow_stroke_range=(1, 22, 4),
        glow_stroke_opacity=0.05
    ):
        self.pieces = pieces
        self.center_points = Group(
            Point(piece.get_center())
            for piece in pieces
        )
        self.offset_multipler = ValueTracker(offset_multiple)

        for piece, point_mob in zip(pieces, self.center_points):
            piece.center_point = point_mob

            piece.offset_vect = rotate_vector(RIGHT, np.random.uniform(0, TAU))
            piece.offset_vect_rot_vel = np.random.uniform(-max_rot_vel, max_rot_vel)

        glow_strokes = np.arange(*glow_stroke_range)
        glows = pieces.replicate(len(glow_strokes))
        glows.set_fill(opacity=0)
        for glow, sw in zip(glows, glow_strokes):
            glow.set_stroke(glow_color, width=float(sw), opacity=glow_stroke_opacity)

        self.glows = glows

        super().__init__(glows, pieces, self.center_points, self.offset_multipler)
        self.add_updater(lambda m, dt: m.update_piece_positions(dt))

    def update_piece_positions(self, dt):
        offset_multiple = self.offset_multipler.get_value()

        for piece in self.pieces:
            piece.offset_vect = rotate_vector(piece.offset_vect, dt * piece.offset_vect_rot_vel)
            piece.offset_radius = offset_multiple
            piece.move_to(piece.center_point.get_center() + piece.offset_radius * piece.offset_vect)

        for glow in self.glows:
            for sm1, sm2 in zip(glow.family_members_with_points(), self.pieces.family_members_with_points()):
                sm1.match_points(sm2)

    def set_offset_multiple(self, value):
        self.offset_multipler.set_value(value)

    def set_glow_opacity(self, opacity=0.1):
        self.glows.set_stroke(opacity=opacity)



# ----- From _2025/grover/runtime.py -----

class ContrastTwoAlgorithmsFrame(DisectAQuantumComputer):
    def construct(self):
        # Set up screens
        background = FullScreenFadeRectangle()
        background.set_fill(GREY_E, 1)
        screens = Rectangle(6, 5).get_grid(1, 2, buff=LARGE_BUFF)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 2)
        screens.to_edge(DOWN, buff=LARGE_BUFF)

        self.add(background)
        self.add(screens)

        # Titles
        titles = VGroup(
            VGroup(get_classical_computer_symbol(), Tex(R"\mathcal{O}(N)")),
            VGroup(get_quantum_computer_symbol(), Tex(R"\mathcal{O}(\sqrt{N})")),
        )
        for title, screen in zip(titles, screens):
            title[0].set_height(1.5)
            title[1].set_height(0.75)
            title.arrange(RIGHT, buff=0.5)
            title.next_to(screen, UP, aligned_edge=LEFT)

        self.add(titles)

        # Preview quantum search
        boxes = Square(0.1).get_grid(25, 4, fill_rows_first=False, v_buff=0.05, h_buff=1.1)
        boxes.set_height(screens[1].get_height() - MED_LARGE_BUFF)
        boxes.move_to(screens[1], UL).shift(MED_SMALL_BUFF * DR)

        values = VGroup(
            Integer(n, font_size=12).replace(box, dim_to_match=1)
            for n, box in enumerate(boxes)
        )

        dist = np.ones(100)
        width_ratio = 5
        bars = self.get_dist_bars(dist, boxes, width_ratio=width_ratio)

        q_dots = DotCloud().to_grid(4, 25).rotate(-90 * DEG)
        q_dots.replace(titles[1][0], dim_to_match=1)
        q_dots.stretch(0.5, 1)
        lines = VGroup(
            Line(point, box.get_center())
            for point, box in zip(q_dots.get_points(), boxes)
        )
        for line in lines:
            line.insert_n_curves(20)
            color = random_bright_color(hue_range=(0.3, 0.4))
            line.set_stroke(color, [0, 2, 2, 0], opacity=0.5)

        self.add(values)
        self.add(bars)

        for n in range(1, 10):
            dist[42] += n
            width_ratio *= 0.9
            lines.shuffle
            self.play(
                LaggedStartMap(VShowPassingFlash, lines, time_width=1.5, lag_ratio=2e-3),
                Transform(bars, self.get_dist_bars(dist, boxes, width_ratio=width_ratio), time_span=(0.5, 1))
            )
