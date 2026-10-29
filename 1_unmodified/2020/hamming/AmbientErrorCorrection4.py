# ==============================================================================
# Scene:      AmbientErrorCorrection4
# Source:     videos/_2020/hamming.py (lines 1292-1296)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl AmbientErrorCorrection4.py AmbientErrorCorrection4 -w -m --fps 15
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


def bit_grid_to_bits(bit_grid):
    return list(map(get_bit_mob_value, bit_grid))


def toggle_bit(bit):
    for sm in bit:
        sm.set_fill(opacity=1 - sm.get_fill_opacity())
    return bit


def hamming_syndrome(bits):
    return reduce(
        lambda i1, i2: i1 ^ i2,
        [i for i, b in enumerate(bits) if b],
        0,
    )


def string_to_bits(message):
    return [int(b) for b in string_to_bools(message)]


def toggle_bit_anim(bit, target_color=None, **kwargs):
    original = bit.copy()
    original[1 - get_bit_mob_value(original)].rotate(PI)
    toggle_bit(bit)
    if target_color is not None:
        bit.set_color(target_color)

    if "path_arc" not in kwargs:
        kwargs["path_arc"] = PI

    return TransformFromCopy(original, bit, **kwargs)


def scan_anim(point, bits, final_stroke_width=0, run_time=3, lag_factor=3, show_robot=True, robot_height=0.5):
    lines = VGroup(*[
        Line(
            point, bit.get_center(),
            stroke_color=[GREEN, BLUE][get_bit_mob_value(bit)],
            stroke_width=1,
        )
        for bit in bits
    ])
    anims = [
        LaggedStartMap(
            lambda m, **kw: Succession(
                ShowCreation(m),
                ApplyMethod(m.set_stroke, None, final_stroke_width),
                **kw
            ),
            lines,
            lag_ratio=lag_factor / len(bits),
            run_time=run_time,
            remover=bool(final_stroke_width)
        )
    ]

    if show_robot:
        robot = SVGMobject("robot")
        robot.set_stroke(width=0)
        robot.set_color(GREY)
        robot.set_gloss(1)
        robot.set_height(robot_height)
        robot.move_to(point, UP)
        anims.append(FadeIn(robot))

    return AnimationGroup(*anims)


def focus_scan_anim_lines(scanim, point, final_stroke_width=1):
    lines = scanim.mobject[0]
    for line in lines:
        line.generate_target()
        line.target.put_start_and_end_on(line.get_start(), point)
        line.target.set_stroke(width=final_stroke_width)

    return AnimationGroup(*[
        MoveToTarget(line)
        for line in lines
    ])


class AmbientErrorCorrection(Scene):
    CONFIG = {
        "N": 8,
        "bit_grid_height": 7,
    }

    def construct(self):
        N = self.N
        size = (2**(N // 2), 2**(N // 2))
        bits = get_bit_grid(
            *size,
            bits=string_to_bits("Claude Shannon was a total boss!"),
            height=self.bit_grid_height,
        )
        bits.move_to(2 * RIGHT)
        point = 2.5 * LEFT + 2.5 * DOWN
        last_block = VMobject()

        for x in range(10):
            block = get_bit_grid(*size, height=self.bit_grid_height)
            block.move_to(2 * RIGHT)
            syndrome = hamming_syndrome(bit_grid_to_bits(block))

            if random.random() < 0.5:
                syndrome = 0
                toggle_bit(block[syndrome])

            scanim = scan_anim(
                point, bits,
                final_stroke_width=0.2, run_time=3, lag_factor=1,
                show_robot=(x == 0),
            )
            self.play(
                FadeIn(block, 6 * RIGHT),
                FadeOut(last_block, 6 * LEFT),
                run_time=2
            )
            self.play(scanim, run_time=1)
            if syndrome:
                flipper = block[syndrome]
                bangs = OldTex("!!!")
                bangs.scale(2)
                bangs.next_to(point, UL)
                bangs.set_color(RED)
                self.play(
                    Write(bangs, run_time=0.5),
                    focus_scan_anim_lines(scanim, flipper.get_center()),
                    flipper.set_color, RED,
                )
                self.play(
                    toggle_bit_anim(flipper, target_color=WHITE),
                    ApplyMethod(scanim.mobject[0].set_stroke, None, 0, 0, remover=True),
                    FadeOut(bangs),
                )
            else:
                check = Checkmark()
                check.scale(2)
                check.next_to(point, UL)
                self.play(FadeIn(check, 0.5 * DOWN))
                self.play(FadeOut(check), FadeOut(scanim.mobject[0]))
            last_block = block


class AmbientErrorCorrection4(AmbientErrorCorrection):
    CONFIG = {
        "N": 4,
        "bit_grid_height": 5,
    }
