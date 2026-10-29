# ==============================================================================
# Scene:      PowerRuleAlgebra
# Source:     videos/_2017/eoc/chapter3.py (lines 1411-1583)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl PowerRuleAlgebra.py PowerRuleAlgebra -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter3.py -----

DERIVATIVE_COLOR = VELOCITY_COLOR


class PowerRuleAlgebra(Scene):
    CONFIG = {
        "dx_color" : YELLOW,
        "x_color" : BLUE,
    }
    def construct(self):
        x_to_n = OldTex("x^n")
        down_arrow = Arrow(UP, DOWN, buff = MED_LARGE_BUFF)
        paren_strings = ["(", "x", "+", "dx", ")"]
        x_dx_to_n = OldTex(*paren_strings +["^n"])
        equals = OldTex("=")
        equals2 = OldTex("=")
        full_product = OldTex(
            *paren_strings*3+["\\cdots"]+paren_strings
        )

        x_to_n.set_color(self.x_color)
        for mob in x_dx_to_n, full_product:
            mob.set_color_by_tex("dx", self.dx_color)
            mob.set_color_by_tex("x", self.x_color)

        nudge_group = VGroup(x_to_n, down_arrow, x_dx_to_n)
        nudge_group.arrange(DOWN)
        nudge_group.to_corner(UP+LEFT)
        down_arrow.next_to(x_to_n[0], DOWN)
        equals.next_to(x_dx_to_n)
        full_product.next_to(equals)
        equals2.next_to(equals, DOWN, 1.5*LARGE_BUFF)

        nudge_brace = Brace(x_dx_to_n, DOWN)
        nudged_output = nudge_brace.get_text("Nudged \\\\ output")
        product_brace = Brace(full_product, UP)
        product_brace.add(product_brace.get_text("$n$ times"))

        self.add(x_to_n)
        self.play(ShowCreation(down_arrow))
        self.play(
            FadeIn(x_dx_to_n),
            GrowFromCenter(nudge_brace),
            GrowFromCenter(nudged_output)
        )
        self.wait()
        self.play(
            Write(VGroup(equals, full_product)),
            GrowFromCenter(
                product_brace,
                rate_func = squish_rate_func(smooth, 0.6, 1)
            ),
            run_time = 3
        )
        self.wait()
        self.workout_product(equals2, full_product)

    def workout_product(self, equals, full_product):
        product_part_tex_pairs = list(zip(full_product, full_product.expression_parts))
        xs, dxs = [
            VGroup(*[
                submob
                for submob, tex in product_part_tex_pairs
                if tex == target_tex
            ])
            for target_tex in ("x", "dx")
        ]

        x_to_n = OldTex("x^n")
        extra_stuff = OldTex("+(\\text{Multiple of }\\, dx^2)")
        # extra_stuff.scale(0.8)
        VGroup(*extra_stuff[-4:-2]).set_color(self.dx_color)

        x_to_n.next_to(equals, RIGHT, align_using_submobjects = True)
        x_to_n.set_color(self.x_color)

        xs_copy = xs.copy()
        full_product.save_state()
        self.play(full_product.set_color, WHITE)
        self.play(xs_copy.set_color, self.x_color)
        self.play(
            Write(equals),
            Transform(xs_copy, x_to_n)
        )
        self.wait()
        brace, derivative_term = self.pull_out_linear_terms(
            x_to_n, product_part_tex_pairs, xs, dxs
        )
        self.wait()

        circle = Circle(color = DERIVATIVE_COLOR)
        circle.replace(derivative_term, stretch = True)
        circle.scale(1.4)
        circle.rotate(
            Line(
                derivative_term.get_corner(DOWN+LEFT),
                derivative_term.get_corner(UP+RIGHT),
            ).get_angle()
        )

        extra_stuff.next_to(brace, aligned_edge = UP)

        self.play(Write(extra_stuff), full_product.restore)
        self.wait()
        self.play(ShowCreation(circle))
        self.wait()

    def pull_out_linear_terms(self, x_to_n, product_part_tex_pairs, xs, dxs):
        last_group = None
        all_linear_terms = VGroup()
        for dx_index, dx in enumerate(dxs):
            if dx is dxs[-1]:
                v_dots = OldTex("\\vdots")
                v_dots.next_to(last_group[0], DOWN)
                h_dots_list = [
                    submob
                    for submob, tex in product_part_tex_pairs
                    if tex == "\\cdots"
                ]
                h_dots_copy = h_dots_list[0].copy()
                self.play(ReplacementTransform(
                    h_dots_copy, v_dots,
                ))
                last_group.add(v_dots)
                all_linear_terms.add(v_dots)

            dx_copy = dx.copy()
            xs_copy = xs.copy()
            xs_copy.remove(xs_copy[dx_index])
            self.play(
                dx_copy.set_color, self.dx_color,
                xs_copy.set_color, self.x_color,
                rate_func = squish_rate_func(smooth, 0, 0.5)
            )

            dx_copy.generate_target()
            xs_copy.generate_target()
            target_list = [dx_copy.target] + list(xs_copy.target)
            target_list.sort(
                key=lambda m: m.get_center()[0]
            )
            dots = OldTex("+", ".", ".", "\\dots")
            for dot_index, dot in enumerate(dots):
                target_list.insert(2*dot_index, dot)
            group = VGroup(*target_list)
            group.arrange(RIGHT, SMALL_BUFF)
            if last_group is None:
                group.next_to(x_to_n, RIGHT)
            else:
                group.next_to(last_group, DOWN, aligned_edge = LEFT)
            last_group = group

            self.play(
                MoveToTarget(dx_copy),
                MoveToTarget(xs_copy),
                Write(dots)
            )
            all_linear_terms.add(dx_copy, xs_copy, dots)

        all_linear_terms.generate_target()
        all_linear_terms.target.scale(0.7)
        brace = Brace(all_linear_terms.target, UP)
        compact = OldTex("+\\,", "n", "x^{n-1}", "\\,dx")
        compact.set_color_by_tex("x^{n-1}", self.x_color)
        compact.set_color_by_tex("\\,dx", self.dx_color)
        compact.next_to(brace, UP)
        brace.add(compact)
        derivative_term = VGroup(*compact[1:3])

        VGroup(brace, all_linear_terms.target).shift(
            x_to_n[0].get_right()+MED_LARGE_BUFF*RIGHT - \
            compact[0].get_left()
        )

        self.play(MoveToTarget(all_linear_terms))
        self.play(Write(brace, run_time = 1))
        return brace, derivative_term
