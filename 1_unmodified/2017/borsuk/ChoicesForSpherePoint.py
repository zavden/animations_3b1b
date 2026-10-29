# ==============================================================================
# Scene:      ChoicesForSpherePoint
# Source:     videos/_2017/borsuk.py (lines 1893-2001)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ChoicesForSpherePoint.py ChoicesForSpherePoint -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GeneralizeBorsukUlam(Scene):
    CONFIG = {
        "n_dims" : 3,
        "boundary_colors" : [GREEN_B, BLUE],
        "output_boundary_color" : [MAROON_B, YELLOW],
        "negative_color" : RED,
    }
    def setup(self):
        self.colors = color_gradient(self.boundary_colors, self.n_dims)

    def construct(self):
        sphere_set = self.get_sphere_set()
        arrow = Arrow(LEFT, RIGHT)
        f = OldTex("f")
        output_space = self.get_output_space()
        equation = self.get_equation()

        sphere_set.to_corner(UP+LEFT)
        arrow.next_to(sphere_set, RIGHT)
        f.next_to(arrow, UP)
        output_space.next_to(arrow, RIGHT)
        equation.next_to(sphere_set, DOWN, buff = LARGE_BUFF)
        equation.to_edge(RIGHT)
        lhs = VGroup(*equation[:2])
        eq = equation[2]
        rhs = VGroup(*equation[3:])

        self.play(FadeIn(sphere_set))
        self.wait()
        self.play(
            ShowCreation(arrow),
            Write(f)
        )
        self.play(Write(output_space))
        self.wait()
        self.play(FadeIn(lhs))
        self.play(
            ReplacementTransform(lhs.copy(), rhs),
            Write(eq)
        )
        self.wait()

    def get_condition(self):
        squares = list(map(Tex, [
            "x_%d^2"%d
            for d in range(1, 1+self.n_dims)
        ]))
        for square, color in zip(squares, self.colors):
            square[0].set_color(color)
            square[-1].set_color(color)
        plusses = [Tex("+") for x in range(self.n_dims-1)]
        plusses += [Tex("=1")]
        condition = VGroup(*it.chain(*list(zip(squares, plusses))))
        condition.arrange(RIGHT)

        return condition

    def get_tuple(self):
        mid_parts = list(it.chain(*[
            ["x_%d"%d, ","]
            for d in range(1, self.n_dims)
        ]))
        tup = OldTex(*["("] + mid_parts + ["x_%d"%self.n_dims, ")"])
        for index, color in zip(it.count(1, 2), self.colors):
            tup[index].set_color(color)

        return tup

    def get_negative_tuple(self):
        mid_parts = list(it.chain(*[
            ["-", "x_%d"%d, ","]
            for d in range(1, self.n_dims)
        ]))
        tup = OldTex(*["("] + mid_parts + ["-", "x_%d"%self.n_dims, ")"])
        for index, color in zip(it.count(1, 3), self.colors):
            tup[index].set_color(self.negative_color)
            tup[index+1].set_color(color)

        return tup

    def get_output_space(self):
        return OldTexText("%dD space"%(self.n_dims-1))
        # n_dims = self.n_dims-1
        # colors = color_gradient(self.output_boundary_color, n_dims)
        # mid_parts = list(it.chain(*[
        #     ["y_%d"%d, ","]
        #     for d in range(1, n_dims)
        # ]))
        # tup = OldTex(*["("] + mid_parts + ["y_%d"%n_dims, ")"])
        # for index, color in zip(it.count(1, 2), colors):
        #     tup[index].set_color(color)

        # return tup

    def get_equation(self):
        tup = self.get_tuple()
        neg_tup = self.get_negative_tuple()
        f1, f2 = [Tex("f") for x in range(2)]
        equals = OldTex("=")
        equation = VGroup(f1, tup, equals, f2, neg_tup)
        equation.arrange(RIGHT, buff = SMALL_BUFF)

        return equation

    def get_sphere_set(self):
        tup = self.get_tuple()
        such_that = OldTexText("such that")
        such_that.next_to(tup, RIGHT)
        condition = self.get_condition()
        condition.next_to(
            tup, DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )
        group = VGroup(tup, such_that, condition)
        l_brace = Brace(group, LEFT)
        r_brace = Brace(group, RIGHT)
        group.add(l_brace, r_brace)

        return group


class ChoicesForSpherePoint(GeneralizeBorsukUlam):
    def construct(self):
        self.add_sphere_set()
        self.initialize_words()
        self.play(Write(self.choice_one_words))
        self.wait()
        self.show_example_choices()
        self.show_binary_choices()

    def get_tuple(self):
        tup = OldTex("(x, y, z)")
        for i, color in zip([1, 3, 5], self.colors):
            tup[i].set_color(color)
        return tup

    def get_condition(self):
        condition = OldTex("x^2+y^2+z^2 = 1")
        for i, color in zip([0, 3, 6], self.colors):
            VGroup(*condition[i:i+2]).set_color(color)
        return condition

    def add_sphere_set(self):
        sphere_set = self.get_sphere_set()
        sphere_set.scale(0.7)
        sphere_set.to_edge(RIGHT)
        sphere_set.shift(UP)

        self.add(sphere_set)
        self.sphere_set = sphere_set

    def initialize_words(self):
        choice_one_words = OldTexText(
            "1) Choose", "$x^2$, $y^2$, $z^2$",
            "so that", "$x^2+y^2+z^2 = 1$"
        )
        for i in 1, 3:
            for j, color in zip([0, 3, 6], self.colors):
                VGroup(*choice_one_words[i][j:j+2]).set_color(color)
        choice_one_words.to_corner(UP+LEFT)

        choice_two_words = OldTexText(
            "2) Make a binary choice for each one"
        )
        choice_two_words.next_to(
            choice_one_words, DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT
        )

        self.choice_one_words = choice_one_words
        self.choice_two_words = choice_two_words

    def show_example_choices(self):
        choices = VGroup(*[
            OldTex(*tex).set_color(color)
            for color, tex in zip(self.colors, [
                ("x", "^2 = ", "1/6"),
                ("y", "^2 = ", "1/3"),
                ("z", "^2 = ", "1/2"),
            ])
        ])
        choices.arrange(
            DOWN, 
            buff = LARGE_BUFF,
            aligned_edge = LEFT
        )
        choices.set_height(FRAME_Y_RADIUS)
        choices.to_edge(LEFT)
        choices.shift(DOWN)

        self.play(FadeIn(
            choices,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait()

        self.choices = choices

    def show_binary_choices(self):
        for choice in self.choices:
            var_tex = choice.expression_parts[0]
            frac_tex = choice.expression_parts[2]
            sqrts = VGroup(*[
                OldTex(
                    var_tex + "=" + sign + \
                    "\\sqrt{%s}"%frac_tex)
                for sign in ["+", "-"]
            ])
            for sqrt in sqrts:
                sqrt.scale(0.6)
            sqrts.arrange(DOWN)
            sqrts.next_to(choice, RIGHT, buff = LARGE_BUFF)
            sqrts.set_color(choice.get_color())

            arrows = VGroup(*[
                Arrow(
                    choice.get_right(), sqrt.get_left(), 
                    color = WHITE,
                    tip_length = 0.1,
                    buff = SMALL_BUFF
                )
                for sqrt in sqrts
            ])

            self.play(ShowCreation(arrows))
            self.play(FadeIn(sqrts, lag_ratio = 0.5))
        self.play(Write(self.choice_two_words))
        self.wait()
