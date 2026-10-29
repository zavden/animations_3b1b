# ==============================================================================
# Scene:      BurstErrors
# Source:     videos/_2020/hamming.py (lines 5051-5159)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl BurstErrors.py BurstErrors -w -m --fps 15
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


class BurstErrors(Scene):
    def construct(self):
        # Setup
        bl = 8
        nb = 4

        bits = get_bit_grid(1, bl * nb, bits=string_to_bits("3b1b"))
        bits.set_height(0.5)
        bits.arrange(RIGHT, buff=SMALL_BUFF)
        bits.move_to(DOWN)
        self.add(bits)

        colors = [BLUE, YELLOW, MAROON_B, TEAL]
        block_words = VGroup(*[
            OldTexText(f"Block {n}", fill_color=color)
            for n, color in zip(range(nb), colors)
        ])
        block_words.set_height(0.5)
        block_words.arrange(RIGHT, buff=LARGE_BUFF)
        block_words.move_to(2 * UP)
        self.add(block_words)

        # Add lines
        lines = VGroup()
        for n, bit in enumerate(bits):
            words = block_words[n // bl]
            line = Line()
            line.match_color(words)
            line.set_stroke(width=2)
            line.words = words
            line.bit = bit
            bit.line = line
            underline = Underline(bit)
            underline.set_stroke(words.get_color(), 4)
            bit.add(underline)
            line.add_updater(lambda m: m.put_start_and_end_on(
                m.words.get_bottom() + SMALL_BUFF * DOWN,
                m.bit.get_top(),
            ))
            lines.add(line)

        self.play(LaggedStartMap(ShowCreation, lines, suspend_mobject_updating=True))
        self.wait()

        # Show burst error
        error_bits = bits[9:13]
        error_words = OldTexText("Burst of errors")
        error_words.next_to(error_bits, DOWN)
        error_words.set_color(RED)
        ruined_words = OldTexText("Ruined")
        ruined_words.set_color(RED)
        ruined_words.next_to(block_words[1], UP)
        strike = Line(LEFT, RIGHT)
        strike.replace(block_words[1])
        strike.set_color(RED)

        self.play(
            LaggedStartMap(toggle_bit_anim, error_bits, target_color=RED),
            LaggedStart(*map(zap_anim, error_bits)),
            Write(error_words)
        )
        self.play(
            ShowCreation(strike),
            FadeIn(ruined_words, 0.5 * DOWN)
        )
        self.wait()
        self.play(
            FadeOut(ruined_words, 0.2 * UP),
            FadeOut(error_words, 0.2 * DOWN),
            FadeOut(strike),
            LaggedStartMap(toggle_bit_anim, error_bits, target_color=WHITE),
            run_time=1,
        )
        for bit in error_bits:
            bit[-1].set_color(YELLOW)

        # Rearrange
        new_order = VGroup()
        for i in range(bl):
            for j in range(nb):
                new_order.add(bits[bl * j + i])
        new_order.generate_target()
        new_order.target.arrange(RIGHT, buff=SMALL_BUFF)
        new_order.target.replace(bits)

        self.play(MoveToTarget(new_order, run_time=3, path_arc=30 * DEGREES))
        self.wait()

        # New burst
        error_bits = new_order[9:13]

        self.play(
            LaggedStartMap(toggle_bit_anim, error_bits, target_color=RED),
            LaggedStart(*map(zap_anim, error_bits)),
            Write(error_words),
        )
        non_error_lines = VGroup()
        for line in lines:
            if line.bit not in error_bits:
                non_error_lines.add(line)
        self.play(non_error_lines.set_stroke, {"width": 1, "opacity": 0.5})
        self.wait()

        error_words = VGroup(*[TexText("1 error", fill_color=GREEN) for x in range(4)])
        for ew, bw in zip(error_words, block_words):
            ew.next_to(bw, UP, MED_LARGE_BUFF)

        self.play(LaggedStartMap(FadeIn, error_words, lambda m: (m, DOWN)))
        self.wait()
