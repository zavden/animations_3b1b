# ==============================================================================
# Scene:      FullExampleWithNewEnd
# Source:     videos/_2020/hamming.py (lines 4250-4762)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FullExampleWithNewEnd.py FullExampleWithNewEnd -w -m --fps 15
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


def get_image_bits(image, bit_height=0.15, buff=MED_SMALL_BUFF):
    bit = Integer(0)
    small_buff = (buff / bit.get_height()) * bit_height
    bit.set_height(bit_height)
    bits = get_bit_grid(
        n_rows=int(image.get_height() / (bit.get_height() + small_buff)),
        n_cols=int(image.get_width() / (bit.get_width() + small_buff)),
        buff=buff
    )
    bits.replace(image)
    return bits


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


class FullExampleWithNewEnd(Scene):
    CONFIG = {
        "random_seed": 3,
    }

    def construct(self):
        # Pull bits out of an image
        image = ImageMobject("Tom_In_Bowtie")
        image.set_height(6)
        image.to_edge(LEFT, buff=LARGE_BUFF)

        bits = get_image_bits(image)
        bits.match_height(image)
        bits.generate_target()
        bits.target.arrange_in_grid(n_cols=11, h_buff=SMALL_BUFF, v_buff=MED_SMALL_BUFF)
        bits.target.next_to(image, RIGHT, LARGE_BUFF, UP)
        for bit, bt in zip(bits, bits.target):
            bit.save_state()
            bit.target = bt
            bit.fade(0.9)

        words = OldTexText("11-bit\\\\chunks")
        words.scale(1.5)
        words.to_edge(RIGHT)
        lines = VGroup()
        for bit in bits.target[10:200:11]:
            line = Line(RIGHT, LEFT)
            line.set_stroke(BLUE, 1)
            line.bit = bit
            line.word = words[0][0]
            line.add_updater(lambda m: m.put_start_and_end_on(
                m.word.get_left() + SMALL_BUFF * LEFT,
                m.bit.get_right() + SMALL_BUFF * RIGHT,
            ))
            lines.add(line)

        self.add(image)
        self.add(bits)
        self.save_state()
        self.play(
            LaggedStartMap(
                Succession, bits,
                lambda m: (Restore(m), MoveToTarget(m)),
                lag_ratio=3 / len(bits),
            ),
            Write(words, rate_func=squish_rate_func(smooth, 0.5, 0.7)),
            ShowCreation(lines, lag_ratio=0.1, rate_func=squish_rate_func(smooth, 0.5, 1)),
            run_time=8
        )

        for line, bit in zip(lines, bits[10::11]):
            line.bit = bit

        for bit in bits:
            if bit.get_center()[1] < -FRAME_HEIGHT / 2:
                bits.remove(bit)

        self.wait()

        # Show many 16 bit blocks
        bits.generate_target()
        bits.target.scale(1.5)
        bits.target.arrange_in_grid(n_cols=11, h_buff=SMALL_BUFF, v_buff=LARGE_BUFF)
        bits.target.move_to(bits, UR)

        box_groups = VGroup()
        box_arrows = VGroup()
        for bit in bits.target[0:77:11]:
            boxes = VGroup(*[Square() for x in range(16)])
            boxes.arrange_in_grid(4, 4, buff=0)
            boxes.set_height(0.8)
            boxes.next_to(bit, LEFT, buff=1.5)
            boxes.set_stroke(GREY_B, 2)
            arrow = Arrow(bit.get_left(), boxes.get_right())
            box_arrows.add(arrow)
            box_groups.add(boxes)

        self.play(
            FadeOut(image, 2 * LEFT),
            MoveToTarget(bits, run_time=2),
            LaggedStartMap(FadeIn, box_groups, run_time=4),
            LaggedStartMap(GrowArrow, box_arrows, run_time=4),
        )
        self.wait()

        # Isolate to one box
        first_bits = bits[:11]
        first_boxes = box_groups[0]

        first_bits.generate_target()
        first_bits.target.set_height(0.6)
        first_bits.target.to_edge(UP)
        first_bits.target.set_x(-3)
        first_boxes.generate_target()
        first_boxes.target.set_height(5)
        first_boxes.target.next_to(first_bits.target, DOWN, LARGE_BUFF)

        self.play(
            MoveToTarget(first_bits),
            MoveToTarget(first_boxes),
            LaggedStart(*map(FadeOut, [
                *bits[11:], box_arrows, box_groups[1:],
                *lines, words,
            ]), lag_ratio=0.01),
            run_time=2
        )

        bits = first_bits
        boxes = first_boxes

        # Try it yourself
        morty = Mortimer()
        morty.to_edge(DR)
        self.play(
            PiCreatureSays(morty, "Try it\\\\yourself", target_mode="hooray"),
            VFadeIn(morty)
        )
        self.play(Blink(morty))
        self.wait(2)
        self.play(LaggedStart(
            FadeOut(morty),
            FadeOut(morty.bubble),
            FadeOut(morty.bubble.content),
        ))

        # Fill block
        N = 4
        ecc_boxes = VGroup(*[boxes[2**n] for n in range(N)])
        message_boxes = VGroup(*[
            box for box in boxes[1:]
            if box not in ecc_boxes
        ])
        pos_labels = get_grid_position_labels(boxes, height=0.2)
        pos_labels.set_color(GREY_B)

        self.play(
            ecc_boxes.set_fill, GREEN, 0.7,
            boxes[0].set_fill, YELLOW, 0.5,
            FadeIn(pos_labels, lag_ratio=0.1)
        )
        self.wait()

        self.play(LaggedStart(*[
            ApplyMethod(bit.move_to, box)
            for bit, box in zip(bits, message_boxes)
        ], run_time=4, lag_ratio=0.3))
        self.wait()

        # Organize bits properly
        bit_template = bits[0].copy()
        if get_bit_mob_value(bit_template) == 1:
            toggle_bit(bit_template)

        new_bits = [None] * 16
        for i in [0, 1, 2, 4, 8]:
            new_bits[i] = bit_template.copy()
            new_bits[i].move_to(boxes[i])

        bits_iter = iter(bits)
        for i, new_bit in enumerate(new_bits):
            if new_bit is None:
                new_bits[i] = next(bits_iter)

        bits = VGroup(*new_bits)

        # Show parity groups
        boxes.save_state()
        self.add(boxes, pos_labels, bits)
        for bit in bits:
            for part in bit:
                if part.get_fill_opacity() > 0:
                    part.set_fill(opacity=1)
            bit.save_state()
        VGroup(*bits[:3], bits[4], bits[8]).set_opacity(0)

        for n in range(N):
            boxes.generate_target()
            boxes.target.set_fill(BLACK, 0)
            get_bit_n_subgroup(boxes.target, n).set_fill(BLUE, 0.8)
            for k in range(n):
                boxes.target[2**k].set_fill(GREEN, 0.5)
            one_rects = get_one_rects(get_bit_n_subgroup(bits, n))
            counter = get_ones_counter(boxes[10:12], one_rects, buff=1.5)
            counter.match_height(bits[0])

            self.play(MoveToTarget(boxes))
            self.add(counter)
            self.play(ShowIncreasingSubsets(one_rects))
            self.wait()
            self.play(Restore(bits[2**n]))
            if counter.get_value() % 2 == 1:
                rect_copy = one_rects[0].copy()
                rect_copy.move_to(bits[2**n])
                one_rects.add(rect_copy)
                bits[2**n][0].set_opacity(1)
                toggle_bit(bits[2**n])
                self.add(rect_copy)
                self.wait()
            self.play(
                LaggedStartMap(FadeOut, VGroup(*one_rects, counter), run_time=1),
            )
        self.play(Restore(boxes))

        # Final parity check
        one_rects = get_one_rects(bits)
        counter = get_ones_counter(boxes[10:12], one_rects, buff=1.5)
        counter.match_height(bits[0])

        self.add(counter)
        self.play(ShowIncreasingSubsets(one_rects))
        self.wait()
        self.play(Restore(bits[0]))
        self.play(LaggedStartMap(FadeOut, VGroup(*one_rects, counter)))
        self.wait()

        # Send as a message
        block_group = VGroup(boxes, pos_labels, bits)
        pis, names = get_sender_and_receiver()
        randy, morty = pis

        line = Line(randy.get_corner(UR), morty.get_corner(UL), buff=MED_SMALL_BUFF)
        line.add(
            Dot().move_to(line.get_start(), RIGHT),
            Dot().move_to(line.get_end(), LEFT),
        )
        line.set_stroke(GREY, 2)
        line_label = OldTexText("Noisy channel")
        line_label.next_to(line, DOWN, SMALL_BUFF)
        line_label.set_color(RED)

        self.play(
            VFadeIn(pis),
            FadeIn(names, DOWN),
            randy.change, "raise_right_hand",
            block_group.set_height, 1,
            block_group.move_to, randy.get_corner(UR), DOWN,
            block_group.shift, 0.1 * UP,
        )
        self.play(
            ShowCreation(line),
            Write(line_label)
        )
        self.play(Blink(randy))
        self.play(
            block_group.match_x, line,
            randy.change, "happy", morty.eyes,
        )

        # Possible changes
        black_box = SurroundingRectangle(block_group, buff=0)
        black_box.set_fill(GREY_D, 1)
        black_box.set_stroke(WHITE, 2)
        change_words = VGroup(
            OldTexText("Maybe flip 0 bits"),
            OldTexText("Maybe flip 1 bit"),
            OldTexText("Maybe flip 2 bits"),
        )
        colors = [WHITE, RED_B, RED]
        for word, color in zip(change_words, colors):
            word.next_to(black_box, UP)
            word.set_color(color)

        morty_arrow = Vector(DOWN)
        morty_arrow.next_to(morty, UP)

        self.play(
            GrowArrow(morty_arrow),
            morty.change, "pondering", morty_arrow
        )
        self.play(ShowCreationThenFadeAround(morty))
        self.play(Blink(morty))
        self.wait()
        self.play(
            morty_arrow.next_to, block_group, UP,
            FadeIn(black_box),
            morty.look_at, black_box,
        )
        self.play(Blink(randy))
        self.wait()
        self.play(Blink(randy))
        self.play(
            FadeIn(change_words[0], 0.25 * DOWN),
            FadeOut(morty_arrow, UP),
            morty.change, "confused", change_words[0],
        )
        for i in [1, 2]:
            self.play(
                FadeIn(change_words[i], 0.25 * DOWN),
                change_words[:i].shift, UP,
            )
        self.wait()
        self.play(Blink(morty))

        error_pos = 10
        toggle_bit(bits[error_pos])

        self.add(block_group, black_box)
        self.play(
            FadeOut(black_box),
            FadeOut(change_words),
        )
        self.play(
            block_group.set_x, line.get_end()[0],
            morty.change, "pondering", line.get_end() + UP,
        )
        self.play(
            Uncreate(line),
            FadeOut(line_label, DOWN),
            FadeOut(randy, DL),
            FadeOut(morty, DR),
            FadeOut(names, DOWN),
            block_group.set_height, 5,
            block_group.set_y, 0,
            block_group.to_edge, RIGHT,
        )
        self.wait()

        # Try it!
        try_it_words = OldTexText("Try it\\\\yourself!")
        try_it_words.scale(2)
        try_it_words.next_to(boxes, LEFT, buff=2)
        self.play(FadeIn(try_it_words, RIGHT))
        self.wait()
        self.play(FadeOut(try_it_words, LEFT))

        # Do parity checks
        working_grid = boxes.copy()
        working_grid.to_edge(LEFT)
        working_grid_words = OldTexText("Possibilities")
        working_grid_words.set_color(BLUE)
        working_grid_words.next_to(working_grid, UP)
        working_grid.set_fill(BLUE, 0.7)
        working_pos_labels = get_grid_position_labels(working_grid)

        counter = Integer(0)
        counter.set_height(0.7)
        counter.set_color(YELLOW)
        counter.next_to(boxes, LEFT, MED_LARGE_BUFF)
        counter.counted = VGroup()
        counter.add_updater(lambda m: m.set_value(len(m.counted)))
        for n in range(N):
            off_bits = get_bit_n_subgroup(bits, n, 0)
            on_bits = get_bit_n_subgroup(bits, n, 1)
            rects = get_one_rects(on_bits)
            counter.counted = rects

            self.play(FadeOut(off_bits))
            self.add(counter)
            self.play(ShowIncreasingSubsets(rects))

            to_fade = get_bit_n_subgroup(working_grid, n, 1 - (len(rects) % 2))
            if n == 0:
                to_fade.set_fill(BLACK, 0)
                self.play(
                    FadeIn(working_grid),
                    FadeIn(working_pos_labels),
                    FadeIn(working_grid_words),
                )
            else:
                self.play(to_fade.set_fill, BLACK, 0)
            self.wait()
            self.play(
                FadeOut(counter),
                FadeOut(rects),
                FadeIn(off_bits),
            )

        # Move working grid
        self.add(working_grid, block_group)
        self.play(
            ApplyMethod(working_grid.move_to, boxes, run_time=2),
            FadeOut(working_grid_words),
            FadeOut(working_pos_labels),
        )

        # Full parity check
        rects = get_one_rects(bits)
        counter.counted = rects
        self.add(counter)
        self.play(ShowIncreasingSubsets(rects))
        self.wait()
        self.play(FadeOut(rects), FadeOut(counter))

        # Correct error bit
        self.play(toggle_bit_anim(bits[error_pos]))
        self.play(FadeOut(working_grid))
        self.wait()

        # Show 11 message bits
        block_group.generate_target()
        block_group.target.center()
        block_group.target.to_edge(DOWN)
        VGroup(*[
            block_group.target[2][i]
            for i in [0, 1, 2, 4, 8]
        ]).set_color(GREY_C)
        self.play(MoveToTarget(block_group))

        message_bits = VGroup(*[
            bit for i, bit in enumerate(bits)
            if i not in [0, 1, 2, 4, 8]
        ])
        message_bits.generate_target()
        message_bits.target.arrange(RIGHT, buff=SMALL_BUFF)
        message_bits.target.to_edge(UP)
        for mb, mt in zip(message_bits, message_bits.target):
            mb.target = mt

        self.play(LaggedStartMap(
            MoveToTarget, message_bits,
            lag_ratio=0.3,
            run_time=4,
        ))
        self.wait()

    def old_parity_checks(self):
        questions = VGroup(*[boxes.copy() for x in range(4)])
        questions.set_height(1)
        questions.arrange(DOWN, buff=0.5)
        questions.set_height(6)
        questions.to_edge(LEFT, buff=1)

        counter = Integer(0, color=YELLOW)
        counter.match_height(bits[0])
        counter.next_to(boxes, LEFT, LARGE_BUFF)

        boxes.save_state()
        self.add(boxes, pos_labels, bits)
        results = VGroup()
        for n, question in enumerate(questions):
            question.set_fill(BLACK, 0)
            get_bit_n_subgroup(question, n).set_fill(BLUE, 0.7)

            one_rects = get_one_rects(get_bit_n_subgroup(bits, n))
            counter.set_value(len(one_rects))

            boxes.generate_target()
            boxes.target.match_style(question)

            self.play(MoveToTarget(boxes))
            self.play(FadeIn(one_rects))

            if counter.get_value() % 2 == 0:
                result = Integer(0, color=GREEN)
            else:
                result = Integer(1, color=RED)
            result.next_to(question, RIGHT)
            results.add(result)

            counter_mover = counter.copy()
            counter_mover.generate_target()
            counter_mover.target.replace(result, stretch=True)
            counter_mover.target.fade(1)
            result.save_state()
            result.replace(counter, stretch=True)
            result.fade(1)

            self.play(
                ReplacementTransform(boxes.copy().set_fill(opacity=0), question),
                MoveToTarget(counter_mover, remover=True),
                Restore(result),
                FadeOut(one_rects),
                FadeOut(counter),
            )
        self.wait()

        one_rects = get_one_rects(bits)
        counter.set_value(len(one_rects))
        words = OldTexText("Likely one error")
        words.next_to(counter, DOWN, LARGE_BUFF, aligned_edge=RIGHT)
        self.play(
            boxes.set_fill, BLACK, 0,
            FadeIn(counter),
            FadeIn(one_rects),
        )
        self.wait()
        self.play(FadeIn(words, 0.1 * UP))
        self.wait()
        self.play(
            FadeOut(VGroup(counter, words, one_rects), lag_ratio=0.2)
        )

        # Read result
        final_result = results.copy()
        final_result.arrange(LEFT, buff=SMALL_BUFF)

        equation = VGroup(
            final_result,
            OldTex("\\rightarrow"),
            Integer(10)
        )
        equation.arrange(RIGHT)
        equation.to_edge(UP)

        self.play(TransformFromCopy(results, final_result, run_time=3, lag_ratio=0.3))
        self.play(
            Write(equation[1]),
            FadeIn(equation[2], LEFT),
        )
        self.wait()
        boxes.generate_target()
        boxes.target[10].set_fill(BLUE, 0.7)
        self.play(MoveToTarget(boxes))
        self.play(toggle_bit_anim(bits[10]))
        self.wait()

        self.play(
            LaggedStartMap(
                FadeOut, VGroup(*equation, *questions, *results),
                lambda m: (m, DOWN),
            ),
            Restore(boxes),
        )
