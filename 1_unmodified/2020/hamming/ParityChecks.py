# ==============================================================================
# Scene:      ParityChecks
# Source:     videos/_2020/hamming.py (lines 1963-2353)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl ParityChecks.py ParityChecks -w -m --fps 15
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


def get_sender_and_receiver(height=2):
    sender = Randolph(height=height)
    receiver = Mortimer(height=height)
    sender.name = OldTexText("Sender")
    receiver.name = OldTexText("Receiver")

    pis = VGroup(sender, receiver)
    names = VGroup(sender.name, receiver.name)

    sender.to_corner(DL)
    receiver.to_corner(DR)
    pis.shift(UP)
    for name, pi in zip(names, pis):
        name.next_to(pi, DOWN)

    return pis, names


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


def get_ones_counter(label, one_rects, buff=MED_LARGE_BUFF):
    counter = Integer()
    counter.match_color(one_rects[0])
    counter.match_height(label[1])
    counter.next_to(label[1], RIGHT, buff=buff, aligned_edge=DOWN)
    f_always(counter.set_value, lambda: len(one_rects))
    return counter


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


class ParityChecks(Scene):
    def construct(self):
        # Show detection
        block = get_bit_grid(4, 4, bits=string_to_bits(":)"))
        block.move_to(3 * LEFT)
        point = block.get_corner(DR) + 2 * RIGHT + UP
        scanim = scan_anim(point, block, final_stroke_width=0.5, run_time=2, lag_factor=2)
        lines, robot = scanim.mobject
        detection_words = OldTexText("Error detected!")
        detection_words.set_color(RED)
        detection_subwords = OldTexText("But I have no idea where!")
        detection_words.next_to(robot.get_top(), UR, SMALL_BUFF)
        detection_subwords.move_to(detection_words, DL)

        self.add(block)
        self.play(scanim)
        self.play(
            GrowFromPoint(detection_words, robot.get_top())
        )
        self.wait()
        self.play(
            detection_words.shift, 0.75 * UP,
            FadeIn(detection_subwords, 0.5 * DOWN),
        )
        self.wait()

        title = OldTexText("Parity Check")[0]
        title.set_color(YELLOW)
        title.set_stroke(BLACK, 3, background=True)
        title.add(Underline(title).shift(0.05 * UP))
        title.scale(1.5)
        title.to_edge(UP)

        self.play(Write(title))
        self.wait()
        self.play(
            LaggedStart(
                FadeOut(scanim.mobject),
                FadeOut(detection_words),
                FadeOut(detection_subwords),
            ),
            block.move_to, DOWN,
        )

        # Single bit vs. message
        pb_rect = SurroundingRectangle(block[0])
        pb_rect.set_stroke(GREEN, 3)
        ms_rect = SurroundingRectangle(block)
        ms_blob = Polygon(
            pb_rect.get_corner(UR) + 0.05 * RIGHT,
            ms_rect.get_corner(UR),
            ms_rect.get_corner(DR),
            ms_rect.get_corner(DL),
            pb_rect.get_corner(DL) + 0.05 * DOWN,
            pb_rect.get_corner(DR) + 0.05 * DR,
        )
        ms_blob.set_stroke(BLUE, 3)

        pb_words = OldTexText("Reserve one special bit")
        pb_words.next_to(pb_rect, LEFT)
        pb_words.match_color(pb_rect)
        ms_words = OldTexText("The rest carry\\\\a message", alignment="")
        ms_words.next_to(ms_blob, RIGHT, aligned_edge=UP)
        ms_words.align_to(pb_words, UP)
        ms_words.match_color(ms_blob)

        self.play(
            FadeIn(pb_words),
            ShowCreation(pb_rect),
        )
        self.wait()
        self.play(
            FadeIn(ms_words),
            ShowCreation(ms_blob),
        )

        # Wave of flips
        k = 3
        for n in range(1, len(block) + k):
            if n < len(block):
                toggle_bit(block[n])
            if 1 <= n - k < len(block):
                toggle_bit(block[n - k])
            self.wait(0.05)

        # Count 1's
        number_ones_label = OldTexText("\\# ", "of 1's: ")
        number_ones_label.set_height(0.7)
        number_ones_label.to_edge(UP)
        number_ones_label.shift(LEFT)

        one_rects = get_one_rects(block)
        one_counter = get_ones_counter(number_ones_label, one_rects)

        self.play(
            FadeIn(number_ones_label, DOWN),
            FadeOut(title, UP),
        )
        self.add(one_counter)
        self.play(ShowIncreasingSubsets(one_rects, run_time=1, rate_func=bezier([0, 0, 1, 1])))
        self.wait()

        # Show need to flip
        want_even_label = OldTexText("Want this\\\\to be even")
        want_even_label.next_to(one_counter, RIGHT, buff=1.5)
        want_even_arrow = Arrow(
            want_even_label.get_left(), one_counter.get_right()
        )
        want_even_label.shift_onto_screen()

        self.play(
            GrowArrow(want_even_arrow),
            FadeIn(want_even_label),
        )
        self.wait()
        self.play(
            LaggedStartMap(
                Indicate, one_rects,
                scale_factor=1.1,
                color=RED,
                lag_ratio=0.2,
                run_time=2,
            )
        )
        self.wait()

        pb = block[0]
        pb_center = pb.get_center()

        self.play(pb.next_to, pb_words, DOWN)
        self.play(toggle_bit_anim(pb))
        self.play(pb.move_to, pb_center)
        one_rects.become(get_one_rects(block))
        self.play(DrawBorderThenFill(one_rects[0]))

        # Show case with no need to flip
        self.play(
            FadeOut(block),
            FadeOut(one_rects),
            FadeOut(one_counter),
        )
        new_block = get_bit_grid(4, 4, bits=string_to_bits("<3"))
        new_block.replace(block)
        block = new_block
        self.play(ShowIncreasingSubsets(block))
        one_rects = get_one_rects(block)
        one_counter = get_ones_counter(number_ones_label, one_rects)
        self.add(one_counter)
        self.play(ShowIncreasingSubsets(one_rects))
        check = Checkmark()
        check.scale(2)
        check.next_to(pb, UP)
        self.play(Write(check, run_time=0.5))
        self.play(FadeOut(check))
        self.wait()

        # Sender and receiver
        self.play(LaggedStart(*map(FadeOut, [
            number_ones_label, one_counter,
            want_even_arrow, want_even_label,
            pb_words, pb_rect,
            ms_words, ms_blob,
            one_rects
        ])))

        pis, names = get_sender_and_receiver()
        sender, receiver = pis

        block.generate_target()
        block.target.scale(0.5)
        block.target.next_to(sender, UR)
        r_block = block.target.copy()
        r_block.next_to(receiver, UL)
        n_block = r_block.copy()
        n_block.move_to(VGroup(block.target, r_block))
        arrows = VGroup(
            Arrow(block.target.get_right(), n_block.get_left()),
            Arrow(n_block.get_right(), r_block.get_left()),
        )
        noise_word = OldTexText("Noise")
        noise_arrow = Vector(0.7 * DOWN)
        noise_arrow.next_to(n_block, UP)
        noise_word.next_to(noise_arrow, UP)
        noise_label = VGroup(noise_word, noise_arrow)
        noise_label.set_color(RED)
        flipper_index = 7

        self.play(
            ApplyMethod(sender.change, "raise_right_hand", block.target),
            VFadeIn(sender),
            FadeIn(names),
            FadeIn(receiver),
            MoveToTarget(block),
        )
        self.play(
            TransformFromCopy(block, n_block),
            GrowArrow(arrows[0]),
            FadeIn(noise_label),
        )
        self.play(
            toggle_bit_anim(n_block[flipper_index], target_color=RED),
            zap_anim(n_block[flipper_index]),
        )
        toggle_bit(r_block[flipper_index])
        self.play(
            TransformFromCopy(n_block, r_block),
            GrowArrow(arrows[1]),
            receiver.change, "pondering", r_block,
        )

        # Recount the 1's
        blocks = (block, r_block)
        one_rects_pair = VGroup(*[get_one_rects(b, buff=0.05) for b in blocks])
        label_pair = VGroup(*[
            OldTexText("\\#", " 1's:").next_to(b, UP, buff=MED_LARGE_BUFF)
            for b in blocks
        ])
        one_counter_pair = VGroup(*[
            get_ones_counter(label, rect, buff=MED_SMALL_BUFF)
            for label, rect in zip(label_pair, one_rects_pair)
        ])

        self.add(label_pair, one_counter_pair)
        self.play(*[
            ShowIncreasingSubsets(group)
            for group in one_rects_pair
        ])
        self.wait()

        bangs = OldTex("!!!")
        bangs.set_color(RED)
        bangs.next_to(receiver, UP)
        self.play(
            FadeIn(bangs, DOWN),
            receiver.change, "horrified", r_block,
        )
        self.play(Blink(receiver))
        self.wait()

        # Define parity and parity bit
        parity_rects = VGroup(
            SurroundingRectangle(VGroup(block, one_counter_pair[0]), buff=MED_SMALL_BUFF),
            SurroundingRectangle(VGroup(r_block, one_counter_pair[1]), buff=MED_SMALL_BUFF),
        )
        parity_rects[0].set_stroke(BLUE, 2)
        parity_rects[1].set_stroke(RED, 2)

        parity_labels = VGroup(*[
            OldTexText(
                "Parity: ", word,
                tex_to_color_map={word: color}
            ).next_to(rect, UP)
            for word, color, rect in zip(
                ["Even", "Odd"],
                [BLUE, RED],
                parity_rects,
            )
        ])

        for label, rect in zip(parity_labels, parity_rects):
            self.play(
                FadeIn(label, DOWN),
                ShowCreation(rect),
            )
        self.play(LaggedStart(*[
            ShowCreationThenFadeOut(Underline(label[0], color=YELLOW))
            for label in parity_labels
        ], lag_ratio=0.3))
        self.wait()
        self.play(Blink(sender))
        self.play(Blink(receiver))
        for bit, label, rect in zip([0, 1], parity_labels, parity_rects):
            bit_mob = get_bit_grid(1, 1, bits=[bit])[0]
            bit_mob.match_height(label[1])
            bit_mob.match_color(label[1])
            bit_mob.move_to(label[1], LEFT)
            x_shift = (rect.get_center() - VGroup(label[0], bit_mob).get_center()) * RIGHT
            bit_mob.shift(x_shift)
            self.play(
                label[1].replace, bit_mob, {"stretch": True},
                label[1].set_opacity, 0,
                FadeIn(bit_mob),
                label[0].shift, x_shift,
            )
            label.replace_submobject(1, bit_mob)

        pb_rect = SurroundingRectangle(block[0], buff=0.05)
        pb_rect.set_stroke(GREEN, 3)
        pb_label = OldTexText("Parity bit")
        pb_label.move_to(pb_rect)
        pb_label.to_edge(LEFT, buff=MED_SMALL_BUFF)
        pb_label.shift(UP)
        pb_label.match_color(pb_rect)
        pb_arrow = Arrow(
            pb_label.get_bottom() + SMALL_BUFF * DOWN,
            pb_rect.get_left(),
            buff=SMALL_BUFF,
            fill_color=GREEN
        )

        self.play(
            Write(pb_label, run_time=1),
            GrowArrow(pb_arrow),
            ShowCreation(pb_rect),
        )
        for color in [RED, BLUE]:
            self.play(
                toggle_bit_anim(block[0]),
                toggle_bit_anim(parity_labels[0][1], target_color=color),
                parity_rects[0].set_color, color,
            )
            self.wait()

        parity_descriptors = VGroup(
            parity_rects, parity_labels,
            pb_rect, pb_label, pb_arrow,
        )
        self.play(FadeOut(parity_descriptors, lag_ratio=0.1))

        # More than 1 error
        new_filpper_indices = [8, 13]
        n_flippers = VGroup(*[n_block[fi] for fi in new_filpper_indices])
        r_flippers = VGroup(*[r_block[fi] for fi in new_filpper_indices])
        for bit in r_flippers:
            toggle_bit(bit)
        new_one_rects_pair = VGroup(*[get_one_rects(b, buff=0.05) for b in blocks])
        new_one_counter_pair = VGroup(*[
            get_ones_counter(label, rect, buff=MED_SMALL_BUFF)
            for label, rect in zip(label_pair, new_one_rects_pair)
        ])
        for bit in r_flippers:
            toggle_bit(bit)

        self.play(
            LaggedStartMap(
                toggle_bit_anim, n_flippers,
                target_color=RED,
            ),
            LaggedStartMap(toggle_bit_anim, r_flippers),
            LaggedStart(*map(zap_anim, n_flippers)),
            receiver.change, "maybe",
            FadeOut(one_rects_pair[1]),
            FadeOut(one_counter_pair[1]),
        )
        self.remove(one_rects_pair, one_counter_pair)
        one_rects_pair = new_one_rects_pair
        one_counter_pair = new_one_counter_pair
        self.add(one_rects_pair, one_counter_pair)

        self.play(
            ShowIncreasingSubsets(one_rects_pair[1])
        )

        for x in range(2):
            self.play(Blink(receiver))
            self.play(Blink(sender))
            self.wait()

        # Even number of errors
        self.play(
            FadeOut(one_rects_pair[1]),
            FadeOut(one_counter_pair[1]),
            FadeOut(bangs),
            receiver.change, "pondering", r_block,
        )
        temp_rect = SurroundingRectangle(
            n_flippers[1],
            buff=0.05,
            color=GREEN,
        )
        temp_rect.flip()
        self.play(
            ShowCreationThenFadeOut(temp_rect),
            toggle_bit_anim(n_flippers[1], target_color=WHITE),
            toggle_bit_anim(r_flippers[1]),
        )
        self.wait()
        self.play(Blink(receiver))

        one_counter_pair.set_opacity(1)
        self.add(one_counter_pair)
        one_rects_pair[1].set_submobjects(
            get_one_rects(r_block, buff=0.05).submobjects
        )
        self.play(
            ShowIncreasingSubsets(one_rects_pair[1])
        )
        self.play(receiver.change, "hooray", r_block)
        self.wait()
        self.play(receiver.change, "erm")
        self.wait()
