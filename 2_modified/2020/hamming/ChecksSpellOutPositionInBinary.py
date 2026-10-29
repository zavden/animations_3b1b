# ==============================================================================
# Scene:      ChecksSpellOutPositionInBinary
# Source:     videos/_2020/hamming.py (lines 3711-4187)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ChecksSpellOutPositionInBinary.py ChecksSpellOutPositionInBinary -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - set_fill(0): the 0 was the opacity, not a color
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


class ChecksSpellOutPositionInBinary(Scene):
    def construct(self):
        N = 4
        pos = 7

        # Setup block
        random.seed(0)
        bits = [random.choice([0, 1]) for n in range(2**N)]
        bits[1] = 0
        bits[2] = 1
        bits[4] = 0
        bits[8] = 0
        block = get_bit_grid(2**(N // 2), 2**(N // 2), bits=bits)
        block.set_height(5)
        block.to_edge(LEFT, buff=LARGE_BUFF)
        boxes = get_bit_grid_boxes(block)
        VGroup(*[boxes[2**n] for n in range(N)]).set_fill(GREY_D, 1)

        pos_labels = VGroup(*map(Integer, range(2**N)))
        pos_labels.set_height(0.2)
        for label, box, bit_label in zip(pos_labels, boxes, block):
            label.move_to(box, DR)
            label.shift(0.1 * UL)
            label.set_color(GREY_A)
            bit_label.scale(0.8)

        self.add(boxes)
        self.add(block)
        self.add(pos_labels)

        self.play(
            zap_anim(block[pos]),
            toggle_bit_anim(block[pos]),
        )

        # Setup questions
        parity_groups = VGroup()
        for n in range(N):
            group = boxes.copy()
            group.set_height(1)
            group.set_width(1, stretch=True)
            group.set_fill(BLACK, 0)
            get_bit_n_subgroup(group, n).set_fill(BLUE_D, 1)
            parity_groups.add(group)
        parity_groups.arrange(DOWN, buff=MED_LARGE_BUFF)
        parity_groups.set_height(6)
        parity_groups.to_edge(RIGHT, buff=3)

        q_labels = VGroup(*[TexText(f"Q{n + 1}:") for n in range(N)])
        for label, group in zip(q_labels, parity_groups):
            label.next_to(group, LEFT, MED_SMALL_BUFF)

        self.play(
            FadeIn(parity_groups),
            FadeIn(q_labels),
        )

        # Binary search down
        bits_word = "{0:b}".format(pos)
        bits_word = (N - len(bits_word)) * '0' + bits_word
        bits = list(map(int, bits_word[::-1]))

        boxes.save_state()
        yes_no_words = VGroup()
        possible_positions = list(range(2**N))
        for n, bit, group in zip(it.count(), bits, parity_groups):
            if bit:
                word = OldTexText("Yes", color=GREEN)
            else:
                word = OldTexText("No", color=RED)
            word.next_to(group, RIGHT)
            yes_no_words.add(word)

            possible_positions = list(filter(
                lambda i: i in get_bit_n_sublist(range(2**N), n, bit_value=bit),
                possible_positions,
            ))

            boxes.target = boxes.saved_state.copy()
            VGroup(*[boxes.target[i] for i in possible_positions]).set_fill(BLUE_D, 0.8)

            self.play(
                FadeIn(word, 0.5 * LEFT),
                MoveToTarget(boxes),
            )
            self.wait()

        # Spell answer in binary
        binary_answers = VGroup(*[
            Integer(bit).move_to(word).match_color(word)
            for bit, word in zip(bits, yes_no_words)
        ])

        self.play(
            LaggedStartMap(GrowFromCenter, binary_answers),
            LaggedStartMap(ApplyMethod, yes_no_words, lambda m: (m.scale, 0), remover=True),
        )

        # Show value of 7
        frame = self.camera.frame

        binary_pos_label = binary_answers.copy()
        binary_pos_label.generate_target()
        binary_pos_label.target.arrange(LEFT, buff=SMALL_BUFF, aligned_edge=DOWN)

        equation = VGroup(
            Integer(7, color=BLUE),
            OldTex("\\rightarrow"),
            binary_pos_label.target,
        )
        equation.arrange(RIGHT)
        equation.to_edge(UP, buff=0)

        arrow = Arrow(equation.get_left(), equation.get_right(), buff=0)
        arrow.next_to(equation, DOWN, SMALL_BUFF)
        trans_words = OldTexText("Decimal to binary")
        trans_words.match_width(arrow)
        trans_words.next_to(arrow, DOWN, SMALL_BUFF)

        self.play(
            MoveToTarget(binary_pos_label),
            frame.move_to, 0.5 * UP
        )
        self.play(
            Write(equation[:-1]),
            Write(trans_words),
            GrowArrow(arrow),
            run_time=1,
        )
        self.wait()

        bin_group = VGroup(*equation[:-1], binary_pos_label, arrow, trans_words)

        # Spell out binary
        bin_equation = OldTex(
            "{7} = {0} \\cdot 8 + {1} \\cdot 4 + {1} \\cdot 2 + {1} \\cdot 1",
            tex_to_color_map={
                "{0}": RED,
                "{1}": GREEN,
                "{7}": BLUE,
            }
        )
        bin_equation.move_to(bin_group, UP)

        bit_parts = list(it.chain(*[
            bin_equation.get_parts_by_tex(f"{{{d}}}")
            for d in [0, 1]
        ]))

        self.play(
            bin_group.next_to, bin_equation, DOWN, LARGE_BUFF,
            *[
                ApplyMethod(m1.copy().replace, m2, {"dim_to_match": 1}, remover=True, run_time=1.5)
                for m1, m2 in zip(binary_pos_label[::-1], bit_parts)
            ],
            ApplyMethod(equation[0].copy().replace, bin_equation[0], remover=True, run_time=1.5)
        )
        self.add(bin_equation[0], *bit_parts)
        self.play(FadeIn(VGroup(*[
            part
            for part in bin_equation
            if part.get_tex() not in ["{0}", "{1}", "{7}"]
        ]), lag_ratio=0.1))
        self.add(bin_equation)
        self.wait()

        # Error at 7
        toggle_bit(block[pos])
        self.play(
            zap_anim(block[pos]),
            toggle_bit_anim(block[pos], target_color=RED),
        )
        self.wait()

        # Four parity checks
        for n, label, group, word in zip(it.count(), q_labels, parity_groups, yes_no_words):
            boxes.target = boxes.saved_state.copy()
            get_bit_n_subgroup(boxes.target, n).set_fill(BLUE, 0.8)

            rect = SurroundingRectangle(VGroup(label, group, word), buff=MED_SMALL_BUFF)
            one_rects = get_one_rects(get_bit_n_subgroup(block, n))

            self.play(
                MoveToTarget(boxes),
                ShowCreation(rect),
                ShowIncreasingSubsets(one_rects)
            )
            self.play(
                FadeOut(one_rects),
                FadeOut(rect),
            )
            self.wait(0.5)
        self.play(Restore(boxes))
        self.wait()

        # Other examples
        toggle_bit(block[7])
        block[7].set_color(WHITE)

        bit_parts = VGroup(*bit_parts)
        to_save = VGroup(
            equation[0], bin_equation[0],
            bit_parts, binary_pos_label, binary_answers,
        )
        to_save.save_state()

        ns = random.sample(list(range(16)), 10)
        for n in ns:
            toggle_bit(block[n])
            block[n].set_color(YELLOW)

            nc1 = Integer(n)
            nc1.replace(equation[0], 1)
            nc1.match_color(equation[0])
            equation[0].set_opacity(0)
            nc2 = nc1.copy()
            nc2.replace(bin_equation[0], 1)
            # CHANGE: set_fill(0): the 0 was the opacity, not a color
            bin_equation[0].set_fill(opacity=0)

            new_bits = int_to_bit_string(n, 4)
            new_bit_mobs = VGroup()
            for b1, b2, b3, value in zip(reversed(bit_parts), binary_pos_label, binary_answers, reversed(new_bits)):
                new_mob = OldTex(value)
                new_mob.set_color(GREEN if int(value) else RED)
                for b in (b1, b2, b3):
                    nmc = new_mob.copy()
                    nmc.replace(b, 1)
                    b.set_opacity(0)
                    new_bit_mobs.add(nmc)

            self.play(*[
                Animation(mob, remover=True, run_time=1)
                for mob in [new_bit_mobs, nc1, nc2]
            ])

            toggle_bit(block[n])
            block[n].set_color(WHITE)

        to_save.restore()
        self.wait()

        # Remove 7 stuff
        self.play(
            FadeOut(VGroup(
                *bin_group, *bin_equation, *binary_answers
            ), lag_ratio=0.1),
            block[pos].set_color, WHITE,
        )

        question_group = VGroup(q_labels, parity_groups)

        # Show numbers 0 through 15
        pos_labels_movers = pos_labels.copy()
        bin_pos_groups = VGroup()
        arrows = VGroup()
        bin_labels = VGroup()

        for n, label in enumerate(pos_labels_movers):
            label.scale(2)
            arrow = OldTex("\\rightarrow")
            bits_word = "{0:b}".format(n)
            bits_word = (N - len(bits_word)) * '0' + bits_word
            bin_label = VGroup(*[Tex(b) for b in bits_word])
            bin_label.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
            pos_group = VGroup(label, arrow, bin_label)
            pos_group.arrange(RIGHT, buff=MED_SMALL_BUFF)
            bin_pos_groups.add(pos_group)
            arrows.add(pos_group[1])
            bin_labels.add(bin_label)

        bin_pos_groups.arrange_in_grid(8, 2, fill_rows_first=False)
        bin_pos_groups.set_height(7)
        bin_pos_groups.to_edge(RIGHT)
        bin_pos_groups.set_y(0.5)

        self.play(
            FadeOut(question_group),
            FadeIn(arrows, lag_ratio=0.02),
            TransformFromCopy(pos_labels, pos_labels_movers),
        )
        self.play(ShowIncreasingSubsets(bin_labels, run_time=3, rate_func=bezier([0, 0, 1, 1])))
        self.wait()

        # Put bin labels in boxes
        for label, box in zip(bin_labels, boxes):
            label.generate_target()
            label.target.set_width(0.7 * box.get_width())
            label.target.move_to(box, DOWN)
            label.target.shift(SMALL_BUFF * UP)

        for bit in block:
            bit.generate_target()
            bit.target.scale(0.5, about_edge=UP),
            bit.target.fade(0.5)

        kw = {
            "run_time": 5,
            "lag_ratio": 0.3,
        }
        self.play(
            LaggedStartMap(MoveToTarget, bin_labels, **kw),
            LaggedStartMap(FadeOut, arrows, **kw),
            LaggedStartMap(FadeOut, pos_labels_movers, **kw),
            LaggedStartMap(FadeOut, pos_labels, **kw),
            LaggedStartMap(MoveToTarget, block, **kw),
        )
        self.wait()

        # Show confusion
        randy = Randolph()
        randy.flip()
        randy.to_corner(DR, buff=LARGE_BUFF)

        self.play(
            VFadeIn(randy),
            randy.change, "maybe", boxes,
        )
        self.play(PiCreatureBubbleIntroduction(
            randy, "Wait...",
            target_mode="confused",
            bubble_type=ThoughtBubble,
            look_at=boxes.get_top(),
        ))
        self.play(Blink(randy))
        self.wait()

        self.play(LaggedStart(*map(ShowCreationThenFadeAround, bin_labels), lag_ratio=0))
        self.play(randy.change, "maybe")
        self.play(
            LaggedStart(*[ShowCreationThenFadeOut(SurroundingRectangle(b, color=GREEN)) for b in block], lag_ratio=0),
            randy.look_at, boxes.get_bottom(),
        )
        self.play(Blink(randy))
        self.play(
            randy.change, 'pondering', boxes,
            FadeOut(randy.bubble),
            FadeOut(randy.bubble.content),
        )
        for x in range(2):
            self.wait()
            self.play(Blink(randy))
            self.play(randy.change, "thinking")
        self.play(FadeOut(randy))

        # Go through parity group 1 (and setup others)
        bit_arrow_groups = VGroup()
        for n in range(N):
            arrow_group = VGroup()
            for bin_label in bin_labels:
                char = bin_label[-(n + 1)]
                arrow = Triangle(start_angle=-PI / 2)
                arrow.stretch(0.8, 0)
                arrow.set_height(0.8 * char.get_height())
                arrow.next_to(char, UP, buff=0.05)
                arrow.set_stroke(width=0)
                if char.get_tex() == '0':
                    arrow.set_fill(GREY, 1)
                else:
                    arrow.set_fill(BLUE, 1)
                arrow_group.add(arrow)
            bit_arrow_groups.add(arrow_group)

        highlight_groups = VGroup()
        for n in range(N):
            highlight_group = boxes.copy()
            highlight_group.set_fill(BLACK, 0)
            get_bit_n_subgroup(highlight_group, n).set_fill(BLUE, 0.5)
            highlight_groups.add(highlight_group)

        questions = VGroup()
        for n in range(N):
            chars = ["\\underline{\\phantom{0}}" for x in range(4)]
            chars[-(n + 1)] = "\\underline{1}"
            question = OldTexText(
                f"""
                If there's an error, does\\\\
                its position look like\\\\
                """,
                " ".join(chars),
                "?"
            )
            question.scale(1.25)
            question[1:].scale(1.5, about_edge=UP)
            question[1:].shift(SMALL_BUFF * DOWN)
            question[1].set_color(BLUE)
            question.next_to(boxes, RIGHT, LARGE_BUFF)
            questions.add(question)

        self.play(
            LaggedStartMap(FadeIn, bit_arrow_groups[0], lag_ratio=0.3, run_time=3),
            FadeOut(block),
        )
        self.play(Transform(boxes, highlight_groups[0]))
        self.wait()
        self.play(Write(questions[0]))
        self.wait()

        # Go through parity groups 2-4
        bit_arrows = bit_arrow_groups[0]
        for n in range(1, N):
            self.play(boxes.set_fill, BLACK, 0)
            self.play(
                Transform(bit_arrows, bit_arrow_groups[n]),
                FadeOut(questions[n - 1])
            )
            self.wait()
            self.play(
                Transform(boxes, highlight_groups[n]),
                FadeIn(questions[n])
            )
            self.wait()

        # Organize questions
        questions.generate_target()
        questions.target.arrange(DOWN, buff=LARGE_BUFF)
        questions.target.set_height(FRAME_HEIGHT - 1)
        questions.target.next_to(boxes, RIGHT, buff=1.5)
        questions.target.match_y(frame)
        questions[:N - 1].set_opacity(0)

        self.play(
            MoveToTarget(questions),
            Restore(boxes),
            FadeOut(bit_arrows),
        )

        fade_anims = []
        for n in range(N):
            rect = SurroundingRectangle(questions[n])
            rect.set_stroke(BLUE, 2)
            self.play(
                FadeIn(highlight_groups[n]),
                FadeIn(rect),
                *fade_anims
            )
            fade_anims = [
                FadeOut(highlight_groups[n]),
                FadeOut(rect),
            ]
        self.play(*fade_anims)

        # Note power of 2 points
        parity_arrows = VGroup(Vector(DOWN), Vector(DOWN), Vector(RIGHT), Vector(RIGHT))
        parity_arrows[0].next_to(boxes[1], UP, SMALL_BUFF)
        parity_arrows[1].next_to(boxes[2], UP, SMALL_BUFF)
        parity_arrows[2].next_to(boxes[4], LEFT, SMALL_BUFF)
        parity_arrows[3].next_to(boxes[8], LEFT, SMALL_BUFF)
        parity_arrows.set_color(GREEN)

        parity_groups = VGroup()
        for n, question in enumerate(questions):
            pg = boxes.copy()
            pg.set_width(pg.get_height(), stretch=True)
            pg.set_height(0.8 * question.get_height())
            pg.set_fill(BLACK, 0)
            get_bit_n_subgroup(pg, n).set_fill(BLUE, 0.8)
            pg.next_to(question, RIGHT, LARGE_BUFF)
            parity_groups.add(pg)

        self.play(
            LaggedStartMap(GrowArrow, parity_arrows),
            ApplyMethod(frame.set_x, -1, run_time=2)
        )
        self.wait()
        rects = VGroup(*[boxes[2**n].copy() for n in range(N)])
        rects.set_fill(BLUE, 0.8)
        self.add(rects, bin_label)
        self.play(
            LaggedStartMap(VFadeInThenOut, rects, lag_ratio=0.5, run_time=5),
            LaggedStartMap(FadeIn, parity_groups, lag_ratio=0.5, run_time=5),
        )
        self.wait()
        self.add(rects, bin_label)
        self.play(
            LaggedStartMap(VFadeInThenOut, rects, lag_ratio=0.5, run_time=5),
        )
        self.wait()
