# ==============================================================================
# Scene:      InitialFiveChooseThreeExample
# Source:     videos/_2018/eop/combinations.py (lines 198-405)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InitialFiveChooseThreeExample.py InitialFiveChooseThreeExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ApplyMethod(mob.scale, f, point): GL scale() takes the point as about_point, not as 2nd positional argument; pass {"about_point": point}
#   - in play(): last_ones.restore listed before ones.set_color (the 2018 method-merge in Scene.play swallowed a trailing restore as an argument of set_color, so it never ran)
# ==============================================================================

from manim_imports_ext import *

def get_stack(
    obj1, obj2, n, k,
    fixed_start = None,
    fixed_end = None,
    obj_to_obj_buff = SMALL_BUFF,
    vertical_buff = MED_SMALL_BUFF,
    ):
    stack = VGroup()
    for indices in it.combinations(list(range(n)), k):
        term = VGroup(*[
             obj1.copy() if i in indices else obj2.copy()
            for i in range(n)
        ])
        if fixed_start:
            term.add_to_back(fixed_start.copy())
        if fixed_end:
            term.add(fixed_end.copy())
        term.arrange(RIGHT, buff = obj_to_obj_buff)
        stack.add(term)
    stack.arrange(DOWN, buff = vertical_buff)
    return stack


def get_stacks(obj1, obj2, n, **kwargs):
    stacks = VGroup()
    for k in range(n+1):
        stacks.add(get_stack(obj1, obj2, n, k, **kwargs))
    stacks.arrange(
        RIGHT, 
        buff = MED_LARGE_BUFF,
        aligned_edge = DOWN
    )
    return stacks


class InitialFiveChooseThreeExample(Scene):
    CONFIG = {
        "n" : 5,
        "zero_color" : BLUE,
        "one_color" : PINK,
    }
    def construct(self):
        self.show_all_stacks()
        self.add_title()
        self.show_binomial_name()
        self.issolate_single_stack()
        self.count_chosen_stack()
        self.count_ways_to_fill_slots()
        self.walk_though_notation()
        self.emphasize_pattern_over_number()

    def show_all_stacks(self):
        stacks = get_stacks(
            self.get_obj1(), self.get_obj2(), self.n,
            vertical_buff = SMALL_BUFF
        )
        stacks.to_edge(DOWN, buff = MED_LARGE_BUFF)

        for stack in stacks:
            self.play(FadeIn(
                stack, 
                run_time = 0.2*len(stack),
                lag_ratio = 0.5
            ))
        self.wait()

        self.set_variables_as_attrs(stacks)

    def add_title(self):
        n = self.n
        stacks = self.stacks

        n_choose_k = OldTex("n \\choose k")
        n_choose_k_words = OldTexText("``n choose k''")
        nCk_group = VGroup(n_choose_k, n_choose_k_words)
        nCk_group.arrange(RIGHT)
        nCk_group.to_edge(UP)

        binomials = VGroup(*[
            OldTex("%d \\choose %d"%(n, k))
            for k in range(n+1)
        ])
        binomial_equations = VGroup()
        for k, binomial in enumerate(binomials):
            binomial.scale(0.75)
            number = OldTex(str(choose(n, k)))
            equation = VGroup(binomial, OldTex("="), number)
            equation.arrange(RIGHT, buff = SMALL_BUFF)
            equation.set_color(YELLOW)
            equation[1].set_color(WHITE)
            binomial_equations.add(equation)

        for stack, eq in zip(stacks, binomial_equations):
            eq.set_width(0.9*stack.get_width())
            eq.next_to(stack, UP)

        mover = VGroup()
        for eq in binomial_equations:
            point = VectorizedPoint(n_choose_k.get_center())
            group = VGroup(n_choose_k, point, point).copy()
            group.target = eq
            mover.add(group)

        self.play(FadeIn(nCk_group))
        self.play(LaggedStartMap(
            MoveToTarget, mover,
            run_time = 3,
        ))
        self.remove(mover)
        self.add(binomial_equations)
        self.wait()

        self.set_variables_as_attrs(
            n_choose_k, n_choose_k_words,
            binomial_equations
        )

    def show_binomial_name(self):
        new_words = OldTexText("``Binomial coefficients''")
        new_words.move_to(self.n_choose_k_words, LEFT)

        self.play(Transform(self.n_choose_k_words, new_words))
        self.wait(2)

    def issolate_single_stack(self):
        stack = self.stacks[3]
        equation = self.binomial_equations[3]

        to_fade = VGroup(*self.stacks)
        to_fade.add(*self.binomial_equations)
        to_fade.add(self.n_choose_k, self.n_choose_k_words)
        to_fade.remove(stack, equation)

        self.play(
            FadeOut(to_fade),
            # CHANGE: GL scale() takes the point as about_point (Cairo took it positionally)
            equation.scale, 1.5, {"about_point": equation.get_bottom()},
        )
        self.wait()
        for line in stack:
            ones = VGroup(*[mob for mob in line if "1" in mob.get_tex()])
            line.ones = ones
            self.play(LaggedStartMap(
                ApplyMethod, ones,
                lambda mob : (mob.set_color, YELLOW),
                rate_func = there_and_back,
                lag_ratio = 0.7,
                run_time = 1,
            ))

    def count_chosen_stack(self):
        stack = self.stacks[3]
        for i, line in enumerate(stack):
            number = OldTex(str(i+1))
            number.next_to(stack, LEFT)
            brace = Brace(VGroup(*stack[:i+1]), LEFT)
            number.next_to(brace, LEFT)
            line.save_state()
            line.set_color(YELLOW)
            self.add(number, brace)
            self.wait(0.25)
            self.remove(number, brace)
            line.restore()
        self.add(number, brace)
        self.wait()

        self.set_variables_as_attrs(
            stack_brace = brace,
            stack_count = number
        )

    def count_ways_to_fill_slots(self):
        lines = VGroup(*[Line(ORIGIN, 0.25*RIGHT) for x in range(5)])
        lines.arrange(RIGHT)
        lines.next_to(self.stacks[3], LEFT, LARGE_BUFF, UP)

        self.play(ShowCreation(lines))
        count = 1
        for indices in it.combinations(list(range(5)), 3):
            ones = VGroup(*[
                self.get_obj1().next_to(lines[i], UP)
                for i in indices
            ])
            num = OldTex(str(count))
            num.next_to(lines, DOWN)
            self.add(ones, num)
            self.wait(0.35)
            self.remove(ones, num)
            count += 1
        self.add(num, ones)
        self.wait()
        self.play(*list(map(FadeOut, [lines, num, ones])))

    def walk_though_notation(self):
        equation = self.binomial_equations[3]
        rect = SurroundingRectangle(equation[0])
        rect.set_color(WHITE)
        words = OldTexText("``5 choose 3''")
        words.next_to(rect, UP)

        self.play(Write(words))
        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.wait(2)

    def emphasize_pattern_over_number(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT)
        words = OldTexText("Remember the pattern \\\\ not the number")
        words.next_to(morty, UP)
        words.shift_onto_screen()

        self.play(FadeIn(morty))
        self.play(
            morty.change, "speaking",
            Write(words, run_time = 2)
        )
        self.play(
            Blink(morty),
            morty.change, "happy"
        )
        self.revert_to_original_skipping_status()
        last_ones = VGroup()
        last_ones.save_state()
        for x in range(2):
            for line in self.stacks[3]:
                ones = line.ones
                ones.save_state()
                # CHANGE: last_ones.restore moved first: the CL18-D play() method merge treats a trailing restore as an argument of the previous method
                self.play(
                    last_ones.restore,
                    ones.set_color, YELLOW,
                    morty.look_at, ones,
                    run_time = 0.25
                )
                last_ones = ones
            self.wait()

    ####

    def get_obj1(self):
        return OldTex("1").set_color(self.one_color)

    def get_obj2(self):
        return OldTex("0").set_color(self.zero_color)
