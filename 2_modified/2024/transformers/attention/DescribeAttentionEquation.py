# ==============================================================================
# Scene:      DescribeAttentionEquation
# Source:     videos/_2024/transformers/attention.py (lines 1850-2080)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl DescribeAttentionEquation.py DescribeAttentionEquation -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/AttentionPaperStill.png  (_lib/assets/generated/2024/transformers/make_attention_images.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class DescribeAttentionEquation(InteractiveScene):
    def construct(self):
        # Stage image
        image = ImageMobject("AttentionPaperStill")
        image.set_height(FRAME_HEIGHT)
        self.add(image)

        # Add equation
        equation = Tex(R"\text{Attention}(Q, K, V) = \text{softmax}\left({K^T Q \over \sqrt{d_k}}\right) V")
        equation.set_height(1.06929)
        equation.move_to([-0.41406, 1.177, 0])

        self.play(
            FadeIn(equation),
            FadeOut(image),
        )
        self.wait()

        # Show Q and K arrays
        syms = ["Q", "K"]
        colors = [YELLOW, TEAL]
        q_array, k_array = arrays = VGroup(
            self.get_array_representation(sym, color)
            for sym, color in zip(syms, colors)
        )
        arrays.arrange(RIGHT, buff=1.5)
        arrays.next_to(equation, DOWN, buff=1.0)

        lil_rects = VGroup()
        rect_lines = VGroup()
        big_rects = VGroup()
        for arr, sym, color in zip(arrays, syms, colors):
            lil_rect = SurroundingRectangle(equation["Q"][0])
            lil_rect.match_x(equation[sym][0])
            big_rect = SurroundingRectangle(arr)
            lines = VGroup(
                Line(lil_rect.get_corner(DOWN + v), big_rect.get_corner(UP + v))
                for v in [LEFT, RIGHT]
            )
            VGroup(lil_rect, big_rect, lines).set_stroke(color, 2)
            lil_rects.add(lil_rect)
            rect_lines.add(lines)
            big_rects.add(big_rect)

            self.play(
                ShowCreation(lil_rect),
                equation[sym].animate.set_color(color),
            )
            self.play(
                TransformFromCopy(lil_rect, big_rect),
                FadeInFromPoint(arr, lil_rect.get_center()),
                ShowCreation(lines, lag_ratio=0)
            )
        self.wait()

        # Highlight numerator
        num_rect = SurroundingRectangle(equation["K^T Q"])
        num_rect.set_stroke(BLUE, 2)

        self.play(
            ReplacementTransform(lil_rects[0], num_rect),
            ReplacementTransform(lil_rects[1], num_rect),
            FadeOut(rect_lines)
        )
        self.wait()

        # Arrange for grid
        frame = self.frame
        qs = q_array[1]
        ks = k_array[1]
        q_array.remove(qs)
        k_array.remove(ks)

        h_buff = 0.8
        v_buff = 0.6

        qs.target = qs.generate_target()
        qs.target.scale(0.75)
        qs.target.arrange(RIGHT, buff=h_buff)
        qs.target.next_to(equation, DOWN, buff=0.75)

        ks.target = ks.generate_target()
        ks.target.scale(0.75)
        ks.target.arrange(DOWN, buff=MED_LARGE_BUFF)
        ks.target[-2].rotate(PI / 2)
        ks.target.next_to(qs.target, DL, buff=v_buff)

        self.play(
            frame.animate.move_to(1.5 * DOWN),
            FadeOut(q_array),
            FadeOut(k_array),
            MoveToTarget(qs),
            MoveToTarget(ks),
            big_rects[0].animate.surround(qs.target).set_stroke(opacity=0),
            big_rects[1].animate.surround(ks.target).set_stroke(opacity=0),
            run_time=2
        )

        # Add grid lines
        grid = VGroup(qs, ks)

        v_lines = Line(UP, DOWN).match_height(grid).scale(1.1).replicate(len(qs) + 1)
        for v_line, mob in zip(v_lines, (ks, *qs)):
            v_line.next_to(mob, RIGHT, buff=h_buff / 2)
            v_line.align_to(qs, UP)

        h_lines = Line(LEFT, RIGHT).match_width(grid).scale(1.1).replicate(len(ks) + 1)
        for h_line, mob in zip(h_lines, (qs, *ks)):
            h_line.next_to(mob, DOWN, buff=v_buff / 2)
            h_line.align_to(ks, LEFT)

        VGroup(v_lines, h_lines).set_stroke(GREY_B, 1)

        grid.add(v_lines, h_lines)

        self.play(
            FadeIn(h_lines, lag_ratio=0.1),
            FadeIn(v_lines, lag_ratio=0.1),
            ks[-2].animate.match_y(h_lines[-3:-1]),
        )

        # Dot products
        dot_prods = VGroup()
        for q in qs:
            for k in ks:
                dot = Tex(".")
                dot.match_x(q)
                dot.match_y(k)
                dot_prod = VGroup(q.copy(), dot, k.copy())
                dot_prod.target = dot_prod.generate_target()
                dot_prod.target.arrange(RIGHT, buff=SMALL_BUFF)
                dot_prod.target.scale(0.7)
                dot_prod.target.move_to(dot)
                if len(q) == 3:
                    dot_prod.target[1:].scale(0)
                    for mob in dot_prod.target:
                        mob.move_to(dot)
                elif len(k) == 3:
                    dot_prod.target[:-1].scale(0)
                    for mob in dot_prod.target:
                        mob.move_to(dot)
                dot.set_opacity(0)
                dot_prods.add(dot_prod)

        self.play(
            LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.01),
            run_time=3
        )
        self.wait()

        # Add sqrt to denominator
        sqrt_part = equation[R"\over \sqrt{d_k}"][0]

        denoms = VGroup()
        for dot_prod in dot_prods:
            dot_prod.target = dot_prod.generate_target()
            if 3 in [len(dot_prod[0]), len(dot_prod[2])]:
                continue
            denom = sqrt_part.copy()
            denom.set_fill(opacity=0.9)
            denom.match_width(dot_prod)
            denom.move_to(dot_prod.get_center(), UP)
            dot_prod.target.next_to(denom, UP, buff=SMALL_BUFF)
            VGroup(dot_prod.target, denom).scale(0.75)
            denoms.add(denom)

        self.play(num_rect.animate.surround(equation[R"K^T Q \over \sqrt{d_k}"]))
        self.play(
            LaggedStartMap(MoveToTarget, dot_prods, lag_ratio=0.05, time_span=(1, 3)),
            LaggedStart(
                (TransformFromCopy(sqrt_part, denom)
                for denom in denoms),
                lag_ratio=0.01,
            ),
            run_time=3
        )
        self.wait()

        # Highlight softmax
        self.play(
            num_rect.animate.surround(equation[R"\text{softmax}\left({K^T Q \over \sqrt{d_k}}\right)"])
        )
        self.wait()

        # Mention V
        v_parts = equation["V"]
        v_rects = VGroup(map(SurroundingRectangle, v_parts))
        v_rects.set_stroke(RED, 3)

        self.play(
            ReplacementTransform(VGroup(num_rect), v_rects),
            v_parts.animate.set_color(RED),
        )
        self.wait()

    def get_array_representation(self, sym, color=WHITE, length=7):
        template = Tex(f"{sym}_0")
        template.set_fill(color)
        substr = template.make_number_changeable(0)
        terms = VGroup()
        term_lines = VGroup()
        term_groups = VGroup()
        for n in range(1, length + 1):
            if n == length:
                substr.become(Tex("n").replace(substr))
            else:
                substr.set_value(n)
            substr.set_color(color)
            term = template.copy()
            lines = Line(ORIGIN, 0.5 * UP).replicate(2)
            lines.arrange(DOWN, buff=term.get_height() + 2 * SMALL_BUFF)
            lines.move_to(term)
            term_lines.add(lines)
            terms.add(term)
            term_groups.add(VGroup(term, lines))
        term_groups.arrange(RIGHT, buff=MED_SMALL_BUFF)

        dots = Tex(R"\dots")
        dots.replace(terms[-2], dim_to_match=0)
        terms.replace_submobject(length - 2, dots)
        term_groups.remove(term_groups[-2])

        brackets = Tex("[]")
        brackets.stretch(1.5, 1)
        brackets.set_height(term_groups.get_height() + MED_SMALL_BUFF)
        for bracket, vect in zip(brackets, [LEFT, RIGHT]):
            bracket.next_to(terms, vect, SMALL_BUFF)

        result = VGroup(brackets, terms, term_lines)

        return result
