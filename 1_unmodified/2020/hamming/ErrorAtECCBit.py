# ==============================================================================
# Scene:      ErrorAtECCBit
# Source:     videos/_2020/hamming.py (lines 3469-3502)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ErrorAtECCBit.py ErrorAtECCBit -w -m --fps 15
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


def get_grid_position_labels(boxes, height=0.25):
    labels = VGroup()
    for n, box in enumerate(boxes):
        label = Integer(n)
        label.set_height(height)
        label.move_to(box, DR)
        label.shift(SMALL_BUFF * UL)
        labels.add(label)
    return labels


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


def zap_anim(bit, bolt_height=0.75):
    bolt = SVGMobject("lightning_bolt")
    bolt[0].add_line_to(bolt[0].get_start())
    bolt.set_fill(RED_B, 1)
    bolt.set_stroke(width=0)
    bolt.set_height(bolt_height)

    bolt.move_to(bit.get_center(), DL)

    outline = bolt.deepcopy()
    outline.set_stroke(RED_D, 2)
    outline.set_fill(opacity=0)

    return AnimationGroup(
        Succession(
            GrowFromPoint(bolt, bolt.get_corner(UR), rate_func=rush_into),
            FadeOut(bolt, run_time=0.5),
        ),
        Succession(
            ShowCreation(outline),
            FadeOut(outline),
        ),
        run_time=1,
    )


class ErrorAtECCBit(Scene):
    def construct(self):
        bits = get_bit_grid(4, 4, height=6)
        toggle_bit(bits[1])
        toggle_bit(bits[4])
        boxes = get_bit_grid_boxes(bits)
        pos_labels = get_grid_position_labels(boxes)
        ecc_boxes = VGroup(*[boxes[2**n] for n in range(4)])
        ecc_boxes.set_fill(GREEN, 0.5)
        bangs = OldTexText("!!!")
        bangs.set_color(RED)
        bangs.next_to(boxes[2], UP, SMALL_BUFF)

        self.add(boxes, ecc_boxes, pos_labels, bits)
        self.wait()
        self.play(LaggedStartMap(Rotate, ecc_boxes, lambda m: (m, PI)))
        self.wait()
        self.play(
            zap_anim(bits[2]),
            toggle_bit_anim(bits[2], target_color=RED),
        )
        self.play(Write(bangs))
        self.wait()

        for bit in bits:
            bit.remove(bit[1 - get_bit_mob_value(bit)])
        for n in range(4):
            bits.generate_target()
            bits.target.set_opacity(1)
            get_bit_n_subgroup(bits.target, n, 0).set_opacity(0)
            self.play(MoveToTarget(bits))
            self.wait()
        self.play(bits.set_opacity, 1)
        self.wait()
