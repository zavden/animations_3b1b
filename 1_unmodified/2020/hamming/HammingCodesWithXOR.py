# ==============================================================================
# Scene:      HammingCodesWithXOR
# Source:     videos/_2020/hamming.py (lines 5498-5811)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl HammingCodesWithXOR.py HammingCodesWithXOR -w -m --fps 15
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


def int_to_bit_string(number, n_bits=None):
    result = "{:b}".format(number)
    if n_bits is not None:
        result = (n_bits - len(result)) * "0" + result
    return result


def get_ones(block):
    result = VGroup()
    for bit in block:
        if isinstance(bit, Integer):
            value = bit.get_value()
        else:
            value = get_bit_mob_value(bit)
        if value == 1:
            result.add(bit)
    return result


def get_one_rects(block, buff=SMALL_BUFF):
    rects = VGroup()
    for bit in get_ones(block):
        rect = SurroundingRectangle(bit, buff=buff)
        rect.set_stroke(YELLOW, 3)
        rect.set_fill(YELLOW, 0.2)
        rects.add(rect)
    return rects


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


def get_xor(height=0.35, color=BLUE_B, stroke_width=4):
    xor = VGroup(
        Line(UP, DOWN),
        Line(LEFT, RIGHT),
        Circle(),
    )
    xor.set_stroke(color, stroke_width)
    xor.set_height(height)
    return xor


class HammingCodesWithXOR(Scene):
    def construct(self):
        # Setup
        bits = get_bit_grid(4, 4, bits=string_to_bits(":)"))
        bits.to_edge(LEFT, buff=1.5)
        boxes = get_bit_grid_boxes(bits)
        block = VGroup(boxes, bits)
        block.set_height(6)
        for bit in bits:
            bit.set_height(0.7)

        bin_pos_labels = VGroup()
        dec_pos_labels = VGroup()
        for n, box, bit in zip(it.count(), boxes, bits):
            bin_label = VGroup(
                *[Integer(int(c)) for c in int_to_bit_string(n, n_bits=4)]
            )
            bin_label.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
            bin_label.set_color(GREY_B)
            bin_label.set_width(0.7 * box.get_width())
            bin_label.move_to(box, DOWN)
            bin_label.shift(SMALL_BUFF * UP)
            bin_pos_labels.add(bin_label)

            dec_label = Integer(n)
            dec_label.match_height(bin_label)
            dec_label.match_style(bin_label[0])
            dec_label.move_to(bin_label, DR)
            dec_pos_labels.add(dec_label)

            bit.generate_target()
            bit.target.scale(0.9)
            bit.target.move_to(box, UP)
            bit.target.shift(MED_SMALL_BUFF * DOWN)

        # Enumerate
        self.add(block)
        kw = {"lag_ratio": 0.3, "run_time": 2}
        self.play(LaggedStartMap(FadeIn, dec_pos_labels, **kw))
        self.wait()
        kw["lag_ratio"] = 0.1
        self.play(
            LaggedStartMap(FadeOut, dec_pos_labels, **kw),
            LaggedStartMap(FadeIn, bin_pos_labels, **kw),
            LaggedStartMap(MoveToTarget, bits, **kw),
        )
        self.wait()

        # Highlight ones
        summands = VGroup()
        for bit, box, label in zip(bits, boxes, bin_pos_labels):
            for mob in bit, box, label:
                mob.save_state()
                mob.generate_target()

            if get_bit_mob_value(bit) == 1:
                box.target.set_fill(BLUE, 0.7)
                summands.add(label.copy())
            else:
                bit.target.fade(0.5)
                label.target.fade(0.5)

        self.play(*[
            LaggedStartMap(MoveToTarget, mob, lag_ratio=0.02)
            for mob in [boxes, bits, bin_pos_labels]
        ])
        self.wait()

        # Arrange sum
        summands.generate_target()
        summands.target.arrange(DOWN, buff=SMALL_BUFF)
        summands.target.set_width(1.5)
        summands.target.set_color(WHITE)
        summands.target.to_edge(RIGHT, buff=1.5)
        summands.target.to_edge(UP)

        line = Line(LEFT, RIGHT)
        xor = get_xor()
        line.set_width(summands.target.get_width() + 0.75)
        line.next_to(summands.target, DOWN, aligned_edge=RIGHT, buff=SMALL_BUFF)
        xor.next_to(line, UP, aligned_edge=LEFT)

        self.play(
            MoveToTarget(summands, run_time=2),
            ShowCreation(line),
            ShowCreation(xor),
        )
        self.wait()

        # Perform xor
        result = VGroup()
        rect_columns = VGroup()
        for tup in zip(*summands):
            rects = get_one_rects(tup)
            result_bit = get_bit_grid(1, 1, bits=[len(rects) % 2])[0]
            result_bit.replace(tup[-1], dim_to_match=1)
            result_bit.shift(1.5 * result_bit.get_height() * DOWN)
            result_bit.set_color(YELLOW)

            result.add(result_bit)
            rect_columns.add(rects)

        pre_result = VGroup()
        for summand in summands:
            pr = result.copy()
            pr.save_state()
            pr.move_to(summand)
            pr.fade(1)
            pre_result.add(pr)

        self.play(LaggedStartMap(Restore, pre_result, lag_ratio=0.05, remover=True))
        self.add(result)
        self.wait()
        self.play(ShowCreationThenFadeOut(SurroundingRectangle(result, stroke_color=BLUE)))
        self.wait()

        for n, rects, result_bit in zip(it.count(), reversed(rect_columns), reversed(result)):
            faders = VGroup()
            for bit_vect in [*summands, result]:
                for k, bit in enumerate(reversed(bit_vect)):
                    if k != n:
                        bit.generate_target()
                        bit.target.fade(0.7)
                        faders.add(bit)
            for group in bits, bin_pos_labels:
                sg = get_bit_n_subgroup(group, n, 0)
                sg.generate_target()
                sg.target.fade(1)
                faders.add(sg)
            faders.save_state()

            self.play(LaggedStartMap(MoveToTarget, faders, lag_ratio=0, run_time=1))

            new_rects = VGroup()
            for bit, pos in zip(get_bit_n_subgroup(bits, n), get_bit_n_subgroup(bin_pos_labels, n)):
                if get_bit_mob_value(bit) == 1:
                    nr = SurroundingRectangle(pos[3 - n], buff=0.05)
                    nr.set_fill(YELLOW, 0.25)
                    new_rects.add(nr)

            self.play(
                ShowIncreasingSubsets(rects),
                ShowIncreasingSubsets(new_rects),
            )
            self.wait()
            self.play(
                faders.restore,
                FadeOut(rects),
                FadeOut(new_rects),
            )
        self.wait()

        # Sender manipulations (Doing more by hand than should here...sorry)
        parity_highlights = VGroup(*[boxes[2**n].copy() for n in range(4)])
        parity_highlights.set_stroke(GREEN, 8)
        parity_highlights.set_fill(BLACK, 0)
        self.play(ShowCreation(parity_highlights))

        words = OldTexText("Try to make\\\\this 0000")
        words.set_color(GREEN)
        words.next_to(boxes, RIGHT, MED_LARGE_BUFF)
        words.to_edge(DOWN, buff=1)
        arrow = Arrow(words.get_right(), result.get_left(), buff=0.1)
        arrow.get_lp = words.get_right
        arrow.get_rp = result.get_left
        arrow.add_updater(lambda m: m.put_start_and_end_on(
            m.get_lp() + SMALL_BUFF * RIGHT,
            m.get_rp() + SMALL_BUFF * LEFT,
        ))
        self.play(
            Write(words),
            DrawBorderThenFill(arrow),
        )
        self.wait()

        strike = Cross(summands[0])
        strike.set_stroke(RED, 8)
        self.play(ShowCreation(strike))
        self.add(summands[0], strike)
        bits[2].generate_target()
        toggle_bit(bits[2].target)
        bits[2].target.fade(0.5)
        self.play(
            boxes[2].set_fill, BLACK, 0,
            MoveToTarget(bits[2]),
            bin_pos_labels[2].fade, 0.5,
            toggle_bit_anim(result[2]),
            FadeOut(summands[0]),
            FadeOut(strike),
        )
        summands.remove(summands[0])
        self.wait()

        toggle_bit(bits[8].saved_state)
        self.play(
            boxes[8].set_fill, BLUE, 0.7,
            Restore(bits[8]),
            Restore(bin_pos_labels[8]),
        )
        new_term = bin_pos_labels[8].copy()
        new_term.generate_target()
        new_term.target.set_color(WHITE)
        new_term.target.replace(summands[2])
        self.play(
            MoveToTarget(new_term),
            summands[:3].move_to, summands[1], DOWN,
        )
        self.play(toggle_bit_anim(result[0]))
        self.wait()
        summands.set_submobjects([*summands[:3], new_term, *summands[3:]])
        self.play(FadeOut(words), FadeOut(arrow), FadeOut(parity_highlights))

        # Show 0 -> 1 error
        pos = 11
        self.play(
            Restore(bits[pos]),
            Restore(bin_pos_labels[pos]),
        )
        self.play(toggle_bit_anim(bits[pos], target_color=RED))
        self.wait()

        new_term = bin_pos_labels[pos].copy()
        new_term.generate_target()
        new_term.target.set_color(RED)
        new_term.target.replace(summands[5])
        bottom_group = VGroup(summands[5:], xor, line, result)
        bottom_group.save_state()
        self.play(
            MoveToTarget(new_term),
            bottom_group.move_to, summands[6], UR,
        )
        self.wait(0.25)
        nt_copy = new_term.copy()
        self.play(
            nt_copy.replace, result,
            nt_copy.fade, 1,
            *[
                toggle_bit_anim(b1, path_arc=0)
                for b1, b2 in zip(result, new_term)
                if b2.get_value() == 1
            ]
        )
        self.remove(nt_copy)
        self.wait()
        self.play(
            Restore(bottom_group),
            FadeOut(new_term),
            toggle_bit_anim(bits[pos], target_color=WHITE)
        )
        self.play(
            bits[pos].fade, 0.5,
            bin_pos_labels[pos].fade, 0.5,
        )

        # Show 1 -> 0 error
        pos = 6
        self.play(
            toggle_bit_anim(bits[pos], target_color=RED),
            zap_anim(bits[pos]),
        )
        self.wait()

        new_term = bin_pos_labels[pos].copy()
        new_term.generate_target()
        new_term.target.set_color(RED)
        new_term.target.replace(summands[3])
        bottom_group = VGroup(summands[3:], xor, line, result)
        bottom_group.save_state()
        self.play(
            MoveToTarget(new_term),
            bottom_group.move_to, summands[4], UR,
        )

        for bit in result:
            bit[0].set_opacity(1)
            bit[1].set_opacity(0)
        nt_copy = new_term.copy()
        self.play(
            nt_copy.move_to, result,
            nt_copy.fade, 1,
            *[
                toggle_bit_anim(b1, path_arc=0)
                for b1, b2 in zip(result, new_term)
                if b2.get_value() == 1
            ]
        )
        self.remove(nt_copy)
        self.wait()

        brace = Brace(VGroup(summands[2], new_term), LEFT, buff=SMALL_BUFF)
        brace_bits = summands[2].copy()
        for bb in brace_bits:
            bb.set_value(0)
        brace_bits.next_to(brace, LEFT)
        self.play(GrowFromCenter(brace))
        self.play(
            Transform(summands[2].copy(), brace_bits, remover=True),
            ReplacementTransform(new_term.copy(), brace_bits),
        )
        self.wait()

        arrow = Arrow(result.get_left(), bin_pos_labels[pos].get_corner(DR), path_arc=-30 * DEGREES, buff=0.1)
        self.play(DrawBorderThenFill(arrow))
        self.wait()

        self.play(toggle_bit_anim(bits[pos], target_color=WHITE))
        self.play(
            Restore(bottom_group),
            FadeOut(new_term),
            FadeOut(brace),
            FadeOut(brace_bits),
            FadeOut(arrow),
        )
        self.wait()
