# ==============================================================================
# Scene:      BlockSize256
# Source:     videos/_2020/hamming.py (lines 3532-3701)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl BlockSize256.py BlockSize256 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2020/chess.py -----

def string_to_bools(message):
    # For easter eggs on the board
    as_int = int.from_bytes(message.encode(), 'big')
    bits = "{0:b}".format(as_int)
    bits = (len(message) * 8 - len(bits)) * '0' + bits
    return [bool(int(b)) for b in bits]



# ----- From _2020/hamming.py -----

def get_bit_grid(n_rows, n_cols, bits=None, buff=MED_SMALL_BUFF, height=4):
    bit_pair = VGroup(Integer(0), Integer(1))
    bit_mobs = VGroup(*[
        bit_pair.copy()
        for x in range(n_rows * n_cols)
    ])
    bit_mobs.arrange_in_grid(n_rows, n_cols, buff=buff)
    bit_mobs.set_height(height)
    if bits is None:
        bits = np.random.randint(0, 2, len(bit_mobs))

    for bit_mob, bit in zip(bit_mobs, bits):
        bit_mob[1 - bit].set_opacity(0)

    bit_mobs.n_rows = n_rows
    bit_mobs.n_cols = n_cols
    return bit_mobs


def get_bit_mob_value(bit_mob):
    return int(bit_mob[1].get_fill_opacity() > bit_mob[0].get_fill_opacity())


def toggle_bit(bit):
    for sm in bit:
        sm.set_fill(opacity=1 - sm.get_fill_opacity())
    return bit


def string_to_bits(message):
    return [int(b) for b in string_to_bools(message)]


def get_bit_grid_boxes(bit_grid, color=GREY_B, stroke_width=2):
    width = get_norm(bit_grid[1].get_center() - bit_grid[0].get_center())
    height = get_norm(bit_grid[bit_grid.n_cols].get_center() - bit_grid[0].get_center())
    return VGroup(*[
        Rectangle(
            height=height,
            width=width,
            stroke_color=color,
            stroke_width=stroke_width,
        ).move_to(bit)
        for bit in bit_grid
    ])


def get_bit_n_sublist(input_list, n, bit_value=1):
    return [
        elem
        for i, elem in enumerate(input_list)
        if bool(i & (1 << n)) ^ bool(1 - bit_value)
    ]


def get_bit_n_subgroup(mob, n, bit_value=1):
    """
    If we enumerate mob, this returns a subgroup of all elements
    whose index has a binary representation with the n'th bit
    equal to bit_value
    """
    return VGroup(*get_bit_n_sublist(mob, n, bit_value))


def toggle_bit_anim(bit, target_color=None, **kwargs):
    original = bit.copy()
    original[1 - get_bit_mob_value(original)].rotate(PI)
    toggle_bit(bit)
    if target_color is not None:
        bit.set_color(target_color)

    if "path_arc" not in kwargs:
        kwargs["path_arc"] = PI

    return TransformFromCopy(original, bit, **kwargs)


class BlockSize256(Scene):
    def construct(self):
        N = 8
        frame = self.camera.frame

        # Bit block
        bits = string_to_bits("You decoded an easter egg. Nice!")
        block = get_bit_grid(2**(N // 2), 2**(N // 2), bits=bits)
        block.set_height(6)
        block.to_edge(LEFT, buff=LARGE_BUFF)
        boxes = get_bit_grid_boxes(block)

        parity_boxes = VGroup(*[boxes[2**k] for k in range(N)])
        parity_boxes.set_fill(GREEN, 0.8)

        bit_boxes = VGroup(*[VGroup(box, bit) for bit, box in zip(block, boxes)])
        to_fade = VGroup()
        to_keep = VGroup()
        for i, bb in enumerate(bit_boxes):
            if i >= 64 or (i % 16) >= 4:
                to_fade.add(bb.copy())
            else:
                to_keep.add(bb.copy())

        to_fade.save_state()
        to_fade.fade(1)
        frame.save_state()
        frame.replace(to_keep, dim_to_match=1)
        frame.scale(1.2)

        self.add(to_keep)
        self.play(
            Restore(frame),
            Restore(to_fade, lag_ratio=0.1),
            run_time=5,
        )

        self.clear()
        self.add(boxes)
        self.add(block)

        # Add title
        title = OldTexText("$256 = 2^8$ bits")
        title.set_height(0.7)
        title.next_to(boxes, UP, MED_LARGE_BUFF)
        title.set_x(0)

        self.play(
            frame.move_to, 0.5 * UP,
            Write(title)
        )
        self.wait()

        # Parity groups
        parity_groups = VGroup()
        for k in range(N):
            group = boxes.copy()
            group.set_fill(BLACK, opacity=0)
            group.set_stroke(GREY_B, 1)
            group.set_height(1.5)
            get_bit_n_subgroup(group, k).set_fill(BLUE_E, 1)
            parity_groups.add(group)

        parity_groups.arrange_in_grid(2, 4, buff=MED_LARGE_BUFF)
        parity_groups.set_width(7)
        VGroup(parity_groups[:4], parity_groups[4:]).arrange(DOWN, buff=1.5)
        parity_groups.to_edge(RIGHT)

        # Question labels
        q_labels = VGroup(*[TexText(f"Q{i + 1}") for i in range(N)])
        for label, group in zip(q_labels, parity_groups):
            label.set_height(0.3)
            label.next_to(group, UP, SMALL_BUFF)

        # Add questions
        self.play(
            LaggedStartMap(FadeIn, q_labels, lambda m: (m, DOWN), lag_ratio=0.3, run_time=5),
            LaggedStartMap(FadeIn, parity_groups, lambda m: (m, DOWN), lag_ratio=0.3, run_time=5),
        )
        self.wait()

        # Isolate one square
        pos = 69  # Why not?
        bits = "{0:b}".format(pos)
        bits = (N - len(bits)) * '0' + bits
        bits = bits[::-1]

        yes_no_group = VGroup()
        boxes.save_state()
        possible_positions = list(range(2**N))
        for k, bit, group in zip(it.count(), bits, parity_groups):
            bit_value = int(bit)
            if bit_value:
                word = OldTexText("Yes", color=GREEN)
            else:
                word = OldTexText("No", color=RED)
            word.next_to(group, DOWN)
            yes_no_group.add(word)

            intersect_positions = get_bit_n_sublist(range(2**N), k, bit_value)
            globals()['intersect_positions'] = intersect_positions
            possible_positions = list(filter(
                lambda i: i in intersect_positions,
                possible_positions,
            ))

            boxes.generate_target()
            boxes.target.match_style(boxes.saved_state)
            globals()['possible_positions'] = possible_positions
            globals()['boxes'] = boxes
            VGroup(*[boxes.target[i] for i in possible_positions]).set_fill(BLUE, 1)

            self.play(
                FadeIn(word),
                MoveToTarget(boxes)
            )
            self.wait()

        # Highlight parity bits
        parity_bits_label = OldTexText("8 parity bits")
        parity_bits_label.next_to(boxes, UP, aligned_edge=LEFT)
        parity_bits_label.set_color(GREEN)

        self.play(
            FadeIn(parity_bits_label, DOWN),
            title.to_edge, RIGHT
        )
        self.add(parity_boxes, block)
        self.play(
            LaggedStartMap(Rotate, parity_boxes, lambda m: (m, TAU)),
        )
        self.add(boxes, block)

        # Un-highlight isolated point
        self.play(
            boxes[pos].set_fill, BLACK, 0,
            FadeOut(yes_no_group)
        )

        # Message bits
        message_bits = VGroup(*[
            bit
            for i, bit in enumerate(block)
            if i not in [2**k for k in range(N)]
        ])
        message_bits.shuffle()

        self.play(
            LaggedStart(*[
                toggle_bit_anim(bit)
                for bit in message_bits
            ], lag_ratio=0.01, run_time=3)
        )
        self.wait()

        # Write redundant
        redundant_label = OldTexText("``Redundant''")
        redundant_label.set_color(GREEN)
        redundant_label.next_to(parity_bits_label[-1][-1], RIGHT, MED_LARGE_BUFF, DOWN)

        self.play(Write(redundant_label))

        block.save_state()
        for k in range(N):
            block.target = block.saved_state.copy()
            get_bit_n_subgroup(block.target, k, 0).set_fill(opacity=0)
            self.play(MoveToTarget(block))
            self.wait(0.5)
        self.play(Restore(block))
        self.wait()
