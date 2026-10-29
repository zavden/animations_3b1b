# ==============================================================================
# Scene:      ReprogrammingThought
# Source:     videos/_2019/bayes/part1.py (lines 4421-4520)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReprogrammingThought.py ReprogrammingThought -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
#   - Outline prior and likelihood using the semantic groups of get_bayes_formula.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject

HYPOTHESIS_COLOR = YELLOW


NOT_HYPOTHESIS_COLOR = GREY


EVIDENCE_COLOR1 = BLUE_C


EVIDENCE_COLOR2 = BLUE_E


NOT_EVIDENCE_COLOR1 = GREY


NOT_EVIDENCE_COLOR2 = GREY_D


def get_bayes_formula(expand_denominator=False):
    t2c = {
        "{H}": HYPOTHESIS_COLOR,
        "{\\neg H}": NOT_HYPOTHESIS_COLOR,
        "{E}": EVIDENCE_COLOR1,
    }
    isolate = ["P", "\\over", "=", "\\cdot", "+"]

    tex = "P({H} | {E}) = {P({H}) P({E} | {H}) \\over "
    if expand_denominator:
        tex += "P({H}) P({E} | {H}) + P({\\neg H}) \\cdot P({E} | {\\neg H})}"
    else:
        tex += "P({E})}"

    formula = OldTex(
        tex,
        tex_to_color_map=t2c,
        isolate=isolate,
    )

    # CHANGE: identify the probabilities by their LaTeX parts, without Cairo glyph indices that do
    # not match the OldTex groups of GL.
    starts = [i for i, part in enumerate(formula) if part.get_tex().strip() == "P"]

    def probability(index):
        start = starts[index]
        end = start + 1
        while end < len(formula) and ")" not in formula[end].get_tex():
            end += 1
        return formula[start:end + 1]

    formula.posterior = probability(0)
    formula.prior = probability(1)
    formula.likelihood = probability(2)
    if expand_denominator:
        formula.denom_prior = probability(3)
        formula.denom_likelihood = probability(4)
        formula.denom_anti_prior = probability(5)
        formula.denom_anti_likelihood = probability(6)
    else:
        formula.p_evidence = probability(3)

    return formula


class BayesDiagram(VGroup):
    CONFIG = {
        "height": 2,
        "square_style": {
            "fill_color": GREY_D,
            "fill_opacity": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "rect_style": {
            "stroke_color": WHITE,
            "stroke_width": 1,
            "fill_opacity": 1,
        },
        "hypothesis_color": HYPOTHESIS_COLOR,
        "not_hypothesis_color": NOT_HYPOTHESIS_COLOR,
        "evidence_color1": EVIDENCE_COLOR1,
        "evidence_color2": EVIDENCE_COLOR2,
        "not_evidence_color1": NOT_EVIDENCE_COLOR1,
        "not_evidence_color2": NOT_EVIDENCE_COLOR2,
        "prior_rect_direction": DOWN,
    }

    def __init__(self, prior, likelihood, antilikelihood, **kwargs):
        super().__init__(**kwargs)
        square = Square(side_length=self.height)
        square.set_style(**self.square_style)

        # Create all rectangles
        h_rect, nh_rect, he_rect, nhe_rect, hne_rect, nhne_rect = [
            square.copy().set_style(**self.rect_style)
            for x in range(6)
        ]

        # Add as attributes
        self.square = square
        self.h_rect = h_rect  # Hypothesis
        self.nh_rect = nh_rect  # Not hypothesis
        self.he_rect = he_rect  # Hypothesis and evidence
        self.hne_rect = hne_rect  # Hypothesis and not evidence
        self.nhe_rect = nhe_rect  # Not hypothesis and evidence
        self.nhne_rect = nhne_rect  # Not hypothesis and not evidence

        # Stretch the rectangles
        for rect in h_rect, he_rect, hne_rect:
            rect.stretch(prior, 0, about_edge=LEFT)
        for rect in nh_rect, nhe_rect, nhne_rect:
            rect.stretch(1 - prior, 0, about_edge=RIGHT)

        he_rect.stretch(likelihood, 1, about_edge=DOWN)
        hne_rect.stretch(1 - likelihood, 1, about_edge=UP)
        nhe_rect.stretch(antilikelihood, 1, about_edge=DOWN)
        nhne_rect.stretch(1 - antilikelihood, 1, about_edge=UP)

        # Color the rectangles
        h_rect.set_fill(self.hypothesis_color)
        nh_rect.set_fill(self.not_hypothesis_color)
        he_rect.set_fill(self.evidence_color1)
        hne_rect.set_fill(self.not_evidence_color1)
        nhe_rect.set_fill(self.evidence_color2)
        nhne_rect.set_fill(self.not_evidence_color2)

        # Add them
        self.hypothesis_split = VGroup(h_rect, nh_rect)
        self.evidence_split = VGroup(he_rect, hne_rect, nhe_rect, nhne_rect)

        # Don't add hypothesis split by default
        self.add(self.square, self.hypothesis_split, self.evidence_split)
        self.square.set_opacity(0)
        self.hypothesis_split.set_opacity(0)

    def add_brace_attrs(self, buff=SMALL_BUFF):
        braces = self.braces = self.create_braces(buff)
        self.braces_buff = buff
        attrs = [
            "h_brace",
            "nh_brace",
            "he_brace",
            "hne_brace",
            "nhe_brace",
            "nhne_brace",
        ]
        for brace, attr in zip(braces, attrs):
            setattr(self, attr, brace)
        return self

    def create_braces(self, buff=SMALL_BUFF):
        kw = {
            "buff": buff,
            "min_num_quads": 1,
        }
        return VGroup(
            Brace(self.h_rect, self.prior_rect_direction, **kw),
            Brace(self.nh_rect, self.prior_rect_direction, **kw),
            Brace(self.he_rect, LEFT, **kw),
            Brace(self.hne_rect, LEFT, **kw),
            Brace(self.nhe_rect, RIGHT, **kw),
            Brace(self.nhne_rect, RIGHT, **kw),
        )

    def refresh_braces(self):
        if hasattr(self, "braces"):
            self.braces.become(
                self.create_braces(self.braces_buff)
            )
        return self

    def set_prior(self, new_prior):
        p = new_prior
        q = 1 - p
        full_width = self.square.get_width()

        left_rects = [self.h_rect, self.he_rect, self.hne_rect]
        right_rects = [self.nh_rect, self.nhe_rect, self.nhne_rect]

        for group, vect, value in [(left_rects, LEFT, p), (right_rects, RIGHT, q)]:
            for rect in group:
                rect.set_width(
                    value * full_width,
                    stretch=True,
                    about_edge=vect,
                )

        self.refresh_braces()
        return self

    def general_set_likelihood(self, new_likelihood, low_rect, high_rect):
        height = self.square.get_height()

        low_rect.set_height(
            new_likelihood * height,
            stretch=True,
            about_edge=DOWN,
        )
        high_rect.set_height(
            (1 - new_likelihood) * height,
            stretch=True,
            about_edge=UP,
        )
        self.refresh_braces()
        return self

    def set_likelihood(self, new_likelihood):
        self.general_set_likelihood(
            new_likelihood,
            self.he_rect,
            self.hne_rect,
        )
        return self

    def set_antilikelihood(self, new_antilikelihood):
        self.general_set_likelihood(
            new_antilikelihood,
            self.nhe_rect,
            self.nhne_rect,
        )
        return self

    def copy(self):
        return self.deepcopy()


class ReprogrammingThought(Scene):
    CONFIG = {
        "camera_config": {
            "background_color": GREY_E,
        }
    }

    def construct(self):
        brain = SVGMobject("brain")
        brain.set_fill(GREY, 1)
        brain.set_sheen(1, UL)
        brain.set_stroke(width=0)

        arrow = DoubleArrow(ORIGIN, 3 * RIGHT)

        formula = get_bayes_formula()

        group = VGroup(brain, arrow, formula)
        group.arrange(RIGHT)
        group.center()

        q_marks = OldTex("???")
        q_marks.scale(1.5)
        q_marks.next_to(arrow, UP, SMALL_BUFF)

        kt = Group(
            ImageMobject("kahneman"),
            ImageMobject("tversky"),
        )
        kt.arrange(RIGHT)
        kt.set_height(2)
        kt.to_corner(UR)

        brain_outline = brain.copy()
        brain_outline.set_fill(opacity=0)
        brain_outline.set_stroke(TEAL, 4)

        self.play(FadeIn(brain, RIGHT))
        self.play(
            GrowFromCenter(arrow),
            LaggedStartMap(FadeInFromDown, q_marks[0]),
            run_time=1
        )
        self.play(FadeIn(formula, LEFT))
        self.wait()

        kw = {"run_time": 1, "lag_ratio": 0.3}
        self.play(LaggedStartMap(FadeInFromDown, kt, **kw))
        self.play(LaggedStartMap(FadeOut, kt, **kw))
        self.wait()

        self.add(brain)
        self.play(ShowCreationThenFadeOut(
            brain_outline,
            lag_ratio=0.01,
            run_time=2
        ))

        # Bubble
        bubble = ThoughtBubble()
        bubble.next_to(brain, UR, SMALL_BUFF)
        bubble.shift(2 * DOWN)

        diagram = BayesDiagram(0.25, 0.8, 0.5)
        diagram.set_height(2.5)
        diagram.move_to(bubble.get_bubble_center())

        group = VGroup(brain, arrow, q_marks, formula)

        self.play(
            DrawBorderThenFill(VGroup(*reversed(bubble))),
            group.shift, 2 * DOWN,
        )
        self.play(FadeIn(diagram))
        self.wait()
        self.play(
            q_marks.scale, 1.5,
            q_marks.space_out_submobjects, 1.5,
            q_marks.set_opacity, 0,
        )
        self.remove(q_marks)
        self.wait()

        # Move parts
        # CHANGE: outline the semantic probabilities, without including the equals sign or the fraction.
        prior_outline = formula.prior.copy()
        prior_outline.set_stroke(YELLOW, 5, background=True)
        like_outline = formula.likelihood.copy()
        like_outline.set_stroke(BLUE, 5, background=True)

        self.play(
            FadeIn(prior_outline),
            ApplyMethod(diagram.set_prior, 0.5, run_time=2)
        )
        self.play(FadeOut(prior_outline))
        self.play(
            FadeIn(like_outline),
            ApplyMethod(diagram.set_likelihood, 0.2, run_time=2),
        )
        self.play(FadeOut(like_outline))
        self.wait()
