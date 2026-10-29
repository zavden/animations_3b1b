# ==============================================================================
# Scene:      DiscussProducts
# Source:     videos/_2017/eoc/chapter4.py (lines 667-711)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DiscussProducts.py DiscussProducts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

SINE_COLOR = BLUE


X_SQUARED_COLOR = GREEN


class DiscussProducts(TeacherStudentsScene):
    def construct(self):
        wrong_product_rule = OldTex(
            "\\frac{d(\\sin(x)x^2)}{dx}", 
            "\\ne",
            "\\left(\\frac{d(\\sin(x))}{dx}\\right)",
            "\\left(\\frac{d(x^2)}{dx}\\right)",
        )
        not_equals = wrong_product_rule[1]
        wrong_product_rule[2].set_color(SINE_COLOR)
        wrong_product_rule[3].set_color(X_SQUARED_COLOR)
        wrong_product_rule.next_to(
            self.get_teacher().get_corner(UP+LEFT),
            UP,
            buff = MED_LARGE_BUFF
        ).shift_onto_screen()

        self.teacher_says(
            "Products are a bit different",
            target_mode = "sassy"
        )
        self.wait(2)
        self.play(RemovePiCreatureBubble(
            self.get_teacher(), 
            target_mode = "raise_right_hand"
        ))
        self.play(Write(wrong_product_rule))
        self.play_student_changes(
            "pondering", "confused", "erm",
            added_anims = [
                not_equals.scale, 1.3,
                not_equals.set_color, RED
            ]
        )
        self.wait()
        self.teacher_says(
            "Think about the \\\\ underlying meaning",
            bubble_config = {"height" : 3},
            added_anims = [
                wrong_product_rule.scale, 0.7,
                wrong_product_rule.to_corner, UP+LEFT
            ]
        )
        self.play_student_changes(*["pondering"]*3)
        self.wait(2)
