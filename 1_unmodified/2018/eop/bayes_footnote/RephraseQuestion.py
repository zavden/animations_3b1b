# ==============================================================================
# Scene:      RephraseQuestion
# Source:     videos/_2018/eop/bayes_footnote.py (lines 407-450)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RephraseQuestion.py RephraseQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RephraseQuestion(Scene):
    def construct(self):
        words = VGroup(*list(map(TexText, [
            r"1 in $1{,000}$ chance \\ of having disease",
            r"1 in $100$ \\ false positive rate.",
            r"""\underline{\phantom{1 in 10}} chance \\
                of having disease \\
                after testing positive.
            """,
        ])))
        words.arrange(RIGHT, buff = LARGE_BUFF)
        words.set_width(2*(FRAME_X_RADIUS - MED_LARGE_BUFF))

        prior = OldTexText("Prior")
        prior.set_color(GREEN)
        prior.next_to(words[0], UP, 1.5*LARGE_BUFF)
        prior_arrow = Arrow(prior, words[0])
        prior_arrow.set_color(prior.get_color())

        posterior = OldTexText("Posterior")
        posterior.next_to(words[2], UP)
        posterior.shift(
            (prior.get_center() - posterior.get_center())[1]*UP
        )
        posterior.set_color(YELLOW)
        posterior_arrow = Arrow(posterior, words[2])
        posterior_arrow.set_color(posterior.get_color())

        self.add(words[0])
        self.play(
            LaggedStartMap(FadeIn, prior),
            ShowCreation(prior_arrow),
            run_time = 1
        )
        self.wait()
        self.play(FadeIn(words[1]))
        self.wait()
        self.play(FadeIn(words[2]))
        self.play(
            LaggedStartMap(FadeIn, posterior),
            ShowCreation(posterior_arrow),
            run_time = 1
        )
        self.wait(2)
