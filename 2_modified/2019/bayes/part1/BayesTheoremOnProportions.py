# ==============================================================================
# Scene:      BayesTheoremOnProportions
# Source:     videos/_2019/bayes/part1.py (lines 4001-4107)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BayesTheoremOnProportions.py BayesTheoremOnProportions -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
#   - Group evidence and hypothesis by semantic probabilities, without old glyph indices.
# ==============================================================================

# CHANGE: group evidence/hypothesis by the semantic terms of get_bayes_formula.
from manim_imports_ext import *

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


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class Person(SVGMobject):
    CONFIG = {
        "file_name": "person",
        "height": 1.5,
        "stroke_width": 0,
        "fill_opacity": 1,
        "fill_color": GREY_B,
    }


class BayesTheoremOnProportions(Scene):
    def construct(self):
        # Place on top of visuals from "HeartOfBayes"
        formula = get_bayes_formula()
        formula.scale(1.5)

        title = OldTexText("Bayes' theorem")
        title.scale(2)
        title.next_to(formula, UP, LARGE_BUFF)
        group = VGroup(formula, title)

        equals = OldTex("=")
        equals.next_to(formula, RIGHT)
        h_line = Line(LEFT, RIGHT)
        h_line.set_width(4)
        h_line.next_to(equals, RIGHT)
        h_line.set_stroke(WHITE, 3)

        self.add(group)
        self.wait()
        self.play(
            group.to_edge, LEFT,
            MaintainPositionRelativeTo(equals, group),
            VFadeIn(equals),
            MaintainPositionRelativeTo(h_line, group),
            VFadeIn(h_line),
        )

        # People
        people = VGroup(*[Person() for x in range(7)])
        people.arrange(RIGHT)
        people.match_width(h_line)
        people.next_to(h_line, DOWN)
        people.set_color(BLUE_E)
        people[:3].set_color(GREEN)
        num_people = people[:3].copy()

        self.play(FadeIn(people, lag_ratio=0.1))
        self.play(num_people.next_to, h_line, UP)
        self.wait(0.5)

        # Diagrams
        diagram = BayesDiagram(0.25, 0.5, 0.2)
        diagram.set_width(0.7 * h_line.get_width())
        diagram.next_to(h_line, DOWN)
        diagram.hne_rect.set_fill(opacity=0.1)
        diagram.nhne_rect.set_fill(opacity=0.1)
        num_diagram = diagram.deepcopy()
        num_diagram.next_to(h_line, UP)
        num_diagram.nhe_rect.set_fill(opacity=0.1)
        low_diagram_rects = VGroup(diagram.he_rect, diagram.nhe_rect)
        top_diagram_rects = VGroup(num_diagram.he_rect)

        self.play(
            FadeOut(people),
            FadeOut(num_people),
            FadeIn(diagram),
            FadeIn(num_diagram),
        )
        self.wait()

        # Circle each part
        E_part = VGroup(formula[4], formula.p_evidence).copy()
        H_part = VGroup(formula[2], formula.prior, formula.likelihood).copy()

        E_arrow = Vector(UP, color=BLUE)
        E_arrow.next_to(E_part[0], DOWN)
        E_words = OldTexText(
            "...among cases where\\\\$E$ is True",
            tex_to_color_map={"$E$": BLUE},
        )
        E_words.next_to(E_arrow, DOWN)
        H_arrow = Vector(DOWN, color=YELLOW)
        H_arrow.next_to(H_part[0], UP)
        H_words = OldTexText(
            "How often is\\\\$H$ True...",
            tex_to_color_map={"$H$": YELLOW},
        )
        H_words.next_to(H_arrow, UP)

        denom_rect = SurroundingRectangle(E_part[1:], color=BLUE)
        numer_rect = SurroundingRectangle(H_part[1:], color=YELLOW)

        self.play(
            formula.set_opacity, 0.5,
            ApplyMethod(
                E_part.set_stroke, YELLOW, 3, {"background": True},
                rate_func=there_and_back,
            ),
            FadeIn(denom_rect),
            ShowCreation(E_arrow),
            FadeIn(E_words, UP),
            low_diagram_rects.set_stroke, TEAL, 3,
        )
        self.wait()
        self.play(
            FadeOut(E_part),
            FadeIn(H_part),
            FadeOut(denom_rect),
            FadeIn(numer_rect),
            ShowCreation(H_arrow),
            FadeIn(H_words, DOWN),
            FadeOut(title, UP),
            low_diagram_rects.set_stroke, WHITE, 1,
            top_diagram_rects.set_stroke, YELLOW, 3,
        )
        self.wait()
