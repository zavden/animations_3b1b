# ==============================================================================
# Scene:      MultiplePerspectives
# Source:     videos/_2020/hamming.py (lines 1399-1497)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultiplePerspectives.py MultiplePerspectives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def int_to_bit_string(number, n_bits=None):
    result = "{:b}".format(number)
    if n_bits is not None:
        result = (n_bits - len(result)) * "0" + result
    return result


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


def get_xor(height=0.35, color=BLUE_B, stroke_width=4):
    xor = VGroup(
        Line(UP, DOWN),
        Line(LEFT, RIGHT),
        Circle(),
    )
    xor.set_stroke(color, stroke_width)
    xor.set_height(height)
    return xor


class MultiplePerspectives(Scene):
    def construct(self):
        # Background
        background = VGroup(*[
            Rectangle().set_fill(color, 1)
            for color in [GREY_E, BLACK, GREY_E]
        ])
        background.set_stroke(width=0)
        background.arrange(RIGHT, buff=0)
        background.set_height(FRAME_HEIGHT)
        background.set_width(FRAME_WIDTH, stretch=True)
        self.add(background)

        # Names
        names = VGroup(
            OldTexText("Parity checks"),
            OldTexText("Xor of indices"),
            OldTexText("Matrix"),
        )

        names.set_height(0.6)
        for name, rect in zip(names, background):
            name.match_x(rect)
        names[0].shift(SMALL_BUFF * DOWN)
        names.to_edge(DOWN, buff=1)

        # Objects
        parity_groups = VGroup()
        for n in range(4):
            pg = VGroup(*[Square() for x in range(16)])
            pg.arrange_in_grid(4, 4, buff=0)
            pg.set_height(0.7)
            pg.set_stroke(GREY_A, 2)
            get_bit_n_subgroup(pg, n).set_fill(BLUE, 0.8)
            parity_groups.add(pg)
        parity_groups.arrange_in_grid(2, 2)

        code = ImageMobject("Hamming_Code_Snippet")

        ints = list(random.sample(list(range(16)), 4))
        ints.sort()
        xor_sum = reduce(op.xor, ints)
        bits = [int_to_bit_string(n, n_bits=4) for n in [*ints, xor_sum]]
        column = Group(*map(TexText, bits))
        column.arrange(DOWN, SMALL_BUFF)
        column[-1].set_color(YELLOW)
        column[-1].shift(MED_SMALL_BUFF * DOWN)
        line = Line(LEFT, RIGHT)
        line.set_stroke(GREY_B)
        line.set_width(column.get_width() + 0.75)
        line.move_to(column[-2:], RIGHT)
        xor = get_xor()
        xor.next_to(line, UP, SMALL_BUFF, LEFT)
        column.add(line, xor)
        code.set_width(2 * column.get_width())
        code.next_to(column, UP)
        column.add(code)

        matrix = IntegerMatrix(
            [
               [1, 1, 0, 1],
               [1, 0, 1, 1],
               [1, 0, 0, 0],
               [0, 1, 1, 1],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1],
            ],
            v_buff=0.6,
            h_buff=0.75,
        )

        objs = Group(parity_groups, column, matrix)

        for name, obj in zip(names, objs):
            obj.match_width(names[0])
            obj.next_to(name, UP, LARGE_BUFF)
        matrix.scale(0.7, about_edge=DOWN)

        # Introduce
        anims = []
        for name, obj in zip(names, objs):
            anims.append(AnimationGroup(
                FadeIn(name, 0.25 * UP),
                FadeIn(obj, lag_ratio=0, run_time=2),
            ))
        self.play(LaggedStart(*anims, lag_ratio=0.4))
        self.wait()
        for name, obj in zip(names, objs):
            obj.add(name)
        self.add(background[0])
        self.play(
            FadeOut(background),
            objs[0].set_x, 0,
            FadeOut(objs[1], 5 * RIGHT),
            FadeOut(objs[2], 2 * RIGHT),
            run_time=2
        )
        self.wait()
