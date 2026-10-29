# ==============================================================================
# Scene:      BinaryCounting
# Source:     videos/_2020/hamming.py (lines 5162-5207)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BinaryCounting.py BinaryCounting -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


def int_to_bit_string(number, n_bits=None):
    result = "{:b}".format(number)
    if n_bits is not None:
        result = (n_bits - len(result)) * "0" + result
    return result


def get_grid_position_labels(boxes, height=0.25):
    labels = VGroup()
    for n, box in enumerate(boxes):
        label = Integer(n)
        label.set_height(height)
        label.move_to(box, DR)
        label.shift(SMALL_BUFF * UL)
        labels.add(label)
    return labels


def toggle_bit_anim(bit, target_color=None, **kwargs):
    original = bit.copy()
    original[1 - get_bit_mob_value(original)].rotate(PI)
    toggle_bit(bit)
    if target_color is not None:
        bit.set_color(target_color)

    if "path_arc" not in kwargs:
        kwargs["path_arc"] = PI

    return TransformFromCopy(original, bit, **kwargs)


class BinaryCounting(Scene):
    def construct(self):
        def get_bit_grids(bit_values):
            left_bits = get_bit_grid(4, 1, buff=LARGE_BUFF, bits=bit_values, height=6)
            left_bits.move_to(3 * LEFT)
            right_bits = get_bit_grid(1, 4, buff=SMALL_BUFF, bits=bit_values, height=0.6)
            right_bits.set_submobjects(list(reversed(right_bits)))
            right_bits.move_to(RIGHT + 2 * UP)
            return VGroup(left_bits, right_bits)

        bit_grids = get_bit_grids([0, 0, 0, 0])

        brace = Brace(bit_grids[1], UP)
        counter = Integer(0, edge_to_fix=ORIGIN)
        counter.match_height(bit_grids[1])
        counter.set_color(BLUE)
        counter.next_to(brace, UP)

        boxes = VGroup(*[Square() for x in range(16)])
        boxes.arrange_in_grid(4, 4, buff=0)
        boxes.set_height(4)
        boxes.next_to(bit_grids[1], DOWN, LARGE_BUFF)
        boxes.set_stroke(GREY_B, 2)
        pos_labels = get_grid_position_labels(boxes)

        self.add(bit_grids)
        self.add(brace)
        self.add(counter)
        self.add(boxes)
        self.add(pos_labels)

        for n in range(16):
            bit_values = list(map(int, int_to_bit_string(n, n_bits=4)))
            boxes.generate_target()
            boxes.target.set_fill(BLACK, 0)
            boxes.target[n].set_fill(BLUE, 0.8)
            anims = [
                ChangeDecimalToValue(counter, n),
                MoveToTarget(boxes)
            ]
            for grid in bit_grids:
                for bit, bv in zip(grid, reversed(bit_values)):
                    if get_bit_mob_value(bit) != bv:
                        anims.append(toggle_bit_anim(bit))
            self.play(*anims, run_time=0.5)
            self.wait()
