# ==============================================================================
# Scene:      ParticularValuesUnhelpfulOverlay
# Source:     videos/_2021/shadows.py (lines 3907-3959)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ParticularValuesUnhelpfulOverlay.py ParticularValuesUnhelpfulOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ParticularValuesUnhelpfulOverlay(Scene):
    def construct(self):
        # Particular value
        expr = OldTex("P(\\theta =", "\\pi / 4", ")", "=", "0")
        expr.set_color_by_tex("\\pi / 4", YELLOW)
        brace = Brace(expr.get_part_by_tex("\\pi / 4"), UP, buff=SMALL_BUFF)
        brace.stretch(0.5, 1, about_edge=DOWN)
        words = Text("Some specific value", font_size=24)
        words.next_to(brace, UP, SMALL_BUFF)
        VGroup(brace, words).set_color(YELLOW)
        VGroup(expr, brace, words).to_corner(UR)

        self.play(FadeIn(expr, lag_ratio=1))
        self.play(
            GrowFromCenter(brace),
            FadeIn(words, shift=0.2 * UP),
        )
        self.wait()

        # Unhelpful
        question = OldTexText("What are you going\\\\to do with that?", font_size=24)
        question.next_to(expr, DOWN, LARGE_BUFF)
        arrow = Arrow(question, expr.get_part_by_tex("0"), buff=SMALL_BUFF)

        self.play(
            FadeIn(question),
            ShowCreation(arrow),
        )
        self.wait()

        # New expr
        range_expr = OldTex(
            "P(\\pi / 4 < \\theta < \\pi / 4 + \\Delta\\theta) > 0",
            tex_to_color_map={
                "\\pi / 4": YELLOW,
                "\\Delta\\theta": GREY_A,
            },
            font_size=40
        )
        range_expr.move_to(expr, RIGHT)
        new_brace = Brace(range_expr.slice_by_tex("\\pi / 4", ")"), UP, buff=SMALL_BUFF)
        new_words = Text("Range of values", font_size=24)
        new_words.next_to(new_brace, UP, SMALL_BUFF)
        VGroup(new_brace, new_words).set_color(YELLOW)

        self.play(
            FadeOut(question),
            FadeOut(arrow),
            TransformMatchingShapes(expr, range_expr),
            FadeTransform(brace, new_brace),
            FadeTransform(words, new_words),
        )
        self.wait()
