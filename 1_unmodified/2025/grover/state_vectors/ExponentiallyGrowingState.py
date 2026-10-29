# ==============================================================================
# Scene:      ExponentiallyGrowingState
# Source:     videos/_2025/grover/state_vectors.py (lines 1931-2010)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExponentiallyGrowingState.py ExponentiallyGrowingState -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BitString(VGroup):
    def __init__(self, value, length=4, buff=SMALL_BUFF):
        self.length = length
        bit_mob = Integer(0)
        super().__init__(bit_mob.copy() for n in range(length))
        self.arrange(RIGHT, buff=buff)
        self.set_value(value)

    def set_value(self, value):
        bits = bin(value)[2:].zfill(self.length)
        for mob, bit in zip(self, bits):
            mob.set_value(int(bit))


class ExponentiallyGrowingState(InteractiveScene):
    def construct(self):
        # Initialize vector
        label = TexText(R"State of a\\ 1 qubit computer")
        n_label = label.make_number_changeable("1", edge_to_fix=RIGHT)
        n_label.set_color(YELLOW)
        label.move_to(3.5 * LEFT)
        vect = self.get_state_vector(1)
        vect.move_to(1.5 * RIGHT)

        brace = self.get_brace_group(vect, 1)
        brace.set_opacity(0)

        self.add(label)
        self.add(vect)

        # Grow the vector
        for n in range(2, 9):
            new_vect = self.get_state_vector(n)
            new_vect.move_to(vect)
            new_brace = self.get_brace_group(new_vect, n)

            n_label.set_value(n)
            self.play(
                ReplacementTransform(vect[0], new_vect[0]),
                FadeTransform(vect[1], new_vect[1]),
                FadeTransformPieces(vect[2], new_vect[2]),
                FadeTransform(brace[0], new_brace[0]),
                FadeTransform(brace[1], new_brace[1]),
            )
            self.wait()

            vect = new_vect
            brace = new_brace

        # Change to 100
        frame = self.frame

        new_brace_label = Tex(R"2^{100}")
        new_brace_label.set_color(YELLOW)
        new_brace_label.next_to(brace[0], RIGHT).shift(SMALL_BUFF * UR)

        top_eq = Tex(R"2^{100} = " + "{:,}".format(2**100))
        top_eq.next_to(vect, UP, MED_LARGE_BUFF).set_x(0)

        self.play(
            FadeTransform(brace[1], new_brace_label),
            ChangeDecimalToValue(n_label, 100),
            frame.animate.set_height(9, about_edge=DOWN),
            FadeIn(top_eq),
            FadeTransform(vect, self.get_state_vector(n + 2).move_to(vect, RIGHT)),
        )
        self.wait()

    def get_state_vector(self, n):
        # Actualy function
        values = normalize(np.random.uniform(-1, 1, 2**n))
        array = DecimalMatrix(
            values.reshape((2**n, 1)),
            decimal_config=dict(include_sign=True)
        )
        array.set_max_height(7)

        bit_strings = VGroup(
            BitString(k, length=n)
            for k in range(2**n)
        )
        bit_strings.set_color(GREY)
        for bits, entry in zip(bit_strings, array.get_entries()):
            bits.set_max_height(entry.get_height())
            bits.next_to(array, LEFT, buff=0.2)
            bits.match_y(entry)

        return VGroup(bit_strings, array.get_brackets(), array.get_entries())

    def get_brace_group(self, vect, n):
        brace = Brace(vect, RIGHT, buff=0.25)
        label = brace.get_tex(Rf"2^{{{n}}} = {2**n}")
        label.shift(SMALL_BUFF * UR)
        return VGroup(brace, label)
