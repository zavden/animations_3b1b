# ==============================================================================
# Scene:      CreateFormulaFromDiagram
# Source:     videos/_2019/bayes/part1.py (lines 2218-2825)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CreateFormulaFromDiagram.py CreateFormulaFromDiagram -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
#   - Accept ManimGL's copy(deep=) and keep the deep copy of the parts of the Bayes diagram.
#   - Group the probabilities and the denominator of the formula by their LaTeX meaning, avoiding Cairo indices that overlapped terms and cut off the result.
#   - Keep the column order and Cairo spacing in the grid so that the indices of people and cells correspond to the right region.
#   - Update GL's family and bounds when replacing the count glyph with a person using replace_submobject.
#   - Limit the width of the expanded denominator to the space available inside the frame.
#   - Locally reduce the character Π to height 2 so that it does not hide the probability values in the closing.
# ==============================================================================

from manim_imports_ext import *

HYPOTHESIS_COLOR = YELLOW


NOT_HYPOTHESIS_COLOR = GREY


EVIDENCE_COLOR1 = BLUE_C


EVIDENCE_COLOR2 = BLUE_E


NOT_EVIDENCE_COLOR1 = GREY


NOT_EVIDENCE_COLOR2 = GREY_D


# CHANGE: support a standalone fraction with the same semantic probability groups.
def get_bayes_formula(expand_denominator=False, include_posterior=True):
    t2c = {
        "{H}": HYPOTHESIS_COLOR,
        "{\\neg H}": NOT_HYPOTHESIS_COLOR,
        "{E}": EVIDENCE_COLOR1,
    }
    isolate = ["P", "\\over", "=", "\\cdot", "+"]

    prefix = "P({H} | {E}) = " if include_posterior else "= "
    tex = prefix + "{P({H}) P({E} | {H}) \\over "
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

    offset = int(include_posterior)
    if include_posterior:
        formula.posterior = probability(0)
    formula.prior = probability(offset)
    formula.likelihood = probability(offset + 1)
    if expand_denominator:
        formula.denom_prior = probability(offset + 2)
        formula.denom_likelihood = probability(offset + 3)
        formula.denom_anti_prior = probability(offset + 4)
        formula.denom_anti_likelihood = probability(offset + 5)
    else:
        formula.p_evidence = probability(offset + 2)

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

    # CHANGE: accept GL's deep argument while preserving independent diagram parts.
    def copy(self, deep=False):
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


class CreateFormulaFromDiagram(Scene):
    CONFIG = {
        "tex_to_color_map": {
            "P": WHITE,
            "H": HYPOTHESIS_COLOR,
            "E": EVIDENCE_COLOR1,
            "\\neg": RED,
        },
        "bayes_diagram_config": {
            "prior": 1 / 21,
            "likelihood": 0.4,
            "antilikelihood": 0.1,
            "not_evidence_color1": GREY,
            "not_evidence_color2": GREY_D,
            "prior_rect_direction": UP,
        },
    }

    def construct(self):
        t2c = self.tex_to_color_map

        # Add posterior
        posterior = OldTex("P(H|E)", tex_to_color_map=t2c)
        posterior.to_corner(UR)
        posterior_words = OldTexText("Goal: ")
        posterior_words.next_to(posterior, LEFT, aligned_edge=UP)
        self.add(posterior)
        self.add(posterior_words)

        # Show prior
        diagram = self.get_diagram()

        prior_label = OldTex("P(H)", tex_to_color_map=t2c)
        prior_label.add_updater(
            lambda m: m.next_to(diagram.h_brace, UP, SMALL_BUFF)
        )

        prior_example = OldTex("= 1 / 21")
        prior_example.add_updater(
            lambda m: m.next_to(prior_label, RIGHT).shift(0.03 * UP)

        )
        # example_words = OldTexText("In our example")
        # example_words.next_to(prior_example[0][1:], UP, buff=SMALL_BUFF, aligned_edge=LEFT)
        # prior_example.add(example_words)

        prior_arrow = Vector(0.7 * RIGHT)
        prior_arrow.next_to(prior_label, LEFT, SMALL_BUFF)
        prior_word = OldTexText("``Prior''")
        prior_word.next_to(prior_arrow, LEFT, SMALL_BUFF)
        prior_word.align_to(prior_label[0], DOWN)
        prior_word.set_color(HYPOTHESIS_COLOR)

        self.add(diagram)
        self.play(ShowIncreasingSubsets(diagram.people, run_time=2))
        self.wait()
        self.play(
            diagram.hypothesis_split.set_opacity, 1,
            FadeIn(diagram.h_brace),
            FadeInFromDown(prior_label),
        )
        self.wait()
        self.play(FadeIn(prior_example))
        self.play(
            LaggedStartMap(
                Indicate, diagram.people[::10],
                color=BLUE,
            )
        )
        self.wait()
        self.play(
            FadeIn(prior_word, RIGHT),
            GrowArrow(prior_arrow)
        )
        self.wait()
        prior_group = VGroup(
            prior_word, prior_arrow,
            prior_label, prior_example,
            diagram.h_brace,
        )

        # First likelihood split
        like_example = OldTex("= 0.4")
        like_example.add_updater(
            lambda m: m.next_to(diagram.he_brace, LEFT)
        )
        like_example.update()

        like_label = OldTex("P(E|H)", tex_to_color_map=t2c)
        like_label.add_updater(
            lambda m: m.next_to(like_example, LEFT)
        )
        like_label.update()

        like_word = OldTexText("``Likelihood''")
        like_word.next_to(like_label, UP, buff=LARGE_BUFF, aligned_edge=LEFT)
        like_arrow = Arrow(
            like_word.get_bottom(),
            like_label.get_top(),
            buff=0.2,
        )

        limit_arrow = Vector(0.5 * UP)
        limit_arrow.next_to(like_label.get_part_by_tex("|"), UP, SMALL_BUFF)
        limit_arrow.set_stroke(WHITE, 4)
        limit_word = OldTexText("Limit\\\\your\\\\view")
        limit_word.next_to(limit_arrow, UP)

        hne_people = diagram.people[:6]
        he_people = diagram.people[6:10]
        nhe_people = diagram.people[19::10]
        nhne_people = diagram.people[10:]
        nhne_people.remove(*nhe_people)

        for group in [hne_people, nhne_people]:
            group.generate_target()
            group.target.set_opacity(0.25)
            group.target.set_stroke(BLACK, 0, background=True)

        self.play(
            diagram.he_rect.set_opacity, 1,
            diagram.hne_rect.set_opacity, 1,
            MoveToTarget(hne_people),
            GrowFromCenter(diagram.he_brace),
            FadeIn(like_label, RIGHT),
            FadeIn(like_example, RIGHT),
        )
        self.wait()
        self.play(
            ShowCreationThenFadeAround(
                like_label.get_part_by_tex("E"),
                surrounding_rectangle_config={
                    "color": EVIDENCE_COLOR1
                }
            ),
        )
        self.play(WiggleOutThenIn(like_label.get_part_by_tex("|")))
        self.play(
            ShowCreationThenFadeAround(
                like_label.get_part_by_tex("H")
            ),
        )
        self.wait()
        self.play(
            diagram.people[10:].set_opacity, 0.2,
            diagram.nh_rect.set_opacity, 0.2,
            FadeIn(limit_word, DOWN),
            GrowArrow(limit_arrow),
            rate_func=there_and_back_with_pause,
            run_time=6,
        )
        self.wait()
        self.play(
            Write(like_word, run_time=1),
            GrowArrow(like_arrow),
        )
        self.wait()

        # Show anti-likelihood
        anti_label = OldTex("P(E| \\neg H)", tex_to_color_map=t2c)
        anti_label.add_updater(
            lambda m: m.next_to(diagram.nhe_brace, RIGHT)
        )

        anti_example = OldTex("= 0.1")
        anti_example.add_updater(
            lambda m: m.next_to(anti_label, RIGHT).align_to(anti_label[0], DOWN)
        )

        neg_sym = anti_label.get_part_by_tex("\\neg").copy()
        neg_sym.generate_target()
        neg_sym.target.scale(2.5)
        not_word = OldTexText("means ", "``not''")
        not_word[1].set_color(RED)
        neg_group = VGroup(neg_sym.target, not_word)
        neg_group.arrange(RIGHT)
        neg_group.next_to(anti_label, UP, LARGE_BUFF)
        neg_group.to_edge(RIGHT, buff=MED_SMALL_BUFF)

        diagram.nhe_rect.set_opacity(1)
        diagram.nhe_rect.save_state()
        diagram.nhe_rect.become(diagram.nh_rect)
        self.play(
            Restore(diagram.nhe_rect),
            GrowFromCenter(diagram.nhe_brace),
            MoveToTarget(nhne_people),
            FadeIn(anti_label, LEFT),
            FadeIn(anti_example, LEFT),
        )
        diagram.nhne_rect.set_opacity(1)
        self.wait()
        self.play(
            ShowCreationThenFadeAround(
                anti_label[2],
                surrounding_rectangle_config={"color": EVIDENCE_COLOR1},
            )
        )
        self.play(
            ShowCreationThenFadeAround(
                anti_label[4:6],
                surrounding_rectangle_config={"color": RED},
            )
        )
        self.wait()
        self.play(
            MoveToTarget(neg_sym),
            FadeIn(not_word)
        )
        self.wait()
        self.play(
            FadeOut(not_word),
            Transform(neg_sym, anti_label.get_part_by_tex("\\neg"))
        )
        self.remove(neg_sym)

        # Recall final answer, geometrically
        he_group = VGroup(diagram.he_rect, he_people)
        nhe_group = VGroup(diagram.nhe_rect, nhe_people)

        denom = VGroup(
            he_group.copy(),
            OldTex("+"),
            nhe_group.copy(),
        )
        denom.arrange(RIGHT)
        answer = VGroup(
            he_group.copy(),
            Underline(denom, stroke_width=2),
            denom,
        )
        answer.arrange(DOWN)
        answer.scale(0.5)
        answer.to_edge(UP, MED_SMALL_BUFF)
        answer.shift(LEFT)

        equals = OldTex("=")
        posterior.generate_target()

        post_group = VGroup(posterior.target, equals, answer)
        post_group.arrange(RIGHT)
        post_group.to_corner(UL)

        post_word = OldTexText("``Posterior''")
        post_word.set_color(YELLOW)
        post_word.to_corner(UL, buff=MED_SMALL_BUFF)

        post_arrow = Arrow(
            post_word.get_bottom(),
            posterior.target[1].get_top(),
            buff=0.2,
        )
        post_arrow.set_stroke(WHITE, 5)

        dividing_line = DashedLine(ORIGIN, FRAME_WIDTH * RIGHT)
        dividing_line.set_stroke(WHITE, 1)
        dividing_line.next_to(answer, DOWN)
        dividing_line.set_x(0)

        diagram.add(
            diagram.h_brace,
            diagram.he_brace,
            diagram.nhe_brace,
        )
        diagram.generate_target(use_deepcopy=True)
        diagram.target.scale(0.5, about_edge=DL)
        diagram.target.refresh_braces()

        like_group = VGroup(like_word, like_arrow)
        like_vect = like_group.get_center() - like_label.get_center()
        self.play(
            ShowCreation(dividing_line),
            MoveToTarget(diagram),
            MaintainPositionRelativeTo(like_group, like_label),
            MaintainPositionRelativeTo(
                VGroup(prior_word, prior_arrow),
                prior_label,
            ),
            MoveToTarget(posterior),
            ReplacementTransform(posterior_words, equals),
        )
        like_group.move_to(like_label.get_center() + like_vect)
        self.wait()
        self.play(TransformFromCopy(he_group, answer[0]))
        self.play(ShowCreation(answer[1]))
        self.play(LaggedStart(
            TransformFromCopy(he_group, answer[2][0]),
            GrowFromCenter(answer[2][1]),
            TransformFromCopy(nhe_group, answer[2][2]),
        ))
        self.wait()

        # Write final answer, as a formula
        # CHANGE: select complete probabilities instead of Cairo glyph offsets.
        formula = get_bayes_formula(expand_denominator=True, include_posterior=False)
        formula.scale(0.9)
        formula.next_to(answer, RIGHT)
        # CHANGE: keep the expanded denominator inside the visible frame.
        formula.set_max_width(
            FRAME_X_RADIUS - MED_SMALL_BUFF - formula.get_left()[0],
            about_edge=LEFT,
        )

        ph = formula.prior
        peh = formula.likelihood
        over = formula.get_part_by_tex("\\over")
        ph2 = formula.denom_prior
        peh2 = formula.denom_likelihood
        pnh = formula.denom_anti_prior
        penh = formula.denom_anti_likelihood

        parts = VGroup(ph, peh, ph2, peh2, pnh, penh)
        parts.save_state()

        np1 = OldTex("(\\# I )")[0]
        person = Person()
        person.replace(np1[2], dim_to_match=1)
        person.scale(1.5)
        # CHANGE: refresh GL's family and bounds when replacing the count glyph.
        np1.replace_submobject(2, person)

        np1.match_height(ph)
        np1.next_to(ph, LEFT, SMALL_BUFF)
        VGroup(np1, ph, peh).match_x(over)

        np2 = np1.copy()
        np2.next_to(ph2, LEFT, SMALL_BUFF)
        VGroup(np2, ph2, peh2).match_width(
            VGroup(ph2, peh2), about_edge=RIGHT
        )

        np3 = np1.copy()
        np3.next_to(pnh, LEFT, SMALL_BUFF)
        VGroup(np3, pnh, penh).match_width(
            VGroup(pnh, penh), about_edge=RIGHT
        )

        nps = VGroup(np1, np2, np3)
        crosses = VGroup(*[Cross(np)[0] for np in nps])

        top_brace = Brace(np1, UP, buff=SMALL_BUFF)
        top_count = Integer(210)
        top_count.add_updater(lambda m: m.next_to(top_brace, UP, SMALL_BUFF))

        low_brace = Brace(np3, DOWN, buff=SMALL_BUFF)
        low_count = Integer(210)
        low_count.add_updater(lambda m: m.next_to(low_brace, DOWN, SMALL_BUFF))

        h_rect = Rectangle(  # Highlighting rectangle
            stroke_color=YELLOW,
            stroke_width=3,
            fill_color=YELLOW,
            fill_opacity=0.25,
        )
        h_rect.replace(diagram.square, stretch=True)

        s_rect = SurroundingRectangle(answer[0])

        diagram.refresh_braces()
        nh_group = VGroup(
            diagram.nh_brace,
            OldTex("P(\\neg H)", tex_to_color_map=t2c),
            OldTex("= 20 / 21"),
        )
        nh_group[1].next_to(nh_group[0], UP, SMALL_BUFF)
        nh_group[2].next_to(nh_group[1], RIGHT, SMALL_BUFF)

        self.play(
            Write(formula.get_part_by_tex("=")),
            Write(formula.get_part_by_tex("\\over")),
            Write(formula.get_part_by_tex("+")),
            run_time=1
        )
        self.play(ShowCreation(s_rect))
        self.wait()
        self.play(
            FadeIn(np1),
            FadeIn(top_brace),
            FadeIn(top_count),
        )
        self.wait()
        self.play(h_rect.replace, diagram.h_rect, {"stretch": True})
        self.play(
            TransformFromCopy(prior_label, ph),
            top_brace.become, Brace(VGroup(np1, ph), UP, buff=SMALL_BUFF),
            ChangeDecimalToValue(top_count, 10),
        )
        self.wait()
        self.play(h_rect.replace, diagram.he_rect, {"stretch": True})
        self.play(
            TransformFromCopy(like_label, peh),
            top_brace.become, Brace(VGroup(np1, peh), UP, buff=SMALL_BUFF),
            ChangeDecimalToValue(top_count, 4)
        )
        self.wait()

        self.play(
            s_rect.move_to, answer[2][0],
            TransformFromCopy(np1, np2),
            TransformFromCopy(ph, ph2),
            TransformFromCopy(peh, peh2),
        )
        self.wait()

        self.play(
            FadeOut(h_rect),
            s_rect.become, SurroundingRectangle(answer[2][2]),
            FadeOut(prior_group),
            FadeIn(nh_group),
        )
        self.wait()
        h_rect.replace(diagram.square, stretch=True)
        self.play(
            FadeIn(np3),
            FadeIn(low_brace),
            FadeIn(low_count),
        )
        self.play(h_rect.replace, diagram.nh_rect, {"stretch": True})
        self.play(
            TransformFromCopy(nh_group[1], pnh),
            low_brace.become, Brace(VGroup(np3, pnh), DOWN, buff=SMALL_BUFF),
            ChangeDecimalToValue(low_count, 200),
        )
        self.play(h_rect.replace, diagram.nhe_rect, {"stretch": True})
        self.play(
            TransformFromCopy(anti_label, penh),
            low_brace.become, Brace(VGroup(np3, penh), DOWN, buff=SMALL_BUFF),
            ChangeDecimalToValue(low_count, 20),
        )
        self.wait()

        # Clean up
        self.play(
            FadeOut(nh_group),
            FadeOut(s_rect),
            FadeOut(h_rect),
            FadeIn(prior_group),
        )
        self.wait()

        self.play(
            ShowCreation(crosses),
            FadeOut(low_brace),
            FadeOut(top_brace),
            FadeOut(low_count),
            FadeOut(top_count),
        )
        self.wait()
        self.play(
            Restore(parts),
            FadeOut(crosses),
            FadeOut(nps),
            answer.set_opacity, 0.2
        )
        self.wait()

        # Write Bayes' theorem
        formula_rect = SurroundingRectangle(formula[1:])
        formula_rect.set_stroke(TEAL, 2)

        bayes_words = OldTexText("Bayes' theorem")
        bayes_words.scale(1.5)
        bayes_words.next_to(formula_rect, UP, SMALL_BUFF)
        bayes_words.match_color(formula_rect)

        self.play(ShowCreation(formula_rect))
        self.play(FadeInFromDown(bayes_words))
        self.wait()

        # Simplify denominator
        # CHANGE: keep the whole fraction and identify its evidence denominator.
        simpler_formula = get_bayes_formula(include_posterior=False)
        simpler_form = VGroup(*[
            part for part in simpler_formula
            if part is not simpler_formula.get_part_by_tex("=")
        ])
        simpler_form.move_to(answer)
        pe = simpler_formula.p_evidence.copy()
        simpler_numerator = VGroup(*[
            part for part in simpler_form if part not in simpler_formula.p_evidence
        ])
        pe.save_state()

        big_denom_rect = SurroundingRectangle(VGroup(ph2, penh))
        lil_denom_rect = SurroundingRectangle(pe)
        for rect in big_denom_rect, lil_denom_rect:
            rect.set_stroke(BLUE, 0)
            rect.set_fill(BLUE, 0.25)
        pe.move_to(big_denom_rect)
        pe.set_opacity(0)

        self.play(
            FadeOut(answer),
            FadeIn(simpler_numerator)
        )
        self.play(TransformFromCopy(formula_rect, big_denom_rect))
        self.wait()
        self.play(
            Restore(pe),
            ReplacementTransform(big_denom_rect, lil_denom_rect),
            Transform(
                formula_rect,
                SurroundingRectangle(simpler_form, color=TEAL),
            ),
            bayes_words.match_x, simpler_form,
        )
        self.remove(pe)
        self.add(simpler_form)
        self.wait()

        # Show all evidence cases
        he_group_copy = he_group.copy()
        nhe_group_copy = nhe_group.copy()
        copies = VGroup(he_group_copy, nhe_group_copy)

        self.play(
            copies.arrange, RIGHT, {"buff": LARGE_BUFF},
            copies.move_to, DOWN,
            copies.to_edge, RIGHT, LARGE_BUFF,
        )
        self.wait()
        self.play(
            he_group_copy.next_to, VGroup(ph2, peh2), DOWN,
        )
        self.play(
            nhe_group_copy.next_to, VGroup(pnh, penh), DOWN,
        )
        self.wait()
        self.play(
            FadeOut(copies),
            FadeOut(lil_denom_rect),
        )
        self.wait()

        # Name posterior
        self.play(
            GrowArrow(post_arrow),
            FadeIn(post_word, RIGHT),
            FadeOut(formula_rect),
            FadeOut(bayes_words),
        )
        self.wait()

        # Show confusion
        randy = Randolph()
        # CHANGE: keep the replacement mascot clear of the likelihood values.
        randy.set_height(2)
        randy.flip()
        randy.next_to(dividing_line, DOWN)
        randy.to_edge(RIGHT)

        prior_rect = SurroundingRectangle(prior_word)
        post_rect = SurroundingRectangle(post_word)
        VGroup(prior_rect, post_rect).set_stroke(WHITE, 2)

        self.play(FadeIn(randy))
        self.play(randy.change, "confused", formula)
        self.play(Blink(randy))
        self.play(randy.change, "horrified", formula)
        self.play(randy.look_at, diagram)
        self.play(Blink(randy))
        self.play(randy.look_at, formula)
        self.play(randy.change, "tired")
        self.wait(2)
        self.play(
            randy.change, "pondering", prior_label,
            ShowCreation(prior_rect)
        )
        self.play(Blink(randy))
        self.play(
            ReplacementTransform(prior_rect, post_rect),
            randy.look_at, post_rect,
        )
        self.play(randy.change, "thinking")
        self.play(FadeOut(post_rect))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.look_at, formula)
        self.play(Blink(randy))
        self.wait()

        # Transition to next scene
        return  # Skip
        to_move = VGroup(posterior, formula)
        self.remove(to_move, *to_move, *to_move[1])
        to_move.generate_target()
        to_move.target[1].scale(1 / 0.9)
        to_move.target.arrange(RIGHT)
        to_move.target.to_corner(UL)

        everything = Group(*self.get_mobjects())

        self.play(
            LaggedStartMap(FadeOutAndShiftDown, everything),
            MoveToTarget(to_move, rate_func=squish_rate_func(smooth, 0.5, 1)),
            run_time=2,
        )

    def get_diagram(self, include_people=True):
        diagram = BayesDiagram(**self.bayes_diagram_config)
        diagram.set_height(5.5)
        diagram.set_width(5.5, stretch=True)
        diagram.move_to(0.5 * DOWN)
        diagram.add_brace_attrs()

        diagram.evidence_split.set_opacity(0)
        diagram.hypothesis_split.set_opacity(0)
        diagram.nh_rect.set_fill(GREY_D)

        if include_people:
            people = VGroup(*[Person() for x in range(210)])
            people.set_color(interpolate_color(GREY_B, WHITE, 0.5))
            # CHANGE: preserve Cairo column order and spacing for indexed grid members.
            cairo_arrange_in_grid(people, n_cols=21)
            people.set_width(diagram.get_width() - SMALL_BUFF)
            people.set_height(diagram.get_height() - SMALL_BUFF, stretch=True)
            people.move_to(diagram)
            people[10:].set_color(GREEN_D)
            people.set_stroke(BLACK, 2, background=True)

            diagram.add(people)
            diagram.people = people

        return diagram
