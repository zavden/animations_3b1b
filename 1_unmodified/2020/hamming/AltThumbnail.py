# ==============================================================================
# Scene:      AltThumbnail
# Source:     videos/_2020/hamming.py (lines 342-416)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AltThumbnail.py AltThumbnail -w -m --fps 15
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


class AltThumbnail(Scene):
    def construct(self):
        background = self.get_background()
        self.add(background)

        bits = get_bit_grid(4, 4)
        bits.arrange_in_grid(h_buff=0.7, v_buff=0.5)
        boxes = get_bit_grid_boxes(bits)
        boxes.set_fill(BLACK, 1)

        boxes[0].set_fill(TEAL_E)
        parity_boxes = VGroup(*(boxes[2**n] for n in range(4)))
        parity_boxes.set_fill(BLUE_E, 1)
        group = VGroup(boxes, bits)
        group.to_edge(DOWN, buff=LARGE_BUFF)

        grouped_blocks = VGroup(*(boxes.copy() for x in range(4)))
        grouped_blocks.arrange_in_grid(buff_ratio=0.4)
        grouped_blocks.match_height(boxes)
        grouped_blocks.match_y(boxes)
        for n, gb in enumerate(grouped_blocks):
            gb.set_fill(BLACK)
            for k, box in enumerate(gb):
                if (k & (2**n)):
                    box.set_fill(BLUE_E)
        grouped_blocks.to_edge(RIGHT, LARGE_BUFF)

        all_blocks = VGroup(group, grouped_blocks)
        all_blocks.arrange(RIGHT, buff=1.0).to_edge(DOWN, LARGE_BUFF)
        all_blocks.set_height(6).center()

        self.add(group)
        self.add(grouped_blocks)
        return

        #
        title = Text("Hamming codes", font_size=72)
        title.to_edge(UP)
        shadow = VGroup()
        for w in np.linspace(50, 0, 50):
            tc = title.copy()
            tc.set_stroke(BLACK, width=w, opacity=0.02)
            tc.set_fill(opacity=0)
            shadow.add(tc)

        self.add(shadow)
        self.add(title)
        return


        #
        words = OldTexText("Parity bits", font_size=72)
        words.next_to(boxes, LEFT, LARGE_BUFF)
        words.to_edge(UP)

        words.move_to(boxes.get_corner(UL), DR)
        words.shift(0.5 * UL)

        lines = VGroup()
        for n, v in zip(range(4), [UP, UP, LEFT, LEFT]):
            lines.add(Line(words.get_corner(DR), boxes[2**n].get_corner(v), buff=0.0))

        lines.set_stroke(BLUE_B)

        self.add(words)
        self.add(lines)

    def get_background(self, n=25, k=100):
        choices = (Integer(0), Integer(1))
        background = VGroup(*(random.choice(choices).copy() for x in range(n * k)))
        background.arrange_in_grid(n, k)
        background.set_height(FRAME_HEIGHT)
        background.set_opacity(0.25)
        background.set_fill(border_width=0)
        return background
