# ==============================================================================
# Scene:      IntroduceQuaternions
# Source:     videos/_2018/quaternions.py (lines 4157-4333)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceQuaternions.py IntroduceQuaternions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceQuaternions(Scene):
    def construct(self):
        self.compare_three_number_systems()
        self.mention_four_perpendicular_axes()
        self.bring_back_complex()
        self.show_components_of_quaternion()

    def compare_three_number_systems(self):
        numbers = self.get_example_numbers()
        labels = VGroup(
            OldTexText("Complex number"),
            OldTexText("Not-actually-a-number-system 3d number"),
            OldTexText("Quaternion"),
        )

        for number, label in zip(numbers, labels):
            label.next_to(number, UP, aligned_edge=LEFT)

            self.play(
                FadeInFromDown(number),
                Write(label),
            )
            self.play(ShowCreationThenFadeAround(
                number[2:],
                surrounding_rectangle_config={"color": BLUE}
            ))
            self.wait()

        shift_size = FRAME_HEIGHT / 2 - labels[2].get_top()[1] - MED_LARGE_BUFF
        self.play(
            numbers.shift, shift_size * UP,
            labels.shift, shift_size * UP,
        )

        self.numbers = numbers
        self.labels = labels

    def mention_four_perpendicular_axes(self):
        number = self.numbers[2]
        three_axes = VGroup(*[
            self.get_simple_axes(label, color)
            for label, color in zip(
                ["i", "j", "k"],
                [GREEN, RED, BLUE],
            )
        ])
        three_axes.arrange(RIGHT, buff=LARGE_BUFF)
        three_axes.next_to(number, DOWN, LARGE_BUFF)

        self.play(LaggedStartMap(FadeInFromLarge, three_axes))
        self.wait(2)

        self.three_axes = three_axes

    def bring_back_complex(self):
        numbers = self.numbers
        labels = self.labels
        numbers[0].move_to(numbers[1], LEFT)
        labels[0].move_to(labels[1], LEFT)
        numbers.remove(numbers[1])
        labels.remove(labels[1])

        group = VGroup(numbers, labels)
        self.play(
            group.to_edge, UP,
            FadeOut(self.three_axes, DOWN)
        )
        self.wait()

    def show_components_of_quaternion(self):
        quat = self.numbers[-1]
        real_part = quat[0]
        imag_part = quat[2:]
        real_brace = Brace(real_part, DOWN)
        imag_brace = Brace(imag_part, DOWN)
        real_word = OldTexText("Real \\\\ part")
        imag_word = OldTexText("Imaginary \\\\ part")
        scalar_word = OldTexText("Scalar \\\\ part")
        vector_word = OldTexText("``Vector'' \\\\ part")
        for word in real_word, scalar_word:
            word.next_to(real_brace, DOWN, SMALL_BUFF)
        for word in imag_word, vector_word:
            word.next_to(imag_brace, DOWN, SMALL_BUFF)
        braces = VGroup(real_brace, imag_brace)
        VGroup(scalar_word, vector_word).set_color(YELLOW)

        self.play(
            LaggedStartMap(GrowFromCenter, braces),
            LaggedStartMap(
                FadeInFrom, VGroup(real_word, imag_word),
                lambda m: (m, UP)
            )
        )
        self.wait()
        self.play(
            FadeOut(real_word, DOWN),
            FadeIn(scalar_word, DOWN),
        )
        self.wait(2)
        self.play(ChangeDecimalToValue(real_part, 0))
        self.wait()
        self.play(
            FadeOut(imag_word, DOWN),
            FadeIn(vector_word, DOWN)
        )
        self.wait(2)

    #
    def get_example_numbers(self):
        number_2d = VGroup(
            DecimalNumber(3.14),
            OldTex("+"),
            DecimalNumber(1.59),
            OldTex("i")
        )
        number_3d = VGroup(
            DecimalNumber(2.65),
            OldTex("+"),
            DecimalNumber(3.58),
            OldTex("i"),
            OldTex("+"),
            DecimalNumber(9.79),
            OldTex("j"),
        )
        number_4d = VGroup(
            DecimalNumber(3.23),
            OldTex("+"),
            DecimalNumber(8.46),
            OldTex("i"),
            OldTex("+"),
            DecimalNumber(2.64),
            OldTex("j"),
            OldTex("+"),
            DecimalNumber(3.38),
            OldTex("k"),
        )
        numbers = VGroup(number_2d, number_3d, number_4d)
        for number in numbers:
            number.arrange(RIGHT, buff=SMALL_BUFF)
            for part in number:
                if isinstance(part, Tex):
                    # part.set_color_by_tex_to_color_map({
                    #     "i": GREEN,
                    #     "j": RED,
                    #     "k": BLUE,
                    # })
                    if part.get_tex() == "j":
                        part.shift(0.5 * SMALL_BUFF * DL)
            number[2].set_color(GREEN)
            if len(number) > 5:
                number[5].set_color(RED)
            if len(number) > 8:
                number[8].set_color(BLUE)
        numbers.arrange(
            DOWN, buff=2, aligned_edge=LEFT
        )
        numbers.center()
        numbers.shift(LEFT)
        return numbers

    def get_simple_axes(self, label, color):
        axes = Axes(
            x_min=-2.5,
            x_max=2.5,
            y_min=-2.5,
            y_max=2.5,
        )
        axes.set_height(2.5)
        label_mob = OldTex(label)
        label_mob.set_color(color)
        label_mob.next_to(axes.coords_to_point(0, 1.5), RIGHT, SMALL_BUFF)
        reals_label_mob = OldTexText("Reals")
        reals_label_mob.next_to(
            axes.coords_to_point(1, 0), DR, SMALL_BUFF
        )
        axes.add(label_mob, reals_label_mob)
        return axes
