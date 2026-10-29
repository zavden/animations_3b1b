# ==============================================================================
# Scene:      SumsToPowerOf2
# Source:     videos/_2018/eop/combinations.py (lines 3298-3452)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SumsToPowerOf2.py SumsToPowerOf2 -w -m --fps 15
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


class SumsToPowerOf2(Scene):
    CONFIG = {
        "n" : 5,
        "alt_n" : 7,
    }
    def construct(self):
        self.setup_stacks()
        self.count_32()
        self.show_sum_as_n_choose_k()
        self.show_alternate_sum()

    def setup_stacks(self):
        stacks = get_stacks(
            OldTex("1").set_color(PINK),
            OldTex("0").set_color(BLUE),
            n = self.n,
            vertical_buff = SMALL_BUFF,
        )
        stacks.to_corner(DOWN+LEFT)
        numbers = VGroup(*[
            OldTex(str(choose(self.n, k)))
            for k in range(self.n + 1)
        ])
        for number, stack in zip(numbers, stacks):
            number.next_to(stack, UP)

        self.play(
            LaggedStartMap(FadeIn, stacks),
            LaggedStartMap(FadeIn, numbers),
        )
        self.wait()

        self.set_variables_as_attrs(stacks, numbers)

    def count_32(self):
        lines = VGroup(*it.chain(*self.stacks))
        rhs = OldTex("= 2^{%d}"%self.n)
        rhs.to_edge(UP, buff = LARGE_BUFF)
        rhs.to_edge(RIGHT, buff = 2)

        numbers = self.numbers.copy()
        numbers.target = VGroup(*[
            OldTex("{%d \\choose %d}"%(self.n, k))
            for k in range(self.n + 1)
        ])
        plusses = VGroup(*[Tex("+") for n in numbers])
        plusses.remove(plusses[-1])
        plusses.add(OldTex("="))
        sum_group = VGroup(*it.chain(*list(zip(
            numbers.target, plusses
        ))))
        sum_group.arrange(RIGHT, SMALL_BUFF)
        sum_group.next_to(numbers, UP, LARGE_BUFF)
        sum_group.shift(MED_LARGE_BUFF*RIGHT)

        for i, line in zip(it.count(1), lines):
            line_copy = line.copy().set_color(YELLOW)
            number = Integer(i)
            number.scale(1.5)
            number.to_edge(UP)
            VGroup(number, line_copy).set_color(YELLOW)
            self.add(line_copy, number)
            self.wait(0.15)
            self.remove(line_copy, number)
        sum_result = number
        self.add(sum_result)
        self.wait()

        sum_result.target = OldTex(str(2**self.n))
        sum_result.target.set_color(sum_result.get_color())
        sum_result.target.next_to(sum_group, RIGHT)
        rhs.next_to(sum_result.target, RIGHT, aligned_edge = DOWN)
        self.play(
            MoveToTarget(sum_result),
            MoveToTarget(numbers),
            Write(plusses),
            Write(rhs),
        )
        self.wait()

        self.set_variables_as_attrs(
            plusses, sum_result, rhs,
            n_choose_k_terms = numbers
        )

    def show_sum_as_n_choose_k(self):
        numbers = self.numbers
        plusses = self.plusses
        n_choose_k_terms = self.n_choose_k_terms
        rhs = VGroup(self.sum_result, self.rhs)
        n = self.n


        fractions = self.get_fractions(n)
        plusses.generate_target()
        sum_group = VGroup(*it.chain(*list(zip(
            fractions, plusses.target
        ))))
        sum_group.arrange(RIGHT, buff = 2*SMALL_BUFF)
        sum_group.next_to(rhs, LEFT)
        sum_group.shift(0.5*SMALL_BUFF*DOWN)

        self.play(
            Transform(n_choose_k_terms, fractions),
            MoveToTarget(plusses),
            lag_ratio = 0.5,
            run_time = 2
        )
        self.wait()

    def show_alternate_sum(self):
        fractions = self.get_fractions(self.alt_n)
        fractions.remove(*fractions[4:-1])
        fractions.submobjects.insert(4, OldTex("\\cdots"))
        plusses = VGroup(*[
            OldTex("+") for f in fractions[:-1]
        ] + [Tex("=")])
        sum_group = VGroup(*it.chain(*list(zip(
            fractions, plusses
        ))))
        sum_group.arrange(RIGHT)
        sum_group.next_to(
            self.n_choose_k_terms, DOWN,
            aligned_edge = LEFT, buff = LARGE_BUFF
        )
        sum_group.shift(SMALL_BUFF*DOWN)
        rhs = OldTex(
            str(2**self.alt_n), 
            "=", "2^{%d}"%(self.alt_n)
        )
        rhs[0].set_color(YELLOW)
        rhs.next_to(sum_group, RIGHT)

        self.play(
            LaggedStartMap(FadeOut, self.stacks),
            LaggedStartMap(FadeOut, self.numbers),
            LaggedStartMap(FadeIn, sum_group),
        )
        self.play(LaggedStartMap(FadeIn, rhs))
        self.wait(2)

    ####

    def get_fractions(self, n):
        fractions = VGroup(OldTex("1"))
        dot_str = " \\!\\cdot\\! "
        for k in range(1, n+1):
            ts = str(n)
            bs = "1"
            for i in range(1, k):
                ts += dot_str + str(n-i)
                bs += dot_str + str(i+1)
            fraction = OldTex("{%s \\over %s}"%(ts, bs))
            fractions.add(fraction)
        return fractions
