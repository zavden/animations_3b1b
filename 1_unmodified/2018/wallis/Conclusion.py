# ==============================================================================
# Scene:      Conclusion
# Source:     videos/_2018/wallis.py (lines 4958-5037)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Conclusion.py Conclusion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


class Conclusion(TeacherStudentsScene):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
    }

    def construct(self):
        wallis_product = get_wallis_product(6)
        wallis_product.move_to(self.hold_up_spot, DOWN)
        wallis_product.shift_onto_screen()
        for i in range(0, len(wallis_product) - 5, 4):
            color = GREEN if (i / 4) % 2 == 0 else BLUE
            wallis_product[i:i + 3].set_color(color)

        sine_formula = OldTex(
            "\\sin(", "f", "\\pi", ")", "=", "f", "\\pi",
            "\\prod_{k \\ne 0}", "\\left(", "1", "-",
            "{f", "\\over", "k}", "\\right)"
        )
        sine_formula.set_color_by_tex("f", GREEN)
        sine_formula.set_color_by_tex("left", WHITE)
        sine_formula.move_to(self.hold_up_spot, DOWN)
        sine_formula.shift_onto_screen()

        euler = ImageMobject("Euler")
        euler.set_height(2.5)
        basel_problem = OldTex(
            "\\frac{1}{1^2} + ",
            "\\frac{1}{2^2} + ",
            "\\frac{1}{3^2} + ",
            "\\cdots",
            "\\frac{\\pi^2}{6}"
        )
        basel_problem.move_to(self.hold_up_spot, DOWN)
        implication = OldTex("\\Rightarrow")
        implication.next_to(basel_problem[0][1], LEFT)

        self.play(
            self.teacher.change, "raise_right_hand",
            FadeInFromDown(wallis_product),
            self.change_students("thinking", "hooray", "surprised")
        )
        self.wait()
        self.play(
            self.teacher.change, "hooray",
            FadeInFromDown(sine_formula),
            wallis_product.to_edge, UP,
            self.change_students("pondering", "thinking", "erm")
        )
        self.wait(3)
        self.play(
            sine_formula.next_to, implication, LEFT,
            {"submobject_to_align": sine_formula[-1]},
            FadeIn(implication),
        )
        euler.next_to(sine_formula, UP)
        self.play(
            FadeIn(euler),
            LaggedStartMap(FadeIn, basel_problem),
            self.teacher.change, "happy",
            self.change_students("sassy", "confused", "hesitant")
        )
        self.wait(2)

        wallis_rect = SurroundingRectangle(wallis_product)
        wallis_rect.set_color(BLUE)
        basel_rect = SurroundingRectangle(basel_problem)
        basel_rect.set_color(YELLOW)

        self.play(
            ShowCreation(wallis_rect),
            FadeOut(implication),
            FadeOut(euler),
            FadeOut(sine_formula),
        )
        self.play(
            ShowCreation(basel_rect),
            self.teacher.change, "surprised",
            self.change_students(*["happy"] * 3)
        )
        self.wait(5)
