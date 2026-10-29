# ==============================================================================
# Scene:      TripleRedundancy
# Source:     videos/_2020/hamming.py (lines 592-958)
# Category:   1 · Renders unmodified
# Includes code copied from: _2020/chess.py
#
# Run from this folder:
#     manimgl TripleRedundancy.py TripleRedundancy -w -m --fps 15
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


def get_sound_wave():
    sound = VGroup(*[
        Line(DOWN, UP).set_height(
            (0.3 + 0.8 * random.random()) * abs(np.sin(x))
        )
        for x in np.linspace(0, 3 * PI, 100)
    ])
    sound.arrange(RIGHT, buff=0.05)
    return sound


# Special animations
def image_reveal_animation(image, bit_height=0.1):
    box = SurroundingRectangle(image)
    box.set_fill(BLACK, 1)
    box.set_stroke(width=0)
    bits = get_image_bits(image, bit_height=bit_height)

    return AnimationGroup(
        Animation(image),
        ApplyMethod(
            box.stretch, 0, 1, {"about_edge": DOWN}, remover=True,
            rate_func=linear,
        ),
        LaggedStartMap(
            VFadeInThenOut, bits,
            run_time=1,
            lag_ratio=3 / len(bits)
        )
    )


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


class TripleRedundancy(Scene):
    def construct(self):
        # Show different file types
        image = ImageMobject("Claude_Shannon")
        image.set_height(6)
        image.to_edge(DOWN)
        video = ImageMobject("ZoeyInGrass")
        video.set_opacity(0)
        sound = get_sound_wave()
        text = OldTexText(
            """
            Fourscore and seven years ago\\\\
            our fathers brought forth, on this\\\\
            continent, a new nation, conceived\\\\
            in liberty, and dedicated to the\\\\
            proposition that all men are created\\\\
            equal. Now we are engaged$\\dots$
            """,
            alignment=""
        )
        code = ImageMobject("Hamming_Code_Snippet")
        files = Group(video, sound, text, code, image)
        for file in files:
            file.match_width(image)
            file.move_to(image, UP)

        brace = Brace(image, UP)
        file_word = OldTexText("Original File")
        file_word.set_height(0.5)
        file_word.next_to(brace, UP)

        self.play(
            GrowFromCenter(brace),
            FadeIn(file_word),
            image_reveal_animation(video),
        )
        video.set_opacity(0)
        self.wait(2)
        for f1, f2 in zip(files, files[1:]):
            self.play(FadeOut(f1), FadeIn(f2))
            self.wait()

        # Show bits
        bits = get_image_bits(image)
        for bit, value in zip(bits, string_to_bits(";)Hi")):
            bit[1 - value].set_opacity(0)
            bit[value].set_opacity(1)
        bits.generate_target()
        bits.target.arrange(RIGHT)
        bits.target.set_height(0.5)
        bits.target.arrange(RIGHT, buff=SMALL_BUFF)
        bits.target.to_edge(LEFT)
        bits.target.shift(UP)
        last_shown_bit_index = 31
        dots = OldTexText("\\dots")
        dots.next_to(bits.target[last_shown_bit_index], RIGHT, aligned_edge=DOWN, buff=SMALL_BUFF)
        new_brace = Brace(VGroup(bits.target[0], dots), UP)
        file_rect = SurroundingRectangle(VGroup(bits.target[0], dots))
        file_rect.set_stroke(BLUE, 4)

        self.play(
            FadeOut(image),
            FadeIn(bits, lag_ratio=1 / len(bits))
        )
        self.play(
            MoveToTarget(bits),
            Transform(brace, new_brace),
            file_word.next_to, new_brace, UP, SMALL_BUFF,
            run_time=3,
        )
        self.play(
            FadeOut(bits[last_shown_bit_index + 1:last_shown_bit_index + 5]),
            FadeIn(dots),
            FadeOut(brace),
            FadeIn(file_rect),
            file_word.next_to, file_rect, UP,
        )
        self.remove(*bits[last_shown_bit_index + 1:])
        bits.remove(*bits[last_shown_bit_index + 1:])
        self.add(bits)
        self.wait()

        # Show redundant copies
        bits.add(dots)
        copies = VGroup(bits.copy(), bits.copy())
        copies.arrange(DOWN, buff=MED_SMALL_BUFF)
        copies.next_to(bits, DOWN, buff=MED_SMALL_BUFF)
        copies.set_color(BLUE)
        copies_rect = SurroundingRectangle(copies, buff=SMALL_BUFF)
        copies_rect.set_stroke(BLUE_E, 4)
        copies_word = OldTexText("Redundant copies")
        copies_word.scale(file_word[0][0].get_height() / copies_word[0][0].get_height())
        copies_word.match_color(copies)
        copies_word.next_to(copies_rect, DOWN)

        self.play(LaggedStart(*[
            TransformFromCopy(bits, bits_copy)
            for bits_copy in copies
        ], lag_ratio=0.5))
        self.play(
            ShowCreation(copies_rect),
            FadeIn(copies_word, UP),
            copies.set_color, WHITE,
        )
        self.wait()

        # Show a correction
        flipper_index = 7
        flipper = bits[flipper_index]
        self.play(
            zap_anim(flipper),
            toggle_bit_anim(flipper),
        )
        self.play()
        self.wait()

        bit_groups = [bits, *copies]
        scan_rect = SurroundingRectangle(
            VGroup(*[group[0] for group in bit_groups])
        )
        scan_rect.set_stroke(GREEN, 5)

        self.add(scan_rect)
        for i in range(flipper_index + 1):
            self.play(
                scan_rect.match_x, bits[i],
                run_time=0.25
            )
            self.wait(0.25)

        bangs = OldTexText("!!!")[0]
        bangs.scale(1.5)
        bangs.set_color(RED)
        bangs.next_to(scan_rect, UP)

        self.play(
            LaggedStartMap(
                FadeIn, bangs,
                lambda m: (m, DOWN),
                run_time=1,
            ),
            scan_rect.set_color, RED
        )
        self.wait()

        flipper_rect = SurroundingRectangle(flipper, buff=SMALL_BUFF)
        flipper_rect.set_stroke(GREEN, 4)
        flipper_rect.set_fill(GREEN, 0.5)
        self.play(
            ReplacementTransform(bangs, flipper_rect)
        )
        self.play(
            toggle_bit_anim(flipper),
            FadeOut(flipper_rect),
            scan_rect.set_color, GREEN,
        )

        for i in range(flipper_index + 1, flipper_index + 5):
            self.play(
                scan_rect.match_x, bits[i],
                run_time=0.25
            )
            self.wait(0.25)
        self.play(FadeOut(scan_rect, 0.2 * RIGHT, run_time=0.5))

        # Show 2/3 of transmission block
        rects = VGroup(file_rect, copies_rect)
        rects.generate_target()
        for rect, width in zip(rects.target, [1, 2]):
            rect.set_width(width, stretch=True)
            rect.set_height(0.75, stretch=True)
            rect.set_fill(rect.get_stroke_color(), opacity=1)
        rects.target[0].set_color(BLUE)
        rects.target[1].set_color(BLUE_E)
        rects.target.set_stroke(width=0)
        rects.target.arrange(RIGHT, buff=0)
        rects.target.set_width(12, stretch=True)
        rects.target.move_to(UP)

        braces = VGroup(*[Brace(rect, UP, buff=SMALL_BUFF) for rect in rects.target])

        frac_labels = VGroup(*[
            DecimalNumber(100 * frac, unit="\\%", num_decimal_places=1)
            for frac in [1 / 3, 2 / 3]
        ])
        for rect, label in zip(rects.target, frac_labels):
            label.move_to(rect)

        redundancy_word = OldTexText("Redundancy")
        redundancy_word.match_height(copies_word)
        redundancy_word.match_color(copies_word)
        redundancy_word.next_to(braces[1], UP, SMALL_BUFF)

        self.play(
            bits.replace, rects.target[0], {"stretch": True},
            bits.set_opacity, 0,
            copies.replace, rects.target[1], {"stretch": True},
            copies.set_opacity, 0,
            MoveToTarget(rects),
            LaggedStartMap(GrowFromCenter, braces),
            file_word.next_to, braces[0], UP, SMALL_BUFF,
            ReplacementTransform(copies_word, redundancy_word),
            run_time=2,
        )
        self.play(Write(frac_labels))
        self.wait()

        # Show failure for some two-bit errors
        bits = get_bit_grid(3, 1, [0, 0, 0], height=3, buff=SMALL_BUFF)
        bits.next_to(rects, DOWN, buff=MED_LARGE_BUFF)

        self.play(FadeIn(bits))
        self.play(
            LaggedStart(zap_anim(bits[0]), zap_anim(bits[2]), lag_ratio=0.5),
            LaggedStart(toggle_bit_anim(bits[0]), toggle_bit_anim(bits[2]), lag_ratio=0.5),
            run_time=1.5,
        )
        self.wait()
        self.play(FadeOut(bits))

        # Shrink bars
        rects.generate_target()
        p = 9 / 256
        rects.target[0].set_width(1 - p, stretch=True)
        rects.target[1].set_width(p, stretch=True)
        rects.target.arrange(RIGHT, buff=0)
        rects.target.match_width(rects, stretch=True)
        rects.target.move_to(rects)

        braces.generate_target()
        for rect, brace in zip(rects.target, braces.target):
            brace.become(Brace(rect, UP, buff=SMALL_BUFF, min_num_quads=1))

        f_always(frac_labels[0].move_to, rects[0].get_center)
        f_always(frac_labels[1].move_to, rects[1].get_center)
        rl_width = frac_labels[1].get_width()
        f_always(frac_labels[1].set_width, lambda: min(0.95 * rects[1].get_width(), rl_width))

        self.play(
            MoveToTarget(rects),
            MoveToTarget(braces),
            ChangeDecimalToValue(frac_labels[0], 100 * (1 - p)),
            ChangeDecimalToValue(frac_labels[1], 100 * p),
            file_word.next_to, braces.target[0], UP, SMALL_BUFF,
            redundancy_word.next_to, braces.target[1], UP, SMALL_BUFF,
            redundancy_word.to_edge, RIGHT,
            run_time=3,
        )
        self.wait()

        ratio_group = VGroup(rects, braces, frac_labels, file_word, redundancy_word)
        ratio_group.clear_updaters()

        # Show space division for a (256, 247) Hamming code
        bits = get_bit_grid(
            16, 16,
            bits=string_to_bits("There are 10 kinds of people...."),
            buff=0.2, height=5
        )
        bits.to_edge(DOWN, buff=MED_SMALL_BUFF)
        bits.shift(2 * LEFT)
        ecc_bits = bits[-9:]
        ecc_rect = SurroundingRectangle(ecc_bits, buff=0.05)
        ecc_rect.set_stroke(BLUE_E, 2)
        ecc_rect.set_fill(BLUE_E, 0.5)

        block_label = OldTexText("256 bit block")
        ecc_label = OldTexText("9 redundancy bits")
        message_label = OldTexText("247 message bits")

        block_label.next_to(bits, RIGHT, LARGE_BUFF)
        block_label.shift(UP)
        ecc_label.next_to(ecc_bits, RIGHT, LARGE_BUFF)
        ecc_label.to_edge(DOWN, buff=MED_SMALL_BUFF)
        ecc_label.set_color(BLUE)
        message_label.move_to(VGroup(block_label, ecc_label))
        message_label.align_to(block_label, LEFT)
        message_label.set_color(YELLOW)

        self.play(
            ratio_group.to_edge, UP,
            LaggedStartMap(FadeIn, bits, lag_ratio=1 / len(bits)),
            Write(block_label),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                SurroundingRectangle(bits, color=BLUE, stroke_opacity=0),
                ecc_rect
            ),
            Write(ecc_label)
        )
        self.wait()
        self.play(
            LaggedStartMap(
                VFadeInThenOut,
                bits[:-9].copy().set_fill(color=YELLOW),
                lag_ratio=0.1 / len(bits),
                run_time=3,
            ),
            Write(message_label),
        )
        self.wait()

        # Show correction
        flipper = random.choice(bits)

        self.play(
            zap_anim(flipper),
            toggle_bit_anim(flipper),
        )
        self.play(flipper.set_color, RED)

        point = bits.get_corner(DL) + 1.5 * LEFT + UP
        scanim = scan_anim(point, bits, final_stroke_width=0.2)
        lines, robot = scanim.mobject

        self.play(scanim)
        self.play(*[
            Succession(
                ApplyMethod(line.put_start_and_end_on, point, flipper.get_center()),
                ApplyMethod(line.set_stroke, None, 1)
            )
            for line in lines
        ])
        self.play(
            toggle_bit_anim(flipper),
            FadeOut(lines),
            FadeOut(robot),
        )
        self.play(flipper.set_color, WHITE)

        # Show two errors
        two_error_label = OldTexText("Two errors")
        two_error_label.next_to(bits, LEFT, buff=MED_LARGE_BUFF, aligned_edge=UP)
        two_error_label.set_color(RED)

        flippers = VGroup(*random.sample(list(bits), 2))

        self.play(
            FadeIn(two_error_label),
            LaggedStart(*[zap_anim(f) for f in flippers], lag_ratio=0.5),
            LaggedStartMap(toggle_bit_anim, flippers, lag_ratio=0.5),
        )
        self.play(flippers.set_color, RED)
        self.wait()

        scanim = scan_anim(point, bits, final_stroke_width=0.2)
        bangs = OldTexText("!!!")[0]
        bangs.set_color(RED)
        bangs.next_to(point, UL, SMALL_BUFF)
        q_marks = OldTexText("???")[0]
        q_marks.replace(bangs, dim_to_match=1)
        q_marks.match_style(bangs)

        self.play(scanim)
        self.play(
            LaggedStartMap(
                FadeIn, bangs,
                lambda m: (m, 0.25 * DOWN),
                lag_ratio=0.2,
                run_time=1,
            ),
        )
        self.wait()
        self.play(ReplacementTransform(bangs, q_marks, lag_ratio=0.2))
        self.wait()
