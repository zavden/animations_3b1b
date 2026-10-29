# ==============================================================================
# Scene:      Rearrange
# Source:     videos/_2019/bayes/footnote.py (lines 416-537)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/bayes/part1.py
#
# Run from this folder:
#     manimgl Rearrange.py Rearrange -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/bayes/part1.py -----

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


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class LibrarianIcon(SVGMobject):
    CONFIG = {
        "file_name": "book",
        "stroke_width": 0,
        "fill_color": GREY_B,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 0.75,
    }



# ----- From _2019/bayes/footnote.py -----

TEX_TO_COLOR_MAP = {
    "A": YELLOW,
    "B": BLUE,
}


MID_COLOR = interpolate_color(BLUE_D, YELLOW, 0.5)


class ShowTwoPerspectives(Scene):
    CONFIG = {
        "pa": 1 / 3,
        "pb": 1 / 4,
        "p_both": 1 / 6,
        "diagram_height": 4,
    }

    def construct(self):
        # Ask about intersection
        formula = self.get_formula()

        venn_diagram = self.get_venn_diagram()
        venn_diagram.next_to(formula, DOWN, LARGE_BUFF)

        arrow = Arrow(
            formula[3].get_bottom(),
            venn_diagram.get_center(),
        )

        self.add(formula)
        self.play(
            formula[:3].set_opacity, 0.2,
            formula[-3:].set_opacity, 0.2,
        )
        for i in (0, 1):
            self.play(
                FadeIn(venn_diagram[0][i]),
                Write(venn_diagram[1][i]),
                run_time=1,
            )
        self.play(ShowCreation(arrow))
        self.wait()

        # Think with respect to A
        diagram1 = self.get_diagram1()
        diagram1.evidence_split.set_opacity(0)
        diagram1.hypothesis_split.set_opacity(1)
        diagram1.to_edge(RIGHT, LARGE_BUFF)
        diagram1.refresh_braces()

        d1_line = DashedLine(
            diagram1.h_rect.get_corner(UR),
            diagram1.h_rect.get_corner(DR),
        )
        d1_line.set_stroke(BLACK, 2)

        space_words = OldTexText(
            "Space of all\\\\possibilities"
        )
        space_words.match_width(diagram1.square)
        space_words.scale(0.9)
        space_words.move_to(diagram1.square)
        space_words.set_fill(BLACK)
        space_outline = SurroundingRectangle(diagram1.square, buff=0)
        space_outline.set_stroke(WHITE, 10)

        self.play(
            FadeOut(venn_diagram[0][1]),
            FadeOut(venn_diagram[1][1]),
            FadeOut(arrow),
            formula[4:6].set_opacity, 1,
        )
        diagram1.pa_label.update()
        self.play(
            FadeIn(diagram1.nh_rect),
            ReplacementTransform(
                venn_diagram[0][0],
                diagram1.h_rect,
            ),
            ReplacementTransform(
                venn_diagram[1][0],
                diagram1.pa_label.get_part_by_tex("A"),
            ),
            FadeIn(diagram1.h_brace),
            FadeIn(diagram1.pa_label[0]),
            FadeIn(diagram1.pa_label[2]),
            ShowCreation(d1_line),
        )
        self.add(diagram1.pa_label)
        self.wait()
        self.play(
            FadeIn(space_words),
            ShowCreation(space_outline),
        )
        self.play(
            FadeOut(space_words),
            FadeOut(space_outline),
        )
        self.wait()

        # Show B part
        B_rects = VGroup(diagram1.he_rect, diagram1.nhe_rect)
        B_rects.set_opacity(1)
        B_rects.set_sheen(0.2, UL)
        diagram1.nhe_rect.set_fill(BLUE_D)
        diagram1.he_rect.set_fill(MID_COLOR)
        diagram1.save_state()
        B_rects.stretch(0.001, 1, about_edge=DOWN)

        diagram1.he_brace.save_state()
        diagram1.he_brace.stretch(0.001, 1, about_edge=DOWN)

        self.add(diagram1.he_brace, diagram1.pba_label)
        self.add(diagram1, d1_line)
        self.play(
            Restore(diagram1),
            Restore(diagram1.he_brace),
            VFadeIn(diagram1.he_brace),
            VFadeIn(diagram1.pba_label),
            formula.pba.set_opacity, 1,
        )
        self.wait()

        # Show symmetric perspective
        diagram1_copy = diagram1.deepcopy()
        diagram2 = self.get_diagram2()
        d2_line = DashedLine(
            diagram2.b_rect.get_corner(UL),
            diagram2.b_rect.get_corner(UR),
        )
        d2_line.set_stroke(BLACK, 2)

        for rect in [diagram2.ba_rect, diagram2.nba_rect]:
            rect.save_state()
            rect.stretch(0.001, 0, about_edge=LEFT)

        self.play(
            diagram1_copy.move_to, diagram2,
            formula.pb.set_opacity, 1,
        )
        self.play(
            diagram1_copy.set_likelihood, self.pb,
            diagram1_copy.set_antilikelihood, self.pb,
            VFadeOut(diagram1_copy),
            FadeIn(diagram2),
            TransformFromCopy(formula.pb, diagram2.pb_label),
            FadeIn(diagram2.pb_brace),
            ShowCreation(d2_line),
        )
        self.wait()
        self.play(
            formula.pab.set_opacity, 1,
            formula.eq1.set_opacity, 1,
        )
        self.play(
            TransformFromCopy(formula.pab, diagram2.pab_label),
            FadeIn(diagram2.pab_brace),
            Restore(diagram2.ba_rect),
            Restore(diagram2.nba_rect),
        )
        self.wait()

    def get_formula(self):
        kw = {
            "tex_to_color_map": {
                "A": YELLOW,
                "B": BLUE,
            }
        }
        parts = VGroup(*[
            OldTex(tex, **kw)
            for tex in [
                "P(B)", "P(A|B)", "=",
                "P(A \\text{ and } B)",
                "=", "P(A)", "P(B|A)",
            ]
        ])
        attrs = [
            "pb", "pab", "eq1", "p_both", "eq2", "pa", "pba"
        ]
        for attr, part in zip(attrs, parts):
            setattr(parts, attr, part)

        parts.arrange(RIGHT, buff=SMALL_BUFF),
        parts.set_width(FRAME_WIDTH - 1)
        parts.center().to_edge(UP)
        return parts

    def get_venn_diagram(self):
        c1 = Circle(
            radius=2.5,
            stroke_width=2,
            stroke_color=YELLOW,
            fill_opacity=0.5,
            fill_color=YELLOW,
        )
        c1.flip(RIGHT)
        c1.rotate(3 * TAU / 8)
        c2 = c1.copy()
        c2.set_color(BLUE)
        c1.shift(LEFT)
        c2.shift(RIGHT)
        circles = VGroup(c1, c2)

        titles = VGroup(
            OldTex("A"),
            OldTex("B"),
        )
        for title, circle, vect in zip(titles, circles, [UL, UR]):
            title.match_color(circle)
            title.scale(2)
            title.next_to(
                circle.get_boundary_point(vect),
                vect,
                buff=SMALL_BUFF
            )

        return VGroup(circles, titles)

    def get_diagram1(self):
        likelihood = (self.p_both / self.pa)
        antilikelihood = (self.pb - self.p_both) / (1 - self.pa)
        diagram = BayesDiagram(self.pa, likelihood, antilikelihood)
        diagram.set_height(self.diagram_height)

        diagram.add_brace_attrs()
        kw = {"tex_to_color_map": TEX_TO_COLOR_MAP}
        diagram.pa_label = OldTex("P(A)", **kw)
        diagram.pba_label = OldTex("P(B|A)", **kw)
        diagram.pa_label.add_updater(
            lambda m: m.next_to(diagram.h_brace, DOWN, SMALL_BUFF),
        )
        diagram.pba_label.add_updater(
            lambda m: m.next_to(diagram.he_brace, LEFT, SMALL_BUFF),
        )

        return diagram

    def get_diagram2(self):
        pa = self.pa
        pb = self.pb
        p_both = self.p_both
        square = Square()
        square.set_stroke(WHITE, 1)
        square.set_fill(GREY_B, 1)
        square.set_height(self.diagram_height)

        b_rect = square.copy()
        b_rect.stretch(pb, 1, about_edge=DOWN)
        b_rect.set_fill(BLUE)
        b_rect.set_sheen(0.2, UL)

        nb_rect = square.copy()
        nb_rect.stretch(1 - pb, 1, about_edge=UP)

        ba_rect = b_rect.copy()
        ba_rect.stretch((p_both / pb), 0, about_edge=LEFT)
        ba_rect.set_fill(MID_COLOR)

        nba_rect = nb_rect.copy()
        nba_rect.stretch((pa - p_both) / (1 - pb), 0, about_edge=LEFT)
        nba_rect.set_fill(YELLOW)

        result = VGroup(
            square.set_opacity(0),
            b_rect, nb_rect,
            ba_rect, nba_rect,
        )
        result.b_rect = b_rect
        result.nb_rect = nb_rect
        result.ba_rect = ba_rect
        result.nba_rect = nba_rect

        pb_brace = Brace(b_rect, LEFT, buff=SMALL_BUFF)
        pab_brace = Brace(ba_rect, DOWN, buff=SMALL_BUFF)
        kw = {"tex_to_color_map": TEX_TO_COLOR_MAP}
        pb_label = OldTex("P(B)", **kw)
        pab_label = OldTex("P(A|B)", **kw)
        pb_label.next_to(pb_brace, LEFT, SMALL_BUFF)
        pab_label.next_to(pab_brace, DOWN, SMALL_BUFF)

        result.pb_brace = pb_brace
        result.pab_brace = pab_brace
        result.pb_label = pb_label
        result.pab_label = pab_label

        VGroup(
            result,
            pb_brace, pab_brace,
            pb_label, pab_label,
        ).to_edge(LEFT)

        return result


class Rearrange(ShowTwoPerspectives):
    def construct(self):
        formula = self.get_formula()
        pb, pab, eq1, p_both, eq2, pa, pba = formula
        over = OldTex("{\\qquad\\qquad \\over \\quad}")
        over.match_width(formula[:2])
        eq3 = eq1.copy()

        new_line = VGroup(
            formula.pb,
            formula.pab,
            eq3,
            formula.pa,
            formula.pba,
        )
        new_line.generate_target()
        new_line.target.arrange(RIGHT, buff=MED_SMALL_BUFF)
        new_line.target[0].shift(SMALL_BUFF * RIGHT)
        new_line.target[-1].shift(SMALL_BUFF * LEFT)
        new_line.target.center()
        eq3.set_opacity(0)

        eq1.generate_target()
        eq1.target.rotate(PI / 3)
        eq1.target.move_to(midpoint(
            p_both.get_corner(DL),
            new_line.target[0].get_corner(UR)
        ))
        eq2.generate_target()
        eq2.target.rotate(-PI / 3)
        eq2.target.move_to(midpoint(
            p_both.get_corner(DR),
            new_line.target[4].get_corner(UL)
        ))

        self.add(formula)
        self.play(
            MoveToTarget(new_line),
            MoveToTarget(eq1),
            MoveToTarget(eq2),
        )
        self.wait()

        over.move_to(VGroup(pa, pba))
        self.play(
            ApplyMethod(
                pb.next_to, over, DOWN,
                path_arc=30 * DEGREES,
            ),
            VGroup(pa, pba).next_to, over, UP,
            ShowCreation(over),
            FadeOut(VGroup(eq1, eq2))
        )
        self.wait(2)
        over.generate_target()
        over.target.next_to(eq3, LEFT)
        numer = VGroup(pb, pab)
        numer.generate_target()
        numer.target.arrange(RIGHT, buff=SMALL_BUFF)
        numer.target.next_to(over.target, UP)
        self.play(LaggedStart(
            MoveToTarget(over, path_arc=-30 * DEGREES),
            MoveToTarget(numer, path_arc=-30 * DEGREES),
            ApplyMethod(pa.next_to, over.target, DOWN),
            ApplyMethod(pba.next_to, eq3, RIGHT),
            lag_ratio=0.3,
        ))
        self.wait(2)

        # Numbers
        pb_brace = Brace(pb, UP, buff=SMALL_BUFF)
        pab_brace = Brace(pab, UP, buff=SMALL_BUFF)
        pa_brace = Brace(pa, DOWN, buff=SMALL_BUFF)

        pb_value = pb_brace.get_tex("(1/21)")
        pab_value = pab_brace.get_tex("(4/10)")
        pa_value = pa_brace.get_tex("(24/210)")

        braces = VGroup(pb_brace, pab_brace, pa_brace)
        values = VGroup(pb_value, pab_value, pa_value)

        self.play(
            LaggedStartMap(GrowFromCenter, braces, lag_ratio=0.3),
            LaggedStartMap(GrowFromCenter, values, lag_ratio=0.3),
            FadeOut(p_both),
        )
        self.wait()

        # Replace symbols
        mag = SVGMobject(file_name="magnifying_glass")
        mag.set_stroke(width=0)
        mag.set_fill(GREY, 1)
        mag.set_sheen(1, UL)

        Bs = VGroup(*[
            mob.get_part_by_tex("B")
            for mob in [pb, pab, pba]
        ])
        As = VGroup(*[
            mob.get_part_by_tex("A")
            for mob in [pab, pa, pba]
        ])
        books = VGroup(*[
            LibrarianIcon().replace(B, dim_to_match=0)
            for B in Bs
        ])
        books.set_color(YELLOW)

        mags = VGroup(*[
            mag.copy().replace(A)
            for A in As
        ])

        self.play(LaggedStart(*[
            ReplacementTransform(A, mag, path_arc=PI)
            for A, mag in zip(As, mags)
        ]))
        self.play(LaggedStart(*[
            ReplacementTransform(B, book, path_arc=PI)
            for B, book in zip(Bs, books)
        ]))
        self.wait()
