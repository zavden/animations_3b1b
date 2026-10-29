# ==============================================================================
# Scene:      SetupSixteenBitExample
# Source:     videos/_2020/hamming.py (lines 1500-1788)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl SetupSixteenBitExample.py SetupSixteenBitExample -w -m --fps 15
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


class SetupSixteenBitExample(Scene):
    def construct(self):
        # Title
        title = OldTexText("Reinventing Hamming Codes")
        title.scale(1.5)
        title.to_edge(UP)
        title.set_color(BLUE)
        self.play(Write(title))

        # Simple but not too simple
        block = get_bit_grid(4, 4, bits=string_to_bits(":)"))
        block.move_to(0.5 * DOWN)
        top_row = block[:4]
        top_row.save_state()
        top_row.center()

        simple_words = OldTexText("Simple\\\\", "but not too\\\\simple")
        simple_words.scale(1.5)
        simple_words.next_to(block[4:12], LEFT, buff=LARGE_BUFF)
        top_simp = simple_words[0]
        top_simp.save_state()
        top_simp.set_y(0)

        self.play(
            FadeIn(top_simp),
            ShowIncreasingSubsets(top_row),
        )
        self.play(
            Restore(top_simp),
            Restore(top_row),
            FadeIn(simple_words[1:]),
            LaggedStartMap(FadeIn, block[4:])
        )
        self.add(block)
        self.add(simple_words)

        boxes = get_bit_grid_boxes(block, color=GREEN)
        bits_word = OldTexText("bits")
        bits_word.set_height(0.7)
        bits_word.next_to(boxes, LEFT, buff=LARGE_BUFF)
        counter = Integer(0, edge_to_fix=RIGHT)
        counter.match_height(bits_word)
        counter.next_to(bits_word, LEFT, buff=0.35)
        bit_count_group = VGroup(bits_word, counter)
        bit_count_group.set_color(YELLOW)

        self.play(
            FadeOut(simple_words),
            FadeIn(bits_word),
            UpdateFromAlphaFunc(
                counter,
                lambda m, a: m.set_fill(opacity=a)
            ),
            UpdateFromFunc(
                counter,
                lambda c: c.set_value(len(boxes))
            ),
            ShowIncreasingSubsets(boxes, run_time=2)
        )

        # Enumerate bits
        block.generate_target()
        block.target.space_out_submobjects(1.5)
        block.target.center()

        new_boxes = get_bit_grid_boxes(block.target, color=GREY_B)
        h_buff = get_norm(block.target[0].get_center() - block.target[4].get_center())
        for box in new_boxes:
            box.set_height(h_buff, stretch=True)

        p_labels = VGroup()
        for n, box in enumerate(new_boxes):
            label = Integer(n)
            label.set_height(0.25)
            label.set_color(YELLOW)
            label.move_to(box, DR)
            label.shift(SMALL_BUFF * UL)
            p_labels.add(label)

        self.play(
            MoveToTarget(block),
            Transform(boxes, new_boxes),
            FadeOut(title, UP),
            FadeOut(VGroup(counter, bits_word), LEFT),
        )
        self.play(FadeIn(p_labels, lag_ratio=0.07, run_time=3))
        self.wait()

        # Data bits
        r_boxes = VGroup(*[boxes[2**n] for n in range(4)]).copy()
        r_bits = VGroup(*[block[2**n] for n in range(4)])
        d_bits = VGroup(*[b for b in block if b not in r_bits])

        d_label = OldTexText("12 bits\\\\of data")
        d_label.set_height(1.5)
        d_label.next_to(boxes, RIGHT, aligned_edge=UP, buff=LARGE_BUFF)
        d_label.set_color(BLUE)

        d_lines = VGroup(*[
            Line(
                d_label.get_left(), bit.get_center(),
                color=(TEAL if get_bit_mob_value(bit) else YELLOW)
            )
            for bit in d_bits
        ])
        d_lines.set_stroke(width=1)

        self.play(
            FadeOut(r_bits),
            d_bits.set_color, BLUE,
            FadeIn(d_label),
            p_labels.set_color, WHITE,
        )
        self.play(LaggedStartMap(ShowCreationThenFadeOut, d_lines))
        self.wait()

        # Redundancy bits
        r_label = OldTexText("4 bits for\\\\", "redundancy")
        r_label.match_height(d_label)
        r_label.next_to(boxes, LEFT, aligned_edge=UP, buff=MED_LARGE_BUFF)
        r_label.set_color(GREEN)

        r_boxes.set_fill(GREEN, 0.5)
        self.add(r_boxes, p_labels)
        self.play(
            FadeIn(r_label, 0.2 * RIGHT),
            LaggedStartMap(FadeIn, r_boxes, run_time=2)
        )
        self.wait()

        # Can't cram in copies
        d_bit_copies = d_bits.copy()
        d_bit_copies.generate_target()
        for n, box in enumerate(r_boxes):
            group = d_bit_copies.target[3 * n:3 * (n + 1)]
            group.arrange_in_grid(2, 2, buff=SMALL_BUFF)
            group.set_width(0.4 * box.get_width())
            group.move_to(box)
            group.set_color(YELLOW)

        self.play(ShowCreationThenDestruction(Underline(r_label[1])))
        self.play(MoveToTarget(d_bit_copies, lag_ratio=0.1, run_time=4, rate_func=linear))
        self.wait()
        self.play(
            UpdateFromAlphaFunc(
                d_bit_copies, lambda m, a: m.shift(0.03 * np.sin(7 * TAU * a) * RIGHT).fade(a),
                remover=True
            )
        )

        # Set true redundancy bits
        highlights = boxes.copy()
        highlights.set_stroke(YELLOW, 6)

        for n in range(4):
            h_group = get_bit_n_subgroup(highlights, n)
            bit = r_bits[n]
            if get_bit_mob_value(bit) == 1:
                toggle_bit(bit)

            self.play(
                FadeIn(h_group, lag_ratio=0.2),
                FadeIn(bit)
            )
            anims = [FadeOut(h_group)]
            if n in [2, 3]:
                anims.append(toggle_bit_anim(bit))
            self.play(*anims)

        # Might expect them to come at the end
        movers = [d_bits, r_bits]
        for mover in movers:
            mover.save_state()
            mover.generate_target()

        for b1, b2 in zip(it.chain(d_bits.target, r_bits.target), block):
            b1.move_to(b2)

        for box, bit in zip(r_boxes, r_bits):
            box.bit = bit
            box.add_updater(lambda m: m.move_to(m.bit))

        self.add(*r_boxes)
        self.play(
            *[
                MoveToTarget(mover, lag_ratio=0.1, run_time=3, path_arc=20 * DEGREES)
                for mover in movers
            ],
        )
        self.wait()

        self.play(*[
            Restore(mover, lag_ratio=0.1, run_time=3, path_arc=20 * DEGREES)
            for mover in movers
        ])
        r_boxes.clear_updaters()
        self.wait()

        power_of_2_rects = VGroup(*[
            SurroundingRectangle(p_labels[2**n])
            for n in range(4)
        ])
        self.play(LaggedStartMap(ShowCreationThenFadeOut, power_of_2_rects))

        # Correct to 11 bits
        cross = Cross(d_label[0][:2])
        c_label = OldTexText("Er...11 bits")
        c_label.match_width(d_label)
        c_label.next_to(d_label, DOWN, buff=MED_LARGE_BUFF)
        c_label.set_color(RED)
        q_mark = OldTex("?")
        q_mark.replace(block[0])
        q_mark.set_color(RED)

        self.play(ShowCreation(cross))
        self.play(Write(c_label))
        self.wait()
        self.play(
            FadeOut(block[0]),
            Write(q_mark),
        )

        randy = Randolph()
        randy.to_corner(DL)

        self.play(
            VFadeIn(randy),
            randy.change, "confused", q_mark
        )
        self.play(Blink(randy))
        self.wait(2)
        self.play(Blink(randy))
        self.wait()

    def old_functions(self):
        # Show redundancy and message
        redundancy_words = OldTexText("Separate some for\\\\redundancy")
        redundancy_words.next_to(block[-4:], LEFT, buff=LARGE_BUFF, aligned_edge=UP)
        redundancy_words.set_color(BLUE)

        vect = redundancy_words.get_center() - bit_count_group.get_center()
        self.play(
            FadeOut(bit_count_group, vect),
            FadeIn(redundancy_words, -vect),
            ApplyMethod(boxes[-4:].set_color, BLUE, lag_ratio=0.2),
            ApplyMethod(block[-4:].set_color, BLUE, lag_ratio=0.2),
        )
        self.wait()

        message_words = OldTexText("Leave the rest\\\\for a message")
        message_words.next_to(block[:-4], LEFT)
        message_words.match_x(redundancy_words)
        message_words.set_color(YELLOW)
        message_words.save_state()
        message_words.replace(redundancy_words)
        message_words.set_opacity(0)

        self.play(
            Restore(message_words),
            boxes[:-4].set_color, YELLOW,
        )
        for x in range(10):
            bits = list(block[:-4])
            random.shuffle(bits)
            for bit in bits:
                if random.random() < 0.5:
                    toggle_bit(bit)
                self.wait(0.2 / 12)
        self.wait()

        # Show correction
        flipper = random.choice(block)
        scanim = scan_anim(
            block.get_corner(DR) + 2 * RIGHT, block,
            final_stroke_width=0.5,
            lag_factor=1,
        )

        self.play(
            zap_anim(flipper),
            toggle_bit_anim(flipper, target_color=RED)
        )
        self.wait()
        self.play(scanim)
        self.play(focus_scan_anim_lines(scanim, flipper.get_center()))
        self.play(
            toggle_bit_anim(flipper, target_color=WHITE),
            FadeOut(scanim.mobject)
        )
