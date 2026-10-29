# ==============================================================================
# Scene:      FourDBorsukUlam
# Source:     videos/_2017/borsuk.py (lines 2435-2502)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FourDBorsukUlam.py FourDBorsukUlam -w -m --fps 15
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


class FourDBorsukUlam(GeneralizeBorsukUlam, PiCreatureScene):
    CONFIG = {
        "n_dims" : 4,
        "use_morty" : False,
    }
    def setup(self):
        GeneralizeBorsukUlam.setup(self)
        PiCreatureScene.setup(self)
        self.pi_creature.to_corner(DOWN+LEFT, buff = MED_SMALL_BUFF)

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

        brace = Brace(Line(ORIGIN, 5*RIGHT))
        brace.to_edge(RIGHT)
        brace_text = brace.get_text("Triplets of numbers")
        brace_text.shift_onto_screen()

        self.play(FadeIn(sphere_set))
        self.change_mode("confused")
        self.wait()
        self.play(
            ShowCreation(arrow),
            Write(f)
        )
        self.play(Write(output_space))
        self.wait()
        self.change_mode("maybe")
        self.wait(2)
        self.change_mode("pondering")
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.wait()
        self.play(*list(map(FadeOut, [brace, brace_text])))
        self.wait()
        self.play(
            FadeIn(lhs),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.play(
            ReplacementTransform(lhs.copy(), rhs),
            Write(eq)
        )
        self.wait(2)

    def get_sphere_set(self):
        sphere_set = GeneralizeBorsukUlam.get_sphere_set(self)
        brace = Brace(sphere_set)
        text = brace.get_text("Hypersphere in 4D")
        sphere_set.add(brace, text)
        return sphere_set
