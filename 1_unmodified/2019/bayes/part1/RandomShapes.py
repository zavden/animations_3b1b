# ==============================================================================
# Scene:      RandomShapes
# Source:     videos/_2019/bayes/part1.py (lines 3124-3166)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RandomShapes.py RandomShapes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

HYPOTHESIS_COLOR = YELLOW


NOT_HYPOTHESIS_COLOR = GREY


EVIDENCE_COLOR1 = BLUE_C


EVIDENCE_COLOR2 = BLUE_E


NOT_EVIDENCE_COLOR1 = GREY


NOT_EVIDENCE_COLOR2 = GREY_D


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


class RandomShapes(Scene):
    def construct(self):
        diagram = BayesDiagram(0.1, 0.4, 0.1)
        diagram.set_height(3)

        e_part = VGroup(diagram.he_rect, diagram.nhe_rect).copy()
        e_part.set_fill(BLUE)

        circle = Circle()
        circle.set_fill(RED, 0.5)
        circle.set_stroke(RED, 2)
        circle.move_to(diagram)

        tri = Polygon(UP, ORIGIN, RIGHT)
        tri.match_height(diagram)
        tri.set_fill(PURPLE, 0.5)
        tri.set_stroke(PURPLE, 2)
        tri.move_to(diagram)

        h_rect = diagram.h_rect
        h_rect.set_fill(YELLOW, 1)

        pi = OldTex("\\pi")
        pi.set_height(2)
        pi.set_stroke(GREEN, 2)
        pi.set_fill(GREEN, 0.5)

        events = VGroup(
            e_part,
            h_rect,
            circle,
            pi,
            tri,
        )

        last = VMobject()
        for event in events:
            self.play(
                FadeIn(event),
                FadeOut(last)
            )
            self.wait()
            last = event
