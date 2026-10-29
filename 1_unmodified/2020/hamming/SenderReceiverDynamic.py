# ==============================================================================
# Scene:      SenderReceiverDynamic
# Source:     videos/_2020/hamming.py (lines 1791-1960)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SenderReceiverDynamic.py SenderReceiverDynamic -w -m --fps 15
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


class SenderReceiverDynamic(PiCreatureScene):
    def construct(self):
        # Sender and receiver
        sender_word = OldTexText("Sender")
        receiver_word = OldTexText("Receiver")
        words = VGroup(sender_word, receiver_word)
        words.scale(1.5)
        words.set_y(-2)
        sender_word.to_edge(LEFT)
        receiver_word.to_edge(RIGHT)

        sender, receiver = pis = self.pi_creatures
        for pi, word in zip(pis, words):
            pi.set_height(2)
            pi.next_to(word, UP)

        self.clear()
        for pi in pis:
            self.play(
                VFadeIn(pi),
                pi.change, "pondering", ORIGIN,
            )
        for word in words:
            self.play(Write(word, run_time=1))
        self.wait()

        # Message
        block = get_bit_grid(4, 4)
        block.set_height(1.5)
        block.next_to(pis[0].get_corner(UR), UR)

        self.play(
            sender.change, "raise_right_hand",
            FadeIn(block, DOWN, lag_ratio=0.01),
        )
        self.add(sender, block)
        block.save_state()
        self.play(
            block.move_to, sender,
            block.scale, 0.5,
            sender.change, "gracious", sender,
        )
        self.play(LaggedStart(
            ApplyMethod(block[1].set_color, GREEN),
            toggle_bit_anim(block[2], target_color=GREEN),
            ApplyMethod(block[4].set_color, GREEN),
            toggle_bit_anim(block[8], target_color=GREEN),
        ))
        self.wait()
        block.generate_target()
        block.target.scale(2)
        block.target.next_to(receiver, UL)
        self.play(
            MoveToTarget(block, run_time=3, path_arc=-30 * DEGREES),
            receiver.change, "tease", receiver.get_corner(UL) + UP,
            sender.change, "happy", receiver.get_corner(UL) + UP,
        )
        self.play(scan_anim(receiver.get_corner(UL), block, lag_factor=1, show_robot=False))
        self.wait()

        # Replace with machines
        underlines = VGroup(*[Underline(word) for word in words])
        underlines.set_color(YELLOW)
        servers = VGroup(*[SVGMobject("server_stack") for x in range(2)])
        servers.set_color(GREY)
        servers.set_stroke(BLACK, 2)
        servers.set_gloss(0.5)
        for server, pi in zip(servers, pis):
            server.move_to(pi)

        self.play(
            LaggedStartMap(ShowCreationThenFadeOut, underlines, lag_ratio=0.7),
            *[
                ApplyMethod(pi.change, "thinking", pi)
                for pi in pis
            ],
        )
        self.wait()
        self.play(
            *it.chain(*[
                [
                    pi.change, "horrified",
                    pi.shift, 2 * UP,
                    pi.set_opacity, 0
                ]
                for pi in pis
            ]),
            FadeIn(servers, 2 * DOWN)
        )
        self.remove(pis)

        bits_copy = block.copy()
        bits_copy.arrange(RIGHT, buff=SMALL_BUFF)
        bits_copy.set_width(0.7 * servers[1].get_width())
        bits_copy.move_to(servers[1], LEFT)
        bits_copy.shift(SMALL_BUFF * RIGHT)
        self.play(
            LaggedStart(*[
                TransformFromCopy(b1, b2)
                for b1, b2 in zip(block, bits_copy)
            ], run_time=3),
        )

        # Sent and received
        sent_block = block.copy()
        sent_block.next_to(servers[0], UR)
        sent_block.match_y(block)
        wire = VGroup(
            SurroundingRectangle(sent_block),
            Line(sent_block.get_right(), block.get_left(), buff=SMALL_BUFF / 2),
            SurroundingRectangle(block),
        )
        wire.set_stroke(GREY, 2)
        noise_word = OldTexText("Potential noise")
        noise_word.scale(0.75)
        noise_word.set_color(RED)
        noise_word.next_to(wire[1], UP, SMALL_BUFF)

        small_words = VGroup(
            OldTexText("sent"),
            OldTexText("received"),
        )
        for word, mob in zip(small_words, [sent_block, block]):
            word.next_to(mob, UP, buff=0.35)

        self.play(
            ShowCreation(wire[0]),
            FadeIn(small_words[0], 0.5 * DOWN),
            FadeIn(sent_block),
        )
        self.play(
            Transform(sent_block.copy(), block, remover=True, lag_ratio=0.01),
            ShowCreation(wire[1]),
            FadeIn(noise_word, lag_ratio=0.1)
        )
        self.play(
            ShowCreation(wire[2]),
            FadeIn(small_words[1], 0.5 * DOWN)
        )

        # Past and future
        cross_lines = VGroup(*[
            Line(
                word.get_left(), word.get_right(),
                stroke_width=5,
                stroke_color=RED,
            )
            for word in words
        ])
        time_words = VGroup(
            OldTexText("Past"),
            OldTexText("Future"),
        )
        time_words.set_color(BLUE)
        for w1, w2 in zip(words, time_words):
            w2.match_height(w1)
            w2.next_to(w1, DOWN)

        self.play(
            LaggedStartMap(ShowCreation, cross_lines, lag_ratio=0.7),
            LaggedStartMap(ApplyMethod, words, lambda m: (m.set_opacity, 0.75), lag_ratio=0.7),
            run_time=1,
        )
        self.play(
            LaggedStartMap(FadeIn, time_words, lambda m: (m, UP), lag_ratio=0.3)
        )
        self.wait(2)

    def create_pi_creatures(self):
        return VGroup(Randolph(), Mortimer())
