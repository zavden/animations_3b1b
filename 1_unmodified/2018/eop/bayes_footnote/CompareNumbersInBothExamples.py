# ==============================================================================
# Scene:      CompareNumbersInBothExamples
# Source:     videos/_2018/eop/bayes_footnote.py (lines 1341-1385)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareNumbersInBothExamples.py CompareNumbersInBothExamples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareNumbersInBothExamples(Scene):
    def construct(self):
        v_line = Line(UP, DOWN).scale(FRAME_Y_RADIUS)
        v_line.shift(MED_LARGE_BUFF*LEFT)
        h_line = Line(LEFT, RIGHT).scale(FRAME_X_RADIUS)
        h_line.to_edge(UP, buff = 1.25*LARGE_BUFF)
        titles = VGroup()
        for word, vect in ("Disease", LEFT), ("Telepathy", RIGHT):
            title = OldTexText("%s example"%word)
            title.shift(vect*FRAME_X_RADIUS/2.0)
            title.to_edge(UP)
            titles.add(title)
        priors = VGroup(*[
            OldTex(
                "P(", "\\text{%s}"%s, ")", "= 1/1{,}000}"
            )
            for s in ("Sick", "Powers")
        ])
        likelihoods = VGroup(*[
            OldTex(
                "P(", "\\text{%s}"%s1, "|", 
                "\\text{Not }", "\\text{%s}"%s2, ")",
                "=", "1/100"
            )
            for s1, s2 in [("+", "Sick"), ("Correct", "Powers")]
        ])
        priors.next_to(likelihoods, UP, LARGE_BUFF)
        for group in priors, likelihoods:
            for mob, vect in zip(group, [LEFT, RIGHT]):
                mob.set_color_by_tex("Sick", BLUE)
                mob.set_color_by_tex("Powers", BLUE)
                mob.set_color_by_tex("+", GREEN)
                mob.set_color_by_tex("Correct", GREEN)
                mob.scale(0.8)
                mob.shift(vect*FRAME_X_RADIUS/2)

        self.play(
            LaggedStartMap(FadeIn, titles, lag_ratio = 0.7),
            *list(map(ShowCreation, [h_line, v_line]))
        )
        self.wait()
        self.play(FadeIn(priors))
        self.wait()
        self.play(FadeIn(likelihoods))
        self.wait(3)
