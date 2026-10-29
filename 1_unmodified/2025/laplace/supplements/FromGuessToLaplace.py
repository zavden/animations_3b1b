# ==============================================================================
# Scene:      FromGuessToLaplace
# Source:     videos/_2025/laplace/supplements.py (lines 866-931)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromGuessToLaplace.py FromGuessToLaplace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FromGuessToLaplace(InteractiveScene):
    def construct(self):
        # Words
        strategy = VGroup(
            Text("“Strategy”", fill_color=GREY_A, font_size=72),
            TexText("Guess $x(t) = e^{{s}t}$", t2c={"{s}": YELLOW}, fill_color=WHITE, font_size=72),
        )
        strategy.arrange(DOWN)
        self.add(strategy)
        return

        # Comment on it
        exp_rect = SurroundingRectangle(strategy[1]["x(t) = e^{{s}t}"], buff=SMALL_BUFF)
        exp_words = Text("Why?", font_size=42)
        exp_words.next_to(exp_rect, RIGHT, SMALL_BUFF)
        VGroup(exp_rect, exp_words).set_color(PINK)

        guess_rect = SurroundingRectangle(strategy[1]["Guess"], buff=SMALL_BUFF)
        guess_rect.match_height(exp_rect, stretch=True).match_y(exp_rect)
        guess_words = Text("Seems dumb", font_size=36)
        guess_words.next_to(guess_rect, DOWN, SMALL_BUFF)
        VGroup(guess_rect, guess_words).set_color(RED)

        self.play(LaggedStart(
            ShowCreation(guess_rect),
            FadeIn(guess_words, lag_ratio=0.1),
            ShowCreation(exp_rect),
            FadeIn(exp_words, lag_ratio=0.1),
            lag_ratio=0.25
        ))
        self.wait()

        # Transition to Laplace
        laplace = Tex(R"\int_0^\infty x(t) e^{-{s}t} dt", t2c={"{s}": YELLOW}, font_size=72)
        laplace.move_to(strategy[1])

        self.play(LaggedStart(
            LaggedStartMap(FadeOut, VGroup(strategy[1]["Guess"], guess_rect, guess_words), shift=DOWN, lag_ratio=0.1),
            TransformFromCopy(strategy[0]["S"][0], laplace[R"\int"][0]),
            TransformFromCopy(strategy[0]["e"][0], laplace[R"0"][0]),
            TransformFromCopy(strategy[0]["g"][0], laplace[R"\infty"][0]),
            FadeOut(strategy[0], lag_ratio=0.1),
            # Break
            FadeOut(VGroup(exp_rect, exp_words), 0.5 * LEFT, lag_ratio=0.1),
            FadeTransform(strategy[1]["x(t)"][0], laplace["x(t)"][0]),
            FadeTransform(strategy[1]["="][0], laplace["-"][0]),
            FadeTransform(strategy[1]["e"][-1], laplace["e"][0]),
            FadeTransform(strategy[1]["{s}t"][0], laplace["{s}t"][0]),
            Write(laplace["dt"][0]),
            lag_ratio=0.15,
            run_time=3,
        ))
        self.wait()

        # Label laplace
        laplace_rect = SurroundingRectangle(laplace)
        laplace_rect.set_color(BLUE)
        laplace_label = Text("Laplace Transform", font_size=72)
        laplace_label.next_to(laplace_rect, UP)
        laplace_label.match_color(laplace_rect)

        self.play(
            Write(laplace_label),
            ShowCreation(laplace_rect),
        )
        self.wait()
