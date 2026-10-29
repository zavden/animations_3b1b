# ==============================================================================
# Scene:      ShowAlternateFactorizationOfTwentyFive
# Source:     videos/_2017/leibniz.py (lines 2829-2843)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowAlternateFactorizationOfTwentyFive.py ShowAlternateFactorizationOfTwentyFive -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
from functools import reduce

class IntroduceRecipe(Scene):
    CONFIG = {
        "N_string" : "25",
        "integer_factors" : [5, 5],
        "gaussian_factors" : [
            complex(2, 1), complex(2, -1),
            complex(2, 1), complex(2, -1),
        ],
        "x_color" : GREEN,
        "y_color" : RED,
        "N_color" : WHITE,
        "i_positive_color" : BLUE,
        "i_negative_color" : YELLOW,
        "i_zero_color" : MAROON_B,
        "T_chart_width" : 8,
        "T_chart_height" : 6,
    }
    def construct(self):
        self.add_title()
        self.show_ordinary_factorization()
        self.subfactor_ordinary_factorization()
        self.organize_factors_into_columns()
        self.mention_conjugate_rule()
        self.take_product_of_columns()
        self.mark_left_product_as_result()
        self.swap_factors()

    def add_title(self):
        title = OldTex(
            "\\text{Recipe for }",
            "a", "+", "b", "i",
            "\\text{ satisfying }",
            "(", "a", "+", "b", "i", ")",
            "(", "a", "-", "b", "i", ")",
            "=", self.N_string
        )
        strings = ("a", "b", self.N_string)
        colors = (self.x_color, self.y_color, self.N_color)
        for tex, color in zip(strings, colors):
            title.set_color_by_tex(tex, color, substring = False)
        title.to_edge(UP, buff = MED_SMALL_BUFF)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.next_to(title, DOWN)
        self.add(title, h_line)
        N_mob = title.get_part_by_tex(self.N_string)
        digest_locals(self, ["title", "h_line", "N_mob"])

    def show_ordinary_factorization(self):
        N_mob = self.N_mob.copy()
        N_mob.generate_target()
        N_mob.target.next_to(self.h_line, DOWN)
        N_mob.target.to_edge(LEFT)

        factors = self.integer_factors
        symbols = ["="] + ["\\cdot"]*(len(factors)-1)
        factorization = OldTex(*it.chain(*list(zip(
            symbols, list(map(str, factors))
        ))))
        factorization.next_to(N_mob.target, RIGHT)

        self.play(MoveToTarget(
            N_mob,
            run_time = 2,
            path_arc = -np.pi/6
        ))
        self.play(Write(factorization))
        self.wait()

        self.factored_N_mob = N_mob
        self.integer_factorization = factorization

    def subfactor_ordinary_factorization(self):
        factors = self.gaussian_factors
        factorization = OldTex(
            "=", *list(map(self.complex_number_to_tex, factors))
        )
        max_width = FRAME_WIDTH - 2
        if factorization.get_width() > max_width:
            factorization.set_width(max_width)
        factorization.next_to(
            self.integer_factorization, DOWN,
            aligned_edge = LEFT
        )
        for factor, mob in zip(factors, factorization[1:]):
            mob.underlying_number = factor
            y = complex(factor).imag
            if y == 0:
                mob.set_color(self.i_zero_color)
            elif y > 0:
                mob.set_color(self.i_positive_color)
            elif y < 0:
                mob.set_color(self.i_negative_color)
        movers = VGroup()
        mover = self.integer_factorization[0].copy()
        mover.target = factorization[0]
        movers.add(mover)
        index = 0
        for prime_mob in self.integer_factorization[1::2]:
            gauss_prime = factors[index]
            gauss_prime_mob = factorization[index+1]
            mover = prime_mob.copy()
            mover.target = gauss_prime_mob
            movers.add(mover)
            if abs(complex(gauss_prime).imag) > 0:
                index += 1
                mover = prime_mob.copy()
                mover.target = factorization[index+1]
                movers.add(mover)
            index += 1

        self.play(LaggedStartMap(
            MoveToTarget,
            movers,
            replace_mobject_with_target_in_scene = True
        ))
        self.wait()

        self.gaussian_factorization = factorization

    def organize_factors_into_columns(self):
        T_chart = self.get_T_chart()
        factors = self.gaussian_factorization.copy()[1:]
        left_factors, right_factors = self.get_left_and_right_factors()
        for group in left_factors, right_factors:
            group.generate_target()
            group.target.arrange(DOWN)
        left_factors.target.next_to(T_chart.left_h_line, DOWN)
        right_factors.target.next_to(T_chart.right_h_line, DOWN)

        self.play(ShowCreation(T_chart))
        self.wait()
        self.play(MoveToTarget(left_factors))
        self.play(MoveToTarget(right_factors))
        self.wait()

        digest_locals(self, ["left_factors", "right_factors"])

    def mention_conjugate_rule(self):
        left_factors = self.left_factors
        right_factors = self.right_factors
        double_arrows = VGroup()
        for lf, rf in zip(left_factors.target, right_factors.target):
            arrow = DoubleArrow(
                lf, rf, 
                buff = SMALL_BUFF,
                tip_length = SMALL_BUFF,
                color = GREEN
            )
            word = OldTexText("Conjugates")
            word.scale(0.75)
            word.add_background_rectangle()
            word.next_to(arrow, DOWN, SMALL_BUFF)
            arrow.add(word)
            double_arrows.add(arrow)
        main_arrow = double_arrows[0]

        self.play(Write(main_arrow, run_time = 1))
        self.wait()
        for new_arrow in double_arrows[1:]:
            self.play(Transform(main_arrow, new_arrow))
            self.wait()
        self.wait()
        self.play(FadeOut(main_arrow))

    def take_product_of_columns(self):
        arrows = self.get_product_multiplication_lines()
        products = self.get_product_mobjects()
        factor_groups = [self.left_factors, self.right_factors]

        for arrow, product, group in zip(arrows, products, factor_groups):
            self.play(ShowCreation(arrow))
            self.play(ReplacementTransform(
                group.copy(), VGroup(product)
            ))
            self.wait()
        self.wait(3)

    def mark_left_product_as_result(self):
        rect = self.get_result_surrounding_rect()
        words = OldTexText("Output", " of recipe")
        words.next_to(rect, DOWN, buff = MED_LARGE_BUFF)
        words.to_edge(LEFT)
        arrow = Arrow(words.get_top(), rect.get_left())

        self.play(ShowCreation(rect))
        self.play(
            Write(words, run_time = 2),
            ShowCreation(arrow)
        )
        self.wait(3)
        self.play(*list(map(FadeOut, [words, arrow])))

        self.output_label_group = VGroup(words, arrow)

    def swap_factors(self):
        for i in range(len(self.left_factors)):
            self.swap_factors_at_index(i)
            self.wait()

    #########

    def get_left_and_right_factors(self):
        factors = self.gaussian_factorization.copy()[1:]
        return VGroup(*factors[::2]), VGroup(*factors[1::2])

    def get_T_chart(self):
        T_chart = VGroup()
        h_lines = VGroup(*[
            Line(ORIGIN, self.T_chart_width*RIGHT/2.0) 
            for x in range(2)
        ])
        h_lines.arrange(RIGHT, buff = 0)
        h_lines.shift(UP)
        v_line = Line(self.T_chart_height*UP, ORIGIN)
        v_line.move_to(h_lines.get_center(), UP)

        T_chart.left_h_line, T_chart.right_h_line = h_lines
        T_chart.v_line = v_line
        T_chart.digest_mobject_attrs()

        return T_chart

    def complex_number_to_tex(self, z):
        z = complex(z)
        x, y = z.real, z.imag
        if y == 0:
            return "(%d)"%x
        y_sign_tex = "+" if y >= 0 else "-"
        if abs(y) == 1:
            y_str = y_sign_tex + "i"
        else:
            y_str = y_sign_tex + "%di"%abs(y)
        return "(%d%s)"%(x, y_str)

    def get_product_multiplication_lines(self):
        lines = VGroup()
        for factors in self.left_factors, self.right_factors:
            line = Line(ORIGIN, 3*RIGHT)
            line.next_to(factors, DOWN, SMALL_BUFF)
            times = OldTex("\\times")
            times.next_to(line.get_left(), UP+RIGHT, SMALL_BUFF)
            line.add(times)
            lines.add(line)
        self.multiplication_lines = lines
        return lines

    def get_product_mobjects(self):
        factor_groups = [self.left_factors, self.right_factors]
        product_mobjects = VGroup()
        for factors, line in zip(factor_groups, self.multiplication_lines):
            product = reduce(op.mul, [
                factor.underlying_number
                for factor in factors
            ])
            color = average_color(*[
                factor.get_color()
                for factor in factors
            ])
            product_mob = OldTex(
                self.complex_number_to_tex(product)
            )
            product_mob.set_color(color)
            product_mob.next_to(line, DOWN)
            product_mobjects.add(product_mob)
        self.product_mobjects = product_mobjects
        return product_mobjects

    def swap_factors_at_index(self, index):
        factor_groups = self.left_factors, self.right_factors
        factors_to_swap = [group[index] for group in factor_groups]
        self.play(*[
            ApplyMethod(
                factors_to_swap[i].move_to, factors_to_swap[1-i],
                path_arc = np.pi/2,
            )
            for i in range(2)
        ])
        for i, group in enumerate(factor_groups):
            group.submobjects[index] = factors_to_swap[1-i]
        self.play(FadeOut(self.product_mobjects))
        self.get_product_mobjects()
        rect = self.result_surrounding_rect
        new_rect = self.get_result_surrounding_rect()
        self.play(*[
            ReplacementTransform(group.copy(), VGroup(product))
            for group, product in zip(
                factor_groups, self.product_mobjects,
            )
        ]+[
            ReplacementTransform(rect, new_rect)
        ])
        self.wait()

    def get_result_surrounding_rect(self, product = None):
        if product is None:
            product = self.product_mobjects[0]
        rect = SurroundingRectangle(product)
        self.result_surrounding_rect = rect
        return rect

    def write_last_step(self):
        output_words, arrow = self.output_label_group
        final_step = OldTexText(
            "Multiply by $1$, $i$, $-1$ or $-i$"
        )
        final_step.scale(0.9)
        final_step.next_to(arrow.get_start(), DOWN, SMALL_BUFF)
        final_step.shift_onto_screen()
        
        anims = [Write(final_step)]
        if arrow not in self.get_mobjects():
            # arrow = Arrow(
            #     final_step.get_top(),
            #     self.result_surrounding_rect.get_left()
            # )
            anims += [ShowCreation(arrow)]
        self.play(*anims)
        self.wait(2)


class ShowAlternateFactorizationOfTwentyFive(IntroduceRecipe):
    CONFIG = {
        "gaussian_factors" : [
            complex(-1, 2), complex(-1, -2),
            complex(2, 1), complex(2, -1),
        ],
    }
    def construct(self):
        self.add_title()
        self.show_ordinary_factorization()
        self.subfactor_ordinary_factorization()
        self.organize_factors_into_columns()
        self.take_product_of_columns()
        self.mark_left_product_as_result()
        self.swap_factors()
