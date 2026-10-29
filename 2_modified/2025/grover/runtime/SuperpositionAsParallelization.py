# ==============================================================================
# Scene:      SuperpositionAsParallelization
# Source:     videos/_2025/grover/runtime.py (lines 546-660)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/grover/qc_supplements.py
#
# Run from this folder:
#     manimgl SuperpositionAsParallelization.py SuperpositionAsParallelization -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/computer_chip.svg  (substitute: copy of the repo's gpu.svg, a chip with pins)
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

class SuperpositionAsParallelization(InteractiveScene):
    def construct(self):
        # Set up
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

        # Bit string
        boxes = Square().get_grid(1, 4, buff=0)
        boxes.set_height(0.5)
        boxes.match_x(classical)
        boxes.set_stroke(WHITE, 2)

        bit_mobs = VGroup(Integer(0).move_to(box) for box in boxes)

        def match_value(bit_mobs, value):
            bit_str = bin(int(value))[2:].zfill(4)
            for bit, mob in zip(bit_str, bit_mobs):
                mob.set_value(int(bit))
            return bit_mobs

        self.play(
            Write(boxes),
            Write(bit_mobs)
        )
        value_tracker = ValueTracker(0)
        self.play(
            value_tracker.animate.set_value(12),
            UpdateFromFunc(bit_mobs, lambda m: match_value(m, value_tracker.get_value())),
            run_time=3,
            rate_func=linear
        )
        self.wait()

        # Superposition
        bit_strings = VGroup()
        for bits in it.product(* 4 * [[0, 1]]):
            bit_string = VGroup(Integer(b) for b in bits)
            bit_string.arrange(RIGHT, buff=SMALL_BUFF)
            bit_strings.add(bit_string)
        bit_strings.arrange(DOWN)
        bit_strings.set_height(5.5)
        bit_strings.next_to(quantum, DOWN, MED_LARGE_BUFF)
        bit_strings.set_fill(opacity=0.75)

        superposition = Superposition(bit_strings)
        superposition.set_offset_multiple(0)
        superposition.set_glow_opacity(0)
        superposition.update()

        superposition_name = TexText(R"``Superposition''")
        superposition_name.set_color(TEAL)
        superposition_name.next_to(superposition, RIGHT, aligned_edge=UP).shift(LEFT)

        self.play(
            LaggedStart(
                (TransformFromCopy(bit_mobs, bit_string)
                for bit_string in bit_strings),
                lag_ratio=0.05,
            )
        )
        self.play(
            superposition.animate.set_offset_multiple(0.1).set_glow_opacity(0.05).shift(1.5 * LEFT),
            Write(superposition_name, run_time=1)
        )
        self.wait(15)

        # Show parallelization lines
        mini_classical = VGroup(
            classical.copy().set_height(0.25).move_to(point).match_x(quantum)
            for point in superposition.center_points
        )
        lines = VGroup(
            VGroup(
                Line(mc.get_left() + 1.1 * LEFT, mc.get_left(), buff=0.1),
                Line(mc.get_right(), mc.get_right() + 1.1 * RIGHT, buff=0.1),
            )
            for mc in mini_classical
        )
        lines.set_stroke(GREY, 2)

        outputs = VGroup(
            Integer(int(n == 12), font_size=24).next_to(line, RIGHT)
            for n, line in enumerate(lines)
        )

        self.play(
            superposition.animate.set_offset_multiple(0.025),
            FadeOut(superposition_name),
            LaggedStart(
                (TransformFromCopy(classical, mc)
                for mc in mini_classical),
                lag_ratio=0.05,
            ),
            LaggedStartMap(ShowCreation, lines),
        )
        self.wait()
        self.play(LaggedStart(
            (TransformFromCopy(piece, output)
            for piece, output in zip(superposition.pieces, outputs)),
            lag_ratio=0.01,
            run_time=3
        ))
        self.wait(15)
