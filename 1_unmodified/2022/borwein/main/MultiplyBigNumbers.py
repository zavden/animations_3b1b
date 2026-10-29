# ==============================================================================
# Scene:      MultiplyBigNumbers
# Source:     videos/_2022/borwein/main.py (lines 1763-1826)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultiplyBigNumbers.py MultiplyBigNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MultiplyBigNumbers(InteractiveScene):
    def construct(self):
        # Numbers
        numbers = VGroup(
            Tex("3{,}141{,}592{,}653{,}589{,}793{,}238"),
            Tex("2{,}718{,}281{,}828{,}459{,}045{,}235"),
        )
        numbers.arrange(DOWN, aligned_edge=RIGHT)
        numbers.scale(1.5)
        numbers.move_to(1.0 * DOWN)
        underline = Underline(numbers).set_stroke(WHITE, 2)
        underline.stretch(1.2, 0, about_edge=RIGHT)
        times = OldTex(R"\times")
        times.scale(1.5)
        times.next_to(underline.get_left(), UR)

        self.add(numbers)
        self.add(underline, times)

        # Prep run time
        d_label = OldTexText("Two $N$-digit numbers", tex_to_color_map={"$N$": YELLOW})
        d_label.next_to(numbers, UP, buff=LARGE_BUFF)
        d2_label = OldTex(R"\mathcal{O}(N^2)", font_size=60, tex_to_color_map={"N": YELLOW})
        dlogd_label = OldTex(R"\mathcal{O}({N} \cdot \text{log}({N}))", font_size=60, tex_to_color_map={"{N}": YELLOW})
        os = VGroup(d2_label, dlogd_label)
        os.arrange(RIGHT, buff=2.5)
        os.next_to(d_label, UP, buff=LARGE_BUFF)
        # cross = Exmark().scale(2).next_to(d2_label, RIGHT)
        cross = Cross(d2_label)
        cross.insert_n_curves(50).set_stroke(RED, (0, 8, 8, 8, 8, 0))
        check = Checkmark().scale(2).next_to(dlogd_label, RIGHT)
        q_marks = OldTex("?", font_size=72)
        q_marks.next_to(d2_label, RIGHT)

        # Square run time
        for num in numbers:
            num.digits = num[::-1]
            num.digits.remove(*num[-4::-4])
            num.digit_highlights = VGroup(*(
                VHighlight(digit, color_bounds=(YELLOW, YELLOW_E), max_stroke_addition=8)
                for digit in num.digits
            ))

        self.add(d_label)
        self.play(FadeIn(d2_label, UP), FadeIn(q_marks, UP))
        for dh2 in numbers[1].digit_highlights:
            self.add(dh2, numbers[1])
            self.play(
                ShowSubmobjectsOneByOne(
                    numbers[0].digit_highlights.copy(),
                    remover=True
                ),
                run_time=1.0
            )
            self.remove(dh2)

        # d * log(d)
        self.play(
            ShowCreation(cross),
            FadeOut(q_marks),
            FadeTransform(d2_label.copy(), dlogd_label)
        )
        self.play(Write(check))
        self.wait()
