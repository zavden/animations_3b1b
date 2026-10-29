# ==============================================================================
# Scene:      GroverPreview
# Source:     videos/_2025/colliding_blocks_v2/grover.py (lines 4-92)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GroverPreview.py GroverPreview -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GroverPreview(InteractiveScene):
    def construct(self):
        # Setup blocks
        block_spacing = 1.0
        blocks = Rectangle(12, 1).get_grid(12, 1, v_buff=block_spacing)
        blocks.set_fill(GREY_D, 1)
        blocks.set_stroke(BLUE, 1)
        blocks.move_to(2.5 * UP, UP)

        for block, tex, color in zip(blocks, it.cycle(["U_k", "U_s"]), it.cycle([BLUE, GREEN])):
            label = Tex(tex)
            label.set_color(color)
            label.move_to(block)
            block.set_stroke(color, 1)
            block.add(label)

        self.add(blocks)

        # Wires
        d = 100
        wires = VGroup(
            *Line(UP, DOWN).set_height(1).replicate(3),
            Tex(R"\dots"),
            *Line(UP, DOWN).set_height(1).replicate(3),
            Tex(R"\dots"),
            *Line(UP, DOWN).set_height(1).replicate(3),
        )
        wires.arrange(RIGHT)
        wires.arrange_to_fit_width(11)
        wires.next_to(blocks, UP, buff=0)
        true_wires = VGroup(w for w in wires if isinstance(w, Line))
        syms = ["1", "2", "3", "k-1", "k", "k+1", "98", "99", "100"]
        kets = VGroup(Tex(Rf"|{sym}\rangle") for sym in syms)
        for ket, line in zip(kets, true_wires):
            ket.set_height(0.35)
            ket.next_to(line, UP)

        key_index = 4
        kets[key_index].set_color(YELLOW)

        for block in blocks:
            block.wires = wires.copy()
            for wire in block.wires:
                if isinstance(wire, Line):
                    wire.set_height(block_spacing)
            block.wires.next_to(block, DOWN, buff=0)
            block.add(block.wires)

        self.add(wires)
        self.add(kets)

        # Add numbers
        amplitudes = VGroup(
            DecimalNumber(0.1, font_size=24, include_sign=True, num_decimal_places=3).next_to(wire, LEFT, buff=0.1)
            for wire in true_wires
        )
        amplitudes[key_index].set_color(YELLOW)

        diag_axis = np.array([math.sqrt(0.99), 0.1, 0])
        state_point = Point(diag_axis)

        def get_new_amplitudes():
            result = amplitudes.copy()
            value = math.sqrt(state_point.get_x()**2 / (d - 1))
            for dec in result:
                dec.set_value(value)
            result[key_index].set_value(state_point.get_y())
            return result

        self.add(amplitudes, state_point)

        # Repeatedly cycle
        curr_amplitudes = amplitudes
        frame = self.frame
        frame.set_y(1)

        for block, axis in zip(blocks, it.cycle([RIGHT, diag_axis])):
            state_point.flip(axis=axis, about_point=ORIGIN)
            new_amplitudes = get_new_amplitudes()
            new_amplitudes.match_y(block.wires)

            self.play(
                FadeOutToPoint(curr_amplitudes.copy(), block[0].get_center(), lag_ratio=0.0025, time_span=(0, 2)),
                FadeInFromPoint(new_amplitudes, block[0].get_center(), lag_ratio=0.0025, time_span=(1, 3.0)),
                frame.animate.set_y(min(block.wires.get_y() + 1, 1)),
                run_time=3,
            )

            curr_amplitudes = new_amplitudes
