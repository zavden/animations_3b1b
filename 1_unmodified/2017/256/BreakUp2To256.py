# ==============================================================================
# Scene:      BreakUp2To256
# Source:     videos/_2017/256.py (lines 30-179)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/crypto.py
#
# Run from this folder:
#     manimgl BreakUp2To256.py BreakUp2To256 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/crypto.py -----

def bit_string_to_mobject(bit_string):
    line = OldTex("0"*32)
    pre_result = VGroup(*[
        line.copy() for row in range(8)
    ])
    pre_result.arrange(DOWN, buff = SMALL_BUFF)
    result = VGroup(*it.chain(*pre_result))
    result.scale(0.7)
    bit_string = (256 - len(bit_string))*"0" + bit_string

    for i, (bit, part) in enumerate(zip(bit_string, result)):
        if bit == "1":
            one = OldTex("1")[0]
            one.replace(part, dim_to_match = 1)
            result.submobjects[i] = one

    return result



# ----- From _2017/256.py -----

class BreakUp2To256(PiCreatureScene):
    def construct(self):
        self.initialize_bits()
        self.add_number()
        self.break_up_as_powers_of_two()
        self.break_up_as_four_billions()
        self.reorganize_four_billions()

    def initialize_bits(self):
        bits = bit_string_to_mobject("")
        bits.to_corner(UP+LEFT)
        one = OldTex("1")[0]
        one.replace(bits[0], dim_to_match = 1)
        self.add(bits)
        self.add_foreground_mobject(VGroup(*bits[-15:]))
        self.number = 0
        self.bits = bits
        self.one = one
        self.zero = bits[0].copy()

    def add_number(self):
        brace = Brace(self.bits, RIGHT)

        number, possibilities = expression = OldTexText(
            "$2^{256}$", "possibilities"
        )
        number.set_color(YELLOW)
        expression.next_to(brace, RIGHT)

        words = OldTexText("Seems big...I guess...")
        words.next_to(self.pi_creature.get_corner(UP+LEFT), UP)

        self.play(
            self.pi_creature.change, "raise_right_hand",
            GrowFromCenter(brace),
            Write(expression, run_time = 1)
        )
        self.wait()
        self.play(
            self.pi_creature.change, "maybe",
            Write(words)
        )
        self.wait(2)
        self.play(
            self.pi_creature.change, "happy",
            FadeOut(words)
        )
        self.wait()

        self.expression = expression
        self.bits_brace = brace

    def break_up_as_powers_of_two(self):
        bits = self.bits
        bits.generate_target()
        subgroups = [
            VGroup(*bits.target[32*i:32*(i+1)])
            for i in range(8)
        ]
        subexpressions = VGroup()
        for i, subgroup in enumerate(subgroups):
            subgroup.shift(i*MED_LARGE_BUFF*DOWN)
            subexpression = OldTexText(
                "$2^{32}$", "possibilities"
            )
            subexpression[0].set_color(GREEN)
            subexpression.next_to(subgroup, RIGHT)
            subexpressions.add(subexpression)

        self.play(
            FadeOut(self.bits_brace),
            ReplacementTransform(
                VGroup(self.expression),
                subexpressions
            ),
            MoveToTarget(bits)
        )
        self.play(self.pi_creature.change, "pondering")
        self.wait()


        self.subexpressions = subexpressions

    def break_up_as_four_billions(self):
        new_subexpressions = VGroup()
        for subexpression in self.subexpressions:
            new_subexpression = OldTexText(
                "4 Billion", "possibilities"
            )
            new_subexpression[0].set_color(YELLOW)
            new_subexpression.move_to(subexpression, LEFT)
            new_subexpressions.add(new_subexpression)

        self.play(
            Transform(
                self.subexpressions, new_subexpressions,
                run_time = 2,
                lag_ratio = 0.5,
            ),
            FadeOut(self.pi_creature)
        )
        self.wait(3)

    def reorganize_four_billions(self):
        target = VGroup(*[
            OldTexText(
                "$\\big($", "4 Billion", "$\\big)$",
                arg_separator = ""
            )
            for x in range(8)
        ])
        target.arrange(RIGHT, buff = SMALL_BUFF)
        target.to_edge(UP)
        target.set_width(FRAME_WIDTH - LARGE_BUFF)
        parens = VGroup(*it.chain(*[
            [t[0], t[2]] for t in target
        ]))
        target_four_billions = VGroup(*[t[1] for t in target])
        target_four_billions.set_color(YELLOW)
        four_billions, to_fade = [
            VGroup(*[se[i] for se in self.subexpressions])
            for i in range(2)
        ]

        self.play(
            self.bits.to_corner, DOWN+LEFT,
            Transform(four_billions, target_four_billions),
            LaggedStartMap(FadeIn, parens),
            FadeOut(to_fade)
        )
        self.wait()

    ######

    def wait(self, time = 1):
        self.play(Animation(self.bits, run_time = time))

    def update_frame(self, *args, **kwargs):
        self.number += 1
        new_bit_string = bin(self.number)[2:]
        for i, bit in enumerate(reversed(new_bit_string)):
            index = -i-1
            bit_mob = self.bits[index]
            if bit == "0":
                new_mob = self.zero.copy()
            else:
                new_mob = self.one.copy()
            new_mob.replace(bit_mob, dim_to_match = 1)
            Transform(bit_mob, new_mob).update(1)
        Scene.update_frame(self, *args, **kwargs)
