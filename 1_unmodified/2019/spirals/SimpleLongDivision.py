# ==============================================================================
# Scene:      SimpleLongDivision
# Source:     videos/_2019/spirals.py (lines 1970-2016)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimpleLongDivision.py SimpleLongDivision -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SimpleLongDivision(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E
        }
    }

    def construct(self):
        divisor = Integer(6)
        num = Integer(20)
        quotient = Integer(num.get_value() // divisor.get_value())
        to_subtract = Integer(-1 * quotient.get_value() * divisor.get_value())
        remainder = Integer(num.get_value() + to_subtract.get_value())

        div_sym = VMobject()
        div_sym.set_points_as_corners([0.2 * UP, UP, UP + 3 * RIGHT])

        divisor.next_to(div_sym, LEFT, MED_SMALL_BUFF)
        num.next_to(divisor, RIGHT, MED_LARGE_BUFF)
        to_subtract.next_to(num, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        h_line = Line(LEFT, RIGHT)
        h_line.next_to(to_subtract, DOWN, buff=MED_SMALL_BUFF)
        remainder.next_to(to_subtract, DOWN, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        quotient.next_to(num, UP, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)

        remainder_rect = SurroundingRectangle(remainder)
        remainder_rect.set_color(RED)

        frame = self.camera_frame
        frame.scale(0.7, about_point=ORIGIN)

        divisor.set_color(YELLOW)
        num.set_color(RED)

        self.add(divisor)
        self.add(div_sym)
        self.add(num)
        self.play(FadeInFromDown(quotient))
        self.play(
            TransformFromCopy(divisor, to_subtract.copy()),
            TransformFromCopy(quotient, to_subtract),
        )
        self.play(ShowCreation(h_line))
        self.play(Write(remainder))
        self.play(ShowCreation(remainder_rect))
        self.wait()
        self.play(FadeOut(remainder_rect))
