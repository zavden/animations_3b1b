# ==============================================================================
# Scene:      IntroduceChi
# Source:     videos/_2017/leibniz.py (lines 3441-3674)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceChi.py IntroduceChi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def chi_func(n):
    if n%2 == 0:
        return 0
    if n%4 == 1:
        return 1
    else:
        return -1


class FactorizationPattern(Scene):
    def construct(self):
        self.force_skipping()

        self.add_number_line()
        self.show_one_mod_four_primes()
        self.show_three_mod_four_primes()
        self.ask_why_this_is_true()
        self.show_two()

    def add_number_line(self):
        line = NumberLine(
            x_min = 0,
            x_max = 36,
            unit_size = 0.4,
            numbers_to_show = list(range(0, 33, 4)),
            big_tick_numbers = list(range(0, 33, 4)),
        )
        line.shift(2*DOWN)
        line.to_edge(LEFT)
        line.add_numbers()

        self.add(line)
        self.number_line = line

    def show_one_mod_four_primes(self):
        primes = [5, 13, 17, 29]
        dots = VGroup(*[
            Dot(self.number_line.number_to_point(prime))
            for prime in primes
        ])
        dots.set_color(GREEN)
        prime_mobs = VGroup(*list(map(Tex, list(map(str, primes)))))
        arrows = VGroup()
        for prime_mob, dot in zip(prime_mobs, dots):
            prime_mob.next_to(dot, UP, LARGE_BUFF)
            prime_mob.set_color(dot.get_color())
            arrow = Arrow(prime_mob, dot, buff = SMALL_BUFF)
            arrow.set_color(dot.get_color())
            arrows.add(arrow)

        factorizations = VGroup(*[
            OldTex("=(%d+%si)(%d-%si)"%(x, y_str, x, y_str))
            for x, y in [(2, 1), (3, 2), (4, 1), (5, 2)]
            for y_str in [str(y) if y is not 1 else ""]
        ])
        factorizations.arrange(DOWN, aligned_edge = LEFT)
        factorizations.to_corner(UP+LEFT)
        factorizations.shift(RIGHT)
        movers = VGroup()
        for p_mob, factorization in zip(prime_mobs, factorizations):
            mover = p_mob.copy()
            mover.generate_target()
            mover.target.next_to(factorization, LEFT)
            movers.add(mover)
        v_dots = OldTex("\\vdots")
        v_dots.next_to(factorizations[-1][0], DOWN)
        factorization.add(v_dots)

        self.play(*it.chain(
            list(map(Write, prime_mobs)),
            list(map(ShowCreation, arrows)),
            list(map(DrawBorderThenFill, dots)),
        ))
        self.wait()
        self.play(*[
            MoveToTarget(
                mover,
                run_time = 2,
                path_arc = np.pi/2,
            )
            for mover in movers
        ])
        self.play(FadeIn(
            factorizations, 
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(4)
        self.play(*list(map(FadeOut, [movers, factorizations])))

    def show_three_mod_four_primes(self):
        primes = [3, 7, 11, 19, 23, 31]
        dots = VGroup(*[
            Dot(self.number_line.number_to_point(prime))
            for prime in primes
        ])
        dots.set_color(RED)
        prime_mobs = VGroup(*list(map(Tex, list(map(str, primes)))))
        arrows = VGroup()
        for prime_mob, dot in zip(prime_mobs, dots):
            prime_mob.next_to(dot, UP, LARGE_BUFF)
            prime_mob.set_color(dot.get_color())
            arrow = Arrow(prime_mob, dot, buff = SMALL_BUFF)
            arrow.set_color(dot.get_color())
            arrows.add(arrow)

        words = OldTexText("Already Gaussian primes")
        words.to_corner(UP+LEFT)
        word_arrows = VGroup(*[
            Line(
                words.get_bottom(), p_mob.get_top(),
                color = p_mob.get_color(),
                buff = MED_SMALL_BUFF
            )
            for p_mob in prime_mobs
        ])

        self.play(*it.chain(
            list(map(Write, prime_mobs)),
            list(map(ShowCreation, arrows)),
            list(map(DrawBorderThenFill, dots)),
        ))
        self.wait()
        self.play(
            Write(words),
            *list(map(ShowCreation, word_arrows))
        )
        self.wait(4)
        self.play(*list(map(FadeOut, [words, word_arrows])))

    def ask_why_this_is_true(self):
        randy = Randolph(color = BLUE_C)
        randy.scale(0.7)
        randy.to_edge(LEFT)
        randy.shift(0.8*UP)

        links_text = OldTexText("(See links in description)")
        links_text.scale(0.7)
        links_text.to_corner(UP+RIGHT)
        links_text.shift(DOWN)

        self.play(FadeIn(randy))
        self.play(PiCreatureBubbleIntroduction(
            randy, "Wait...why?",
            bubble_type = ThoughtBubble,
            bubble_config = {"height" : 2, "width" : 3},
            target_mode = "confused",
            look_at = self.number_line,
        ))
        self.play(Blink(randy))
        self.wait()
        self.play(FadeIn(links_text))
        self.wait(2)
        self.play(*list(map(FadeOut, [
            randy, randy.bubble, randy.bubble.content,
            links_text
        ])))

    def show_two(self):
        two_dot = Dot(self.number_line.number_to_point(2))
        two = OldTex("2")
        two.next_to(two_dot, UP, LARGE_BUFF)
        arrow = Arrow(two, two_dot, buff = SMALL_BUFF)
        VGroup(two_dot, two, arrow).set_color(YELLOW)

        mover = two.copy()
        mover.generate_target()
        mover.target.to_corner(UP+LEFT)
        factorization = OldTex("=", "(1+i)", "(1-i)")
        factorization.next_to(mover.target, RIGHT)
        factors = VGroup(*factorization[1:])

        time_i_arrow = Arrow(
            factors[1].get_bottom(),
            factors[0].get_bottom(),
            path_arc = -np.pi
        )
        times_i = OldTex("\\times i")
        # times_i.scale(1.5)
        times_i.next_to(time_i_arrow, DOWN)
        times_i.set_color(time_i_arrow.get_color())
        words = OldTexText("You'll see why this matters...")
        words.next_to(times_i, DOWN)
        words.shift_onto_screen()

        self.play(
            Write(two),
            ShowCreation(arrow),
            DrawBorderThenFill(two_dot)
        )
        self.wait()
        self.play(
            MoveToTarget(mover),
            Write(factorization)
        )

        self.revert_to_original_skipping_status()
        self.wait(2)
        self.play(ShowCreation(time_i_arrow))
        self.play(Write(times_i))
        self.wait(2)
        self.play(FadeIn(words))
        self.wait(2)


class IntroduceChi(FactorizationPattern):
    CONFIG = {
        "numbers_list" : [
            list(range(i, 36, d))
            for i, d in [(1, 4), (3, 4), (2, 2)]
        ],
        "colors" : [GREEN, RED, YELLOW]
    }
    def construct(self):
        self.add_number_line()
        self.add_define_chi_label()
        for index in range(3):
            self.describe_values(index)
        self.fade_out_labels()
        self.cyclic_pattern()
        self.write_multiplicative_label()
        self.show_multiplicative()


    def add_define_chi_label(self):
        label = OldTexText("Define $\\chi(n)$:")
        chi_expressions = VGroup(*[
            self.get_chi_expression(numbers, color)
            for numbers, color in zip(
                self.numbers_list,
                self.colors
            )
        ])
        chi_expressions.scale(0.9)
        chi_expressions.arrange(
            DOWN, buff = MED_LARGE_BUFF, aligned_edge = LEFT
        )
        chi_expressions.to_corner(UP+RIGHT)
        brace = Brace(chi_expressions, LEFT)
        label.next_to(brace, LEFT)

        self.play(
            Write(label),
            GrowFromCenter(brace)
        )
        self.define_chi_label = label
        self.chi_expressions = chi_expressions

    def describe_values(self, index):
        numbers = self.numbers_list[index]
        color = self.colors[index]
        dots, arrows, labels = self.get_dots_arrows_and_labels(
            numbers, color
        )
        chi_expression = self.chi_expressions[index]

        self.introduce_dots_arrows_and_labels(dots, arrows, labels)
        self.wait()
        self.play(
            Write(VGroup(*[
                part 
                for part in chi_expression
                if part not in chi_expression.inputs
            ])), 
        *[
            ReplacementTransform(label.copy(), num_mob)
            for label, num_mob in zip(
                labels, chi_expression.inputs
            )
        ])
        self.wait()

    def fade_out_labels(self):
        self.play(*list(map(FadeOut, [
            self.last_dots, self.last_arrows, self.last_labels,
            self.number_line
        ])))

    def cyclic_pattern(self):
        input_range = list(range(1, 9))
        chis = VGroup(*[
            OldTex("\\chi(%d)"%n)
            for n in input_range
        ])
        chis.arrange(RIGHT, buff = LARGE_BUFF)
        chis.set_stroke(WHITE, width = 1)
        numbers = VGroup()
        arrows = VGroup()
        for chi, n in zip(chis, input_range):
            arrow = OldTex("\\Uparrow")
            arrow.next_to(chi, UP, SMALL_BUFF)
            arrows.add(arrow)
            value = OldTex(str(chi_func(n)))
            for tex, color in zip(["1", "-1", "0"], self.colors):
                value.set_color_by_tex(tex, color)
            value.next_to(arrow, UP)
            numbers.add(value)
        group = VGroup(chis, arrows, numbers)
        group.set_width(FRAME_WIDTH - LARGE_BUFF)
        group.to_edge(DOWN, buff = LARGE_BUFF)

        self.play(*[
            FadeIn(
                mob, 
                run_time = 3,
                lag_ratio = 0.5
            )
            for mob in [chis, arrows, numbers]
        ])

        self.play(LaggedStartMap(
            ApplyMethod,
            numbers,
            lambda m : (m.shift, MED_SMALL_BUFF*UP),
            rate_func = there_and_back,
            lag_ratio = 0.2,
            run_time = 6
        ))

        self.wait()
        self.play(*list(map(FadeOut, [chis, arrows, numbers])))

    def write_multiplicative_label(self):
        morty = Mortimer()
        morty.scale(0.7)
        morty.to_corner(DOWN+RIGHT)

        self.play(PiCreatureSays(
            morty, "$\\chi$ is ``multiplicative''",
            bubble_config = {"height" : 2.5, "width" : 5}
        ))
        self.play(Blink(morty))
        self.morty = morty

    def show_multiplicative(self):
        pairs = [(3, 5), (5, 5), (2, 13), (3, 11)]
        expressions = VGroup()
        for x, y in pairs:
            expression = OldTex(
                "\\chi(%d)"%x,
                "\\cdot",
                "\\chi(%d)"%y,
                "=", 
                "\\chi(%d)"%(x*y)
            )
            braces = [
                Brace(expression[i], UP) 
                for i in (0, 2, 4)
            ]
            for brace, n in zip(braces, [x, y, x*y]):
                output = chi_func(n)
                label = brace.get_tex(str(output))
                label.set_color(self.number_to_color(output))
                brace.add(label)
                expression.add(brace)
            expressions.add(expression)

        expressions.next_to(ORIGIN, LEFT)
        expressions.shift(DOWN)
        expression = expressions[0]

        self.play(
            FadeIn(expression),
            self.morty.change, "pondering", expression
        )
        self.wait(2)
        for new_expression in expressions[1:]:
            self.play(Transform(expression, new_expression))
            self.wait(2)




    #########

    def get_dots_arrows_and_labels(self, numbers, color):
        dots = VGroup()
        arrows = VGroup()
        labels = VGroup()
        for number in numbers:
            point = self.number_line.number_to_point(number)
            dot = Dot(point)
            label = OldTex(str(number))
            label.scale(0.8)
            label.next_to(dot, UP, LARGE_BUFF)
            arrow = Arrow(label, dot, buff = SMALL_BUFF)
            VGroup(dot, label, arrow).set_color(color)
            dots.add(dot)
            arrows.add(arrow)
            labels.add(label)
        return dots, arrows, labels

    def introduce_dots_arrows_and_labels(self, dots, arrows, labels):
        if hasattr(self, "last_dots"):
            self.play(
                ReplacementTransform(self.last_dots, dots),
                ReplacementTransform(self.last_arrows, arrows),
                ReplacementTransform(self.last_labels, labels),
            )
        else:
            self.play(
                Write(labels),
                FadeIn(arrows, lag_ratio = 0.5),
                LaggedStartMap(
                    DrawBorderThenFill, dots,
                    stroke_width = 4,
                    stroke_color = YELLOW
                ),
                run_time = 2
            )
        self.last_dots = dots
        self.last_arrows = arrows
        self.last_labels = labels

    def get_chi_expression(self, numbers, color, num_terms = 4):
        truncated_numbers = numbers[:num_terms]
        output = str(chi_func(numbers[0]))
        result = OldTex(*it.chain(*[
            ["\\chi(", str(n), ")", "="]
            for n in truncated_numbers
        ] + [
            ["\\cdots =", output]
        ]))
        result.inputs = VGroup()
        for n in truncated_numbers:
            num_mob = result.get_part_by_tex(str(n), substring = False)
            num_mob.set_color(color)
            result.inputs.add(num_mob)
        result.set_color_by_tex(output, color, substring = False)
        return result

    def number_to_color(self, n):
        output = chi_func(n)
        if n == 1:
            return self.colors[0]
        elif n == -1:
            return self.colors[1]
        else:
            return self.colors[2]
