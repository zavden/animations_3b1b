# ==============================================================================
# Scene:      TwentyQuestions
# Source:     videos/_2020/hamming.py (lines 2602-3449)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwentyQuestions.py TwentyQuestions -w -m --fps 15
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


class TwentyQuestions(Scene):
    def construct(self):
        # Hamming's insight
        bits = [
            1, 0, 0, 1,
            0, 1, 0, 0,
            0, 1, 0, 1,
            1, 0, 1, 1,
        ]
        block = get_bit_grid(4, 4, bits=bits)

        hamming = ImageMobject("Richard_Hamming")
        hamming.set_height(3)
        hamming.to_corner(DL)

        bulb = Lightbulb()
        bulb.next_to(hamming.get_corner(UR), UP)

        self.add(block)
        self.play(FadeIn(hamming, 0.5 * RIGHT))
        self.play(Write(bulb, run_time=1, stroke_width=5))
        self.wait()

        # Preview parity checks
        parity_word = OldTexText("Parity check")
        parity_word.set_height(0.7)
        parity_word.set_color(BLUE)
        parity_word.move_to(block, UP)
        parity_word.set_opacity(0)

        back_rects = VGroup(*[
            SurroundingRectangle(bit, buff=MED_SMALL_BUFF / 2).scale(0)
            for bit in get_bit_n_subgroup(block, 0)
        ])
        back_rects.set_stroke(width=0)
        back_rects.set_fill(BLUE_E, 1)

        last_one_rects = VMobject()

        self.add(back_rects, block)

        for n, vect in zip(it.count(), [UP, UP, RIGHT, RIGHT]):
            block.generate_target()
            block.target.set_color(WHITE)
            color_group = get_bit_n_subgroup(block.target, n)
            color_group.set_color(BLUE)
            one_rects = get_one_rects(color_group)

            rects = VGroup(*[
                SurroundingRectangle(bit, buff=MED_SMALL_BUFF / 2)
                for bit in color_group
            ])
            rects.match_style(back_rects)

            self.play(
                FadeOut(last_one_rects),
                MoveToTarget(block),
                parity_word.next_to, color_group, vect, MED_LARGE_BUFF,
                parity_word.set_opacity, 1,
                Transform(back_rects, rects),
            )
            self.play(ShowIncreasingSubsets(one_rects))
            last_one_rects = one_rects

        self.play(
            FadeOut(back_rects),
            FadeOut(last_one_rects),
            FadeOut(parity_word),
            block.set_color, WHITE,
        )

        # Expand to grid
        block.generate_target()
        block.target.space_out_submobjects(1.5)
        block.target.to_edge(LEFT, buff=LARGE_BUFF)

        boxes = get_bit_grid_boxes(block.target)
        p_labels = get_grid_position_labels(boxes)
        p_labels.set_color(GREY_C)

        self.play(
            FadeOut(hamming, LEFT),
            FadeOut(bulb, 1.5 * LEFT),
            MoveToTarget(block),
        )
        self.play(
            ShowCreation(boxes, lag_ratio=0.2),
            FadeIn(p_labels, lag_ratio=0.2),
        )

        # Set up questions
        q_labels = VGroup(*[
            OldTexText(f"Q{n}:")
            for n in range(1, 5)
        ])
        q_labels.set_height(0.5)
        q_labels.arrange(DOWN, buff=1.25)
        q_labels.next_to(boxes, RIGHT, buff=2)

        questions = VGroup()
        for n, q_label in enumerate(q_labels):
            m_grids = VGroup(boxes.copy(), boxes.copy())
            m_grids.set_height(1)
            m_grids.set_width(1, stretch=True)
            colors = [GREY_BROWN, BLUE]
            for k, m_grid in enumerate(m_grids):
                get_bit_n_subgroup(m_grid, n, k).set_fill(colors[k], 0.75)
            vs = OldTexText("or")
            question = VGroup(m_grids[0], vs, m_grids[1])
            question.arrange(RIGHT)
            question.next_to(q_label, RIGHT, buff=MED_SMALL_BUFF)
            question.add_to_back(q_label)
            questions.add(question)

        questions.to_edge(RIGHT, buff=MED_LARGE_BUFF)

        for question in questions:
            question.save_state()
            q_center = question.get_center()
            for mob in question:
                if mob is not question[0]:
                    mob.move_to(q_center)
                mob.set_fill(opacity=0)
                mob.set_stroke(width=0)

        self.play(
            LaggedStartMap(Restore, questions, lag_ratio=0.25),
            run_time=3,
        )
        self.wait()

        questions.save_state()

        # Focus on question 1
        h_rects = boxes.copy()
        h_rects.set_fill(BLUE, 0.5)
        h_groups = VGroup(*[
            get_bit_n_subgroup(h_rects, n)
            for n in range(4)
        ])

        pc_words = OldTexText("Parity check\\\\these 8 bits")
        pc_words.next_to(boxes, RIGHT, aligned_edge=UP)
        pc_words.shift(DOWN)
        pc_words.set_color(BLUE)

        block.save_state()
        self.add(h_groups[0], block, p_labels)
        self.play(
            questions[1:].fade, 0.9,
            FadeIn(h_groups[0], lag_ratio=0.3, run_time=3),
            get_bit_n_subgroup(block, 0, 0).fade, 0.9,
            Write(pc_words, run_time=1)
        )
        self.wait()

        # Scan first group
        def get_sub_scanim(n, boxes=boxes, block=block, **kwargs):
            return scan_anim(
                boxes.get_corner(DR) + UR,
                get_bit_n_subgroup(block, n),
                lag_factor=0.5,
                run_time=2,
                **kwargs
            )

        scanim = get_sub_scanim(0)
        robot = scanim.mobject[-1]
        bangs = OldTex("!!!")
        bangs.set_color(RED)
        bangs.next_to(robot, UR, buff=SMALL_BUFF)
        check = Checkmark()
        check.next_to(robot, UR, buff=SMALL_BUFF)
        for mob in (bangs, check):
            mob.scale(1.5, about_edge=DL)

        q1_rect = SurroundingRectangle(questions[0][3])

        self.play(scanim)
        self.play(FadeIn(bangs, 0.1 * DOWN, lag_ratio=0.2))
        self.wait()
        self.play(ShowCreation(q1_rect))
        self.wait()
        self.play(
            get_sub_scanim(0, show_robot=False),
            FadeOut(bangs)
        )
        self.play(FadeIn(check, 0.2 * DOWN))
        self.wait()
        self.play(
            q1_rect.move_to, questions[0][1],
        )
        self.play(
            LaggedStartMap(
                ShowCreationThenFadeOut,
                get_bit_n_subgroup(h_rects, 0, 0).copy().set_fill(GREY_BROWN, 0.5)
            )
        )
        self.wait()
        self.play(LaggedStart(*map(FadeOut, [
            robot, check, q1_rect,
        ])))

        # Comment over in pi creature scene
        pass

        # Highlight parity bit
        frame = self.camera.frame
        frame.save_state()

        ecc_rects = VGroup(*[
            h_group[0]
            for h_group in h_groups
        ])
        pb_label = OldTexText("Parity bit")
        pb_label.next_to(ecc_rects[0], UP, MED_LARGE_BUFF)
        pb_arrow = Arrow(
            pb_label.get_bottom() + MED_SMALL_BUFF * LEFT,
            block[1].get_top(),
            buff=0.1
        )
        pb_label.set_color(GREEN)
        pb_arrow.set_color(GREEN)
        pb_arrow.set_stroke(BLACK, 5, background=True)

        h_groups[0].remove(ecc_rects[0])
        self.add(ecc_rects[0], block, p_labels)
        self.play(
            frame.set_height, 9, {"about_edge": DOWN},
            FadeIn(pb_label, 0.5 * DOWN),
            GrowArrow(pb_arrow),
            ecc_rects[0].set_color, GREEN,
        )
        self.wait()
        self.play(ShowCreationThenFadeAround(p_labels[1]))
        self.wait()

        one_rects = get_one_rects(get_bit_n_subgroup(block, 0))
        counter = get_ones_counter(boxes[-2:], one_rects)
        counter.scale(0.5)
        self.add(counter)
        self.play(ShowIncreasingSubsets(one_rects))
        self.wait()
        self.play(toggle_bit_anim(block[1]))
        one_rects.set_submobjects(
            get_one_rects(get_bit_n_subgroup(block, 0)).submobjects
        )
        self.wait()

        # Back to all questions
        self.play(
            LaggedStart(*map(FadeOut, [
                one_rects, counter,
                pb_arrow, pb_label,
                pc_words, h_groups[0]
            ])),
            frame.restore,
        )
        toggle_bit(block.saved_state[1])  # Dumb hack
        self.play(
            questions.restore,
            block.restore,
        )

        # Focus on question 2
        self.play(
            questions[0].fade, 0.9,
            questions[2:].fade, 0.9,
            get_bit_n_subgroup(block, 1, 0).fade, 0.9,
            ecc_rects[0].fade, 0.5,
        )
        self.add(h_groups[1], block, p_labels)
        self.play(FadeIn(h_groups[1], lag_ratio=0.2, run_time=2))

        pb_label.next_to(boxes[2], UP, SMALL_BUFF)
        h_groups[1].remove(ecc_rects[1])
        self.add(ecc_rects[1], block, p_labels)
        self.play(
            FadeIn(pb_label, 0.25 * LEFT),
            ecc_rects[1].set_color, GREEN,
        )
        self.wait()

        # Apply second parity check
        one_rects = get_one_rects(get_bit_n_subgroup(block, 1))
        counter = get_ones_counter(boxes[-2:], one_rects)
        counter.scale(0.5)
        self.add(counter)
        self.play(
            ShowIncreasingSubsets(one_rects)
        )
        self.wait()
        self.play(LaggedStart(*map(FadeOut, [
            one_rects, counter, pb_label,
        ])))

        # Find error in right half
        scanim = get_sub_scanim(1)
        robot = scanim.mobject[-1]
        self.play(
            zap_anim(block[6]),
            toggle_bit_anim(block[6], target_color=RED)
        )
        self.play(scanim)
        self.play(FadeIn(bangs, 0.1 * DOWN, lag_ratio=0.1))
        self.wait()

        q2_rect = q1_rect.copy()
        q2_rect.move_to(questions[1][3])
        self.play(ShowCreation(q2_rect))
        self.wait()

        self.play(
            toggle_bit_anim(block[6], target_color=WHITE),
            FadeOut(bangs),
        )
        self.play(get_sub_scanim(1, show_robot=False))
        self.play(FadeIn(check, 0.2 * DOWN))
        self.wait()
        self.play(q2_rect.move_to, questions[1][1])
        self.play(
            ShowCreationThenFadeOut(
                get_bit_n_subgroup(boxes.copy(), 1, 0).set_fill(GREY_BROWN, 0.5),
                lag_ratio=0.5,
                run_time=2,
            )
        )
        self.wait()

        self.play(
            FadeOut(h_groups[1]),
            FadeOut(robot),
            FadeOut(check),
            FadeOut(q2_rect),
            block.restore,
            Transform(questions[0], questions.saved_state[0]),
            ecc_rects[0].set_fill, GREEN, 0.5,
        )

        # Mention two errors?

        # How to use Q1 with Q2
        q1_rect.move_to(questions[0][3])
        q2_rect.move_to(questions[1][3])
        q1_highlight, q2_highlight = [
            get_bit_n_subgroup(h_rects, n).copy().set_fill(BLUE, 0.5)
            for n in [0, 1]
        ]

        q2_highlight.set_fill(opacity=0)
        q2_highlight.set_stroke(YELLOW, 7)

        self.add(q1_highlight, block, p_labels)
        self.play(
            FadeIn(q1_highlight, lag_ratio=0.2),
            ShowCreation(q1_rect),
            get_bit_n_subgroup(block, 0, 0).fade, 0.9,
            *map(FadeOut, ecc_rects[:2]),
        )
        self.wait()
        self.play(
            FadeIn(q2_highlight, lag_ratio=0.2),
            ShowCreation(q2_rect),
            get_bit_n_subgroup(block, 1, 0)[1::2].fade, 0.9,
        )
        self.wait(2)
        self.play(
            q1_rect.move_to, questions[0][1],
            q1_highlight.move_to, boxes, LEFT,
            q1_highlight.set_fill, GREY_BROWN,
            block.restore,
            FadeOut(q2_highlight),
        )
        self.play(get_bit_n_subgroup(block, 0).fade, 0.9)
        self.wait()
        self.play(
            FadeIn(q2_highlight, lag_ratio=0.2),
            block[::4].fade, 0.9,
        )
        self.wait(2)
        self.play(
            q1_highlight.move_to, boxes, RIGHT,
            q1_highlight.set_fill, BLUE,
            q2_highlight.move_to, boxes, LEFT,
            block.restore,
            q1_rect.move_to, questions[0][3],
            q2_rect.move_to, questions[1][1],
        )
        self.play(
            block[::4].fade, 0.9,
            get_bit_n_subgroup(block, 1).fade, 0.9,
        )
        self.wait(2)
        self.play(
            q1_rect.move_to, questions[0][1],
            q1_highlight.move_to, boxes, LEFT,
            q1_highlight.set_fill, GREY_BROWN,
            block[1::4].fade, 0.9,
            Transform(block[0::4], block.saved_state[0::4]),
        )
        self.wait()

        morty = Mortimer(height=2)
        morty.flip()
        morty.next_to(boxes, RIGHT, buff=0.5, aligned_edge=DOWN)
        words = OldTexText("Or no error\\\\at all!")
        words.next_to(morty, UP)

        self.play(
            VFadeIn(morty),
            morty.change, "shruggie", questions[0],
            FadeIn(words, DOWN)
        )
        self.play(Blink(morty))
        self.wait(2)
        self.play(
            LaggedStart(*map(FadeOut, [
                q1_highlight, q2_highlight[1::2],
                words, morty,
            ])),
            block.restore,
        )
        self.wait()

        column_highlight = q2_highlight[0::2]

        # Choosing a column
        self.play(
            q1_rect.move_to, questions[0][3],
            column_highlight.move_to, boxes[1], UP,
        )
        self.wait()
        self.play(
            q1_rect.move_to, questions[0][1],
            q2_rect.move_to, questions[1][3],
            column_highlight.move_to, boxes[2], UP,
        )
        self.wait()
        self.play(
            q1_rect.move_to, questions[0][3],
            column_highlight.move_to, boxes[3], UP,
        )
        self.wait()

        # Bring back the parity highlights
        self.add(*ecc_rects[:2], block, p_labels)
        self.play(
            LaggedStart(*map(FadeOut, [
                column_highlight, q1_rect, q2_rect
            ])),
            *map(FadeIn, ecc_rects[:2]),
        )
        self.wait()
        for n in [2, 3]:
            self.play(Transform(questions[n], questions.saved_state[n]))
        self.wait()

        # Question 3
        self.add(h_groups[2], block, p_labels)
        self.play(
            get_bit_n_subgroup(block, 2, 0).fade, 0.9,
            FadeIn(h_groups[2], lag_ratio=0.2, run_time=2),
            questions[:2].fade, 0.9,
            questions[3].fade, 0.9,
        )
        self.wait()

        h_groups[2].remove(ecc_rects[2])
        self.add(ecc_rects[2], block, p_labels)
        self.play(
            ecc_rects[2].set_color, GREEN,
            ShowCreationThenFadeOut(SurroundingRectangle(boxes[4], buff=0))
        )
        self.wait()

        one_rects = get_one_rects(get_bit_n_subgroup(block, 2))
        self.play(ShowIncreasingSubsets(one_rects))
        self.wait()
        temp_check = Checkmark()
        temp_check.set_height(0.4)
        temp_check.next_to(block[4], UL, buff=0)
        self.play(Write(temp_check))
        self.play(FadeOut(temp_check))
        self.play(FadeOut(one_rects))
        self.play(
            block.restore,
            FadeOut(h_groups[2]),
        )
        self.wait()

        # Question 4
        self.add(h_groups[3], block, p_labels)
        self.play(
            questions[2].fade, 0.9,
            Transform(questions[3], questions.saved_state[3]),
            get_bit_n_subgroup(block, 3, 0).fade, 0.9,
            FadeIn(h_groups[3], lag_ratio=0.2, run_time=2),
        )
        self.wait()
        h_groups[3].remove(ecc_rects[3])
        self.add(ecc_rects[3], block, p_labels)
        self.play(
            ecc_rects[3].set_color, GREEN,
            ShowCreationThenFadeOut(SurroundingRectangle(boxes[8], buff=0))
        )

        one_rects = get_one_rects(get_bit_n_subgroup(block, 3))
        self.play(ShowIncreasingSubsets(one_rects))
        self.wait()
        self.play(toggle_bit_anim(block[8]))
        toggle_bit(block.saved_state[8])
        one_rects.set_submobjects(get_one_rects(get_bit_n_subgroup(block, 3)))
        self.wait()
        self.play(FadeOut(one_rects, lag_ratio=0.2))
        self.play(
            block.restore,
            questions.restore,
            FadeOut(h_groups[3], lag_ratio=0.2),
        )
        self.wait()

        # Point out rolls of questions
        braces = VGroup(
            Brace(questions[:2], LEFT),
            Brace(questions[2:], LEFT),
        )
        for brace, text in zip(braces, ["column", "row"]):
            brace.words = brace.get_text(f"Which\\\\{text}?")

        for brace in braces:
            self.play(
                GrowFromCenter(brace),
                FadeIn(brace.words, 0.25 * RIGHT)
            )
            self.wait()

        # Example with error at 3
        q_rects = VGroup()
        for question, answer in zip(questions, [1, 1, 0, 0]):
            q_rects.add(SurroundingRectangle(question[1 + 2 * answer]))

        self.play(
            zap_anim(block[3]),
            toggle_bit_anim(block[3], target_color=RED),
        )
        self.wait()

        target_square = SurroundingRectangle(boxes[3::4], buff=0, stroke_width=5)
        for n in range(4):
            highlight = get_bit_n_subgroup(h_rects.copy(), n)
            one_rects = get_one_rects(get_bit_n_subgroup(block, n))
            self.add(highlight, block, p_labels)
            self.play(
                FadeIn(highlight),
                ShowCreation(q_rects[n]),
                ShowIncreasingSubsets(one_rects),
            )
            self.wait()
            self.play(
                FadeOut(highlight),
                FadeOut(one_rects),
            )
            if n == 1:
                self.play(FadeIn(target_square))
            elif n == 3:
                self.play(target_square.replace, boxes[3], {"stretch": True})
        self.wait()
        self.play(
            toggle_bit_anim(block[3], target_color=WHITE)
        )
        self.wait()

        # Binary counting
        for n in range(1, 16):
            target_square.generate_target()
            target_square.target.move_to(boxes[n])
            for k, q_rect in enumerate(q_rects):
                index = 3 if((1 << k) & n) else 1
                q_rect.generate_target()
                q_rect.target.move_to(questions[k][index])
            self.play(*map(MoveToTarget, [target_square, *q_rects]), run_time=0.5)
            self.wait()

        # Bit 0
        for q_rect, question in zip(q_rects, questions):
            q_rect.generate_target()
            q_rect.target.move_to(question[1])

        self.play(
            target_square.move_to, boxes[0],
            LaggedStartMap(MoveToTarget, q_rects),
        )
        self.wait()
        for n in range(4):
            group = get_bit_n_subgroup(h_rects.copy(), n)
            self.play(FadeIn(group, lag_ratio=0.2))
            self.wait(0.5)
            self.play(FadeOut(group))
        self.wait()

        randy = Randolph(height=2)
        randy.next_to(boxes, RIGHT, buff=MED_LARGE_BUFF, aligned_edge=DOWN)
        ne_word = OldTexText("No error?")
        ne_word.next_to(randy, UP, buff=MED_LARGE_BUFF)
        ne_word.shift(0.2 * RIGHT)
        ez_word = OldTexText("or error\\\\at bit 0?")
        ez_word.set_color(RED)
        ez_word.move_to(ne_word, DOWN)

        self.play(
            VFadeIn(randy),
            randy.change, 'pondering', questions,
            FadeOut(braces),
            *[
                FadeOut(brace.words)
                for brace in braces
            ]
        )
        self.play(FadeIn(ne_word, 0.5 * DOWN))
        self.play(Blink(randy))
        self.wait()
        self.play(
            ne_word.next_to, ez_word, UP, MED_LARGE_BUFF,
            FadeIn(ez_word, 0.25 * DOWN),
            randy.change, "confused", target_square,
        )
        self.play(Blink(randy))
        for x in range(2):
            self.play(toggle_bit_anim(block[0]))
        self.play(randy.change, "pondering", questions)

        # Count through again
        for n in [*range(0, 16), 0]:
            target_square.move_to(boxes[n])
            for k, q_rect in enumerate(q_rects):
                index = 3 if((1 << k) & n) else 1
                q_rect.move_to(questions[k][index])
            randy.look_at(target_square)
            self.wait(0.5)

        # Highlight no error
        ne_rect = SurroundingRectangle(ne_word)
        ne_rect.set_stroke(GREY_B, 2)
        ne_comment = OldTexText("17th outcome")
        ne_comment.set_color(GREY_B)
        ne_comment.next_to(ne_rect, UP)

        self.play(
            ShowCreation(ne_rect),
            FadeIn(ne_comment, 0.25 * DOWN),
            randy.change, "maybe", ne_comment,
        )
        for x in range(2):
            self.play(Blink(randy))
            self.wait(2)

        # Nix bit 0
        zero_rect = SurroundingRectangle(boxes[0], buff=0)
        zero_rect.set_fill(BLACK, 1)
        zero_rect.set_stroke(BLACK, 0)
        zero_rect.scale(0.98)

        self.play(
            GrowFromCenter(zero_rect),
            boxes[0].set_stroke, {"width": 0},
            FadeOut(target_square),
            randy.change, "raise_left_hand", zero_rect,
        )
        ne_word.generate_target()
        ne_word.target[0][-1].set_opacity(0)
        ne_word.target.next_to(randy, UP, MED_LARGE_BUFF)
        ne_word.target.set_color(YELLOW)
        self.play(
            MoveToTarget(ne_word),
            LaggedStart(*map(FadeOut, [ne_rect, ne_comment, ez_word]))
        )
        for n in range(4):
            highlight = get_bit_n_subgroup(h_rects.copy(), n)
            one_rects = get_one_rects(get_bit_n_subgroup(block, n))
            self.add(highlight, block, p_labels, zero_rect, one_rects)
            self.wait()
            self.remove(highlight, one_rects)

        # (15, 11) setup
        stat_words = VGroup(
            OldTexText("15", "-bit block"),
            OldTexText("11", " bits of\\\\message", alignment=""),
            OldTexText("4 bits of\\\\redundancy", alignment=""),
        )
        stat_words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        stat_words[0].set_color(YELLOW)
        stat_words[2].set_color(GREEN)
        stat_words.next_to(boxes, RIGHT, buff=MED_LARGE_BUFF, aligned_edge=UP)
        stat_words.shift(0.5 * DOWN)

        self.play(
            LaggedStart(*map(FadeOut, [*q_rects, ne_word])),
            randy.change, "tease", stat_words,
            FadeIn(stat_words[0], 0.5 * LEFT)
        )
        self.play(Blink(randy))
        self.play(
            FadeIn(stat_words[1], 0.5 * LEFT),
            LaggedStart(*[
                toggle_bit_anim(bit)
                for i, bit in enumerate(block)
                if i not in [0, 1, 2, 4, 8]
            ])
        )
        self.play(
            LaggedStart(*[
                toggle_bit_anim(bit)
                for i, bit in enumerate(block)
                if i not in [0, 1, 2, 4, 8]
            ])
        )
        self.wait()
        self.play(
            FadeIn(stat_words[2], 0.5 * LEFT),
            LaggedStart(*map(ShowCreationThenFadeAround, [
                block[2**n]
                for n in range(4)
            ]))
        )
        self.play(Blink(randy))

        code_name = OldTexText("(", "15", ", ", "11", ")", " Hamming code")
        code_name.set_height(0.8)
        code_name.to_edge(UP)
        code_name.shift(UP)

        self.play(
            ApplyMethod(frame.set_height, 9, {"about_edge": DOWN}, run_time=2),
            TransformFromCopy(stat_words[0][0], code_name[1]),
            TransformFromCopy(stat_words[1][0], code_name[3]),
            LaggedStart(*map(FadeIn, [
                code_name[i] for i in [0, 2, 4, 5]
            ])),
        )
        self.wait()

        # Bring back bit zero
        self.play(
            LaggedStart(*map(FadeOut, [
                *stat_words, randy,
                *questions, code_name,
            ])),
            ApplyMethod(frame.match_x, block),
            run_time=2
        )

        old_zero_rect = zero_rect
        zero_rect = old_zero_rect.copy()
        zero_rect.set_stroke(YELLOW, 2)
        zero_rect.set_fill(YELLOW, 0.5)
        zero_rect.save_state()
        zero_rect.stretch(0, 1, about_edge=UP)
        zero_words = OldTexText("Can we put this bit to work?")
        zero_words.set_height(0.7)
        zero_words.next_to(zero_rect, UP, MED_LARGE_BUFF)
        zero_words.match_x(block)
        zero_words.set_color(YELLOW)

        self.add(zero_rect, block, p_labels)
        block[0].set_opacity(0)
        self.play(
            FadeOut(old_zero_rect),
            Restore(zero_rect),
            Write(zero_words)
        )
        self.wait()

        # Parity check the whole block
        pc_words = OldTexText("Parity check\\\\ \\emph{the whole block}")
        pc_words.set_height(1.2)
        pc_words.next_to(boxes, LEFT, buff=MED_LARGE_BUFF)

        one_rects = get_one_rects(block)
        counter = get_ones_counter(boxes[-2:], one_rects)
        counter.scale(0.5)

        self.play(
            Write(pc_words, run_time=1),
            ShowCreationThenFadeOut(h_rects.copy()),
        )
        self.wait()
        ecc_bits = VGroup(*[block[2**n] for n in range(4)])
        for x in range(2):
            self.play(LaggedStartMap(toggle_bit_anim, ecc_bits, lag_ratio=0.25, run_time=1))
        self.wait()

        self.add(counter)
        self.play(ShowIncreasingSubsets(one_rects))
        self.wait()
        block[0][1].set_opacity(1)
        self.play(Write(block[0]))
        one_rects.set_submobjects(get_one_rects(block))
        self.wait()
        self.play(*map(FadeOut, [one_rects, counter]))

        # Walk through single and two bit errors
        self.play(
            zap_anim(block[9]),
            toggle_bit_anim(block[9], target_color=RED),
        )
        one_rects.set_submobjects(get_one_rects(block))
        counter.set_opacity(1)
        self.add(counter)
        self.play(ShowIncreasingSubsets(one_rects))
        self.wait()

        self.play(
            zap_anim(block[5]),
            toggle_bit_anim(block[5], target_color=RED),
        )
        one_rects.set_submobjects(get_one_rects(block))
        self.wait()
        self.play(FadeOut(one_rects), FadeOut(counter))

        for n in [2, 3]:
            group = get_bit_n_subgroup(h_rects.copy(), n)
            group.set_fill(opacity=0)
            group.set_stroke(BLUE, 10)
            self.play(ShowCreation(group, lag_ratio=0.5))
            self.play(FadeOut(group))
        self.wait()

        scanim = scan_anim(boxes.get_corner(DR) + 2 * UR, block, lag_factor=0.5, run_time=2)
        robot = scanim.mobject[-1]
        robot.set_color(GREY_B)
        robot.scale(2, about_edge=UP)
        ded_words = OldTexText("At least\\\\2 errors!")
        ded_words.set_color(RED)
        ded_words.next_to(robot, UR, buff=SMALL_BUFF)

        self.play(scanim)
        self.play(FadeIn(ded_words, 0.5 * DOWN))
        self.wait()

        # Extended name
        new_title = OldTexText("Extended Hamming Code")
        new_title.replace(zero_words, dim_to_match=1)
        self.play(
            FadeIn(new_title, DOWN),
            FadeOut(zero_words, UP),
            FadeOut(pc_words),
        )
        self.wait()
