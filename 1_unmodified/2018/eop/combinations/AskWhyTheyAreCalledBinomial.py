# ==============================================================================
# Scene:      AskWhyTheyAreCalledBinomial
# Source:     videos/_2018/eop/combinations.py (lines 3454-3512)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskWhyTheyAreCalledBinomial.py AskWhyTheyAreCalledBinomial -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PascalsTriangle(VGroup):
    CONFIG = {
        "n_rows" : 9,
        "distance" : 0.8,
        "max_width_to_distance_ratio" : 0.7,
        "angle" : 0.2*np.pi,
    }
    def __init__(self, **kwargs):
        VGroup.__init__(self, **kwargs)

        distance = self.distance
        angle = self.angle
        max_width = self.max_width_to_distance_ratio * distance
        t_down = rotate_vector(distance*DOWN, -angle)
        t_right = 2*distance*np.sin(angle)*RIGHT

        for n in range(self.n_rows):
            row = VGroup()
            for k in range(n+1):
                num = OldTex(str(choose(n, k)))
                num.shift(n*t_down + k*t_right)
                row.add(num)
            self.add(row)
        self.center()


class AskWhyTheyAreCalledBinomial(TeacherStudentsScene):
    def construct(self):
        example_binomials = VGroup(*[
            OldTex("(x+y)^%d"%d)
            for d in range(2, 7)
        ])
        example_binomials.arrange(UP)
        example_binomials.next_to(
            self.teacher.get_corner(UP+LEFT), UP 
        )

        pascals = PascalsTriangle(n_rows = 6)
        pascals.set_height(3)
        pascals.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        pascals.set_color_by_gradient(BLUE, YELLOW)

        binomial_word = OldTexText(
            "Bi", "nomials",
            arg_separator = "",
        )
        binomial_word.set_color_by_tex("Bi", YELLOW)
        binomial_word.set_color_by_tex("nomials", WHITE)
        binomial_word.next_to(example_binomials, LEFT, buff = 1.5)
        arrows = VGroup(*[
            Arrow(binomial_word.get_right(), binom.get_left())
            for binom in example_binomials
        ])
        arrows.set_color(BLUE)

        two_variables = OldTexText("Two", "variables")
        two_variables.next_to(binomial_word, DOWN)
        two_variables.shift(SMALL_BUFF*LEFT)
        for tv, bw in zip(two_variables, binomial_word):
            tv.set_color(bw.get_color())

        self.student_says(
            "Why are they called \\\\ ``binomial coefficients''?"
        )
        self.play(LaggedStartMap(FadeIn, pascals))
        self.wait()
        self.play(
            FadeIn(example_binomials[0]),
            RemovePiCreatureBubble(self.students[1]),
            self.teacher.change, "raise_right_hand",
        )
        moving_binom = example_binomials[0].copy()
        for binom in example_binomials[1:]:
            self.play(Transform(moving_binom, binom))
            self.add(binom)
        self.wait()

        #Name themn
        self.play(
            Write(binomial_word),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.play_student_changes(*["pondering"]*3)
        self.play(Write(two_variables))
        self.wait(2)
