# ==============================================================================
# Scene:      DiskOfBits
# Source:     videos/_2020/hamming.py (lines 419-589)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiskOfBits.py DiskOfBits -w -m --fps 15
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


class DiskOfBits(Scene):
    def construct(self):
        # Setup disc
        bits = get_bit_grid(2**5, 2**6, height=6)

        inner_r = 1
        outer_r = 3
        annulus = Annulus(
            inner_radius=inner_r * 0.93,
            outer_radius=outer_r * 1.02,
            fill_color=GREY_D,
        )
        annulus.set_gloss(0.5)

        for bit in bits:
            point = bit.get_center()
            norm = get_norm(point)
            to_inner = inner_r - norm
            to_outer = norm - outer_r
            sdf = 10 * max(to_inner, to_outer)
            if 0 < sdf < 0.5:
                bit.scale(1 - sdf)
            elif sdf > 0:
                bits.remove(bit)

        disc = VGroup(annulus, bits)

        # Setup scratch
        scratch_line = Line(disc.get_top(), disc.get_right())
        scratch_line.set_stroke(RED, width=2, opacity=0.75)

        flipped_bits = VGroup()
        for bit in bits:
            point = bit.get_center()
            norm = abs(point[0] + point[1] - 3)
            alpha = 1 - clip(norm / 0.2, 0, 1)
            if alpha > 0.25:
                bit.generate_target()
                bit.target.set_stroke(width=1)
                bit.target.set_color(RED)
                flipped_bits.add(bit)

        # Add disc
        light = self.camera.light_source
        light.move_to([0, -10, 10])

        random_bits = bits.copy()
        random_bits.sort(lambda p: -get_norm(p))
        self.add(annulus)
        self.play(
            LaggedStartMap(FadeIn, random_bits, lag_ratio=10 / len(bits)),
            light.move_to, [-10, 10, 10],
            run_time=1,
        )
        self.clear()
        self.add(disc)

        # Show scratch
        self.play(
            LaggedStartMap(MoveToTarget, flipped_bits),
            ShowCreationThenDestruction(scratch_line),
            run_time=2,
        )

        # Flip 'em'
        self.play(LaggedStartMap(toggle_bit_anim, flipped_bits))
        self.wait()

        # Show image in and image out
        disc.generate_target()
        disc.target.scale(0.5)

        in_image = ImageMobject("Mona_Lisa")
        in_image.to_edge(LEFT)
        in_image.shift(UP)
        in_words = OldTexText("What was\\\\encoded")
        in_words.next_to(in_image, DOWN)
        out_image = in_image.copy()
        out_image.to_edge(RIGHT)
        out_words = OldTexText("What is\\\\decoded")
        out_words.next_to(out_image, DOWN)

        in_arrow = Arrow(
            in_image.get_right(),
            disc.target.get_left() + 0.2 * UP,
            buff=MED_SMALL_BUFF,
        )
        out_arrow = Arrow(
            disc.target.get_right() + 0.2 * UP,
            out_image.get_left(),
            buff=MED_SMALL_BUFF,
        )
        for arrow in in_arrow, out_arrow:
            arrow.set_fill(GREY_B)

        self.play(
            MoveToTarget(disc),
            GrowArrow(out_arrow),
        )

        in_bits = get_bit_grid(40, 33)
        in_bits.replace(in_image, stretch=True)
        in_bits.set_fill(GREY_B)
        out_bits = in_bits.copy()
        out_bits.move_to(out_image)

        out_image_blocker = SurroundingRectangle(out_image)
        out_image_blocker.set_fill(BLACK, 1)
        out_image_blocker.set_stroke(width=0)

        self.add(out_image, out_image_blocker, out_bits, out_words)
        self.play(
            LaggedStart(
                *[
                    Succession(
                        GrowFromPoint(
                            out_bit,
                            random.choice(bits).get_center(),
                        ),
                        FadeOut(out_bit),
                    )
                    for out_bit in out_bits
                ],
                lag_ratio=3 / len(out_bits),
                run_time=12,
            ),
            ApplyMethod(
                out_image_blocker.stretch, 0, 1, {"about_edge": DOWN},
                run_time=12,
                rate_func=bezier([0, 0, 1, 1]),
            ),
            FadeIn(out_words, UP),
        )
        self.wait()
        self.play(
            TransformFromCopy(out_image, in_image),
            ReplacementTransform(
                in_words.copy().replace(out_words).set_opacity(0),
                in_words,
            ),
        )
        self.play(
            LaggedStart(
                *[
                    Succession(
                        FadeIn(in_bit),
                        Transform(in_bit, random.choice(bits)),
                        FadeOut(in_bit),
                    )
                    for in_bit in in_bits
                ],
                lag_ratio=3 / len(in_bits),
                run_time=12,
            ),
            GrowArrow(in_arrow),
        )
        self.wait()

        # Pi Creature
        randy = Randolph()
        randy.set_height(1.5)
        randy.to_edge(DOWN)
        randy.shift(2 * LEFT)

        self.play(FadeIn(randy))
        self.play(randy.change, "maybe")
        self.play(Blink(randy))
        self.play(randy.change, "confused")
        self.wait(2)
        self.play(Blink(randy))
        self.wait()
