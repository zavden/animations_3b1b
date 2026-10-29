# ==============================================================================
# Scene:      EuclidProof
# Source:     videos/_2024/antp/main.py (lines 206-319)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EuclidProof.py EuclidProof -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class EuclidProof(InteractiveScene):
    def construct(self):
        # Suppose finite
        prime_sequence = Tex(R"2, 3, 5, \dots , p_n", font_size=72)
        prime_sequence.move_to(UP + LEFT)
        last = prime_sequence["p_n"]
        finite_words = Text("All primes (suppose finite)", font_size=60)
        finite_words.next_to(last, UR).shift(0.2 * UP)
        sequence_rect = SurroundingRectangle(prime_sequence)
        sequence_rect.set_stroke(YELLOW, 2)
        sequence_rect.set_stroke(YELLOW, 2)
        finite_words.next_to(sequence_rect, UP)
        finite_words.shift(RIGHT * (sequence_rect.get_x() - finite_words["All primes"].get_x()))

        last_arrow = Arrow(
            finite_words["prime"].get_corner(DL),
            last,
            path_arc=-PI / 3,
            buff=0.1
        )
        VGroup(finite_words, sequence_rect).set_color(YELLOW)

        self.add(prime_sequence)
        self.add(finite_words)
        self.add(sequence_rect)

        # Multiply, add 1, factor
        product = Tex(R"N = 2 \cdot 3 \cdot 5 \cdots p_n", font_size=72)
        product.next_to(prime_sequence, DOWN, LARGE_BUFF)

        plus_one = Tex("+1", font_size=72)
        plus_one.next_to(product, RIGHT, 0.2)
        plus_one.shift(0.05 * UP)
        N_mob = VGroup(product, plus_one)
        N_mob.match_x(prime_sequence)

        psc = prime_sequence.copy()
        self.play(
            TransformMatchingTex(
                psc,
                product,
                matched_pairs=[
                    (psc[","], product[R"\cdot"]),
                    (psc[R"\dots"], product[R"\cdots"]),
                ],
                run_time=1
            )
        )
        self.play(Write(plus_one))
        self.wait()

        # Factor
        N_rect = SurroundingRectangle(
            VGroup(product[2:], plus_one)
        )
        factor_arrow = Vector(DL)
        factor_arrow.next_to(N_rect, DOWN)
        factor_word = Text("Prime factors", font_size=60)
        factor_word.next_to(factor_arrow, RIGHT, buff=0)

        VGroup(N_rect, factor_arrow, factor_word).set_color(TEAL)

        factor_eq = Tex(R"N = q_1 \cdots q_k", font_size=72)
        factor_eq[R"q_1 \cdots q_k"].set_color(RED)
        factor_eq.next_to(product, DOWN, buff=1.5, aligned_edge=LEFT)

        self.play(
            FadeTransformPieces(product.copy(), factor_eq),
            FadeIn(N_rect),
            GrowArrow(factor_arrow),
            FadeIn(factor_word, 0.5 * DOWN),
        )
        self.wait(3)

        # Contradiction
        q_rect = SurroundingRectangle(factor_eq["q_1"], buff=0.1)
        q_rect.set_stroke(WHITE, 3)
        q_words = TexText(R"Cannot be in $\{2, 3, 5, \dots, p_n\}$", font_size=60)
        q_words.next_to(q_rect, UP, aligned_edge=LEFT)
        q_words.match_color(factor_eq[2])
        rect = SurroundingRectangle(Group(*(
            mob
            for mob in self.mobjects
            if isinstance(mob, StringMobject)
        )), buff=0.5)
        rect.set_stroke(WHITE, 3)
        rect.shift(0.35 * DOWN)
        rect.set_fill(RED, 0.1)
        cont_word = Text("Contradiction!", font_size=90)
        cont_word.next_to(rect, UP, buff=0.5, aligned_edge=RIGHT)
        cont_word.set_color(WHITE)

        self.play(
            Transform(N_rect, q_rect),
            FadeTransformPieces(factor_word, q_words),
            FadeOut(factor_arrow),
        )
        self.wait(4)
        self.play(
            FadeIn(rect),
            FadeIn(cont_word, 0.5 * UP),
        )
        self.wait()

    def infinite(self):
        # Interlude to show infinite
        inf_sequence = Tex(R"2, 3, 5, 7, 11, \dots", font_size=72)
        inf_sequence.move_to(prime_sequence, LEFT)
        inf_arrow = Vector(RIGHT)
        inf_arrow.next_to(inf_sequence, RIGHT, SMALL_BUFF)
        inf_words = Text("Infinite", font_size=60)
        inf_words.next_to(inf_arrow, DOWN, aligned_edge=LEFT)

        self.add(inf_sequence, inf_arrow, inf_words)
