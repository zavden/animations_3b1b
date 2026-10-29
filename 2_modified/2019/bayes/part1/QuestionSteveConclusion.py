# ==============================================================================
# Scene:      QuestionSteveConclusion
# Source:     videos/_2019/bayes/part1.py (lines 4222-4404)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl QuestionSteveConclusion.py QuestionSteveConclusion -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
#   - Accept ManimGL's copy(deep=) and keep the deep copy of the parts of the Bayes diagram.
#   - Keep the column order and Cairo spacing in the grid so that the indices of people and cells correspond to the right region.
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

    # CHANGE: accept GL's deep argument while preserving independent diagram parts.
    def copy(self, deep=False):
        return self.deepcopy()


class ProbabilityBar(VGroup):
    CONFIG = {
        "color1": BLUE_D,
        "color2": GREY_BROWN,
        "height": 0.5,
        "width": 6,
        "rect_style": {
            "stroke_width": 1,
            "stroke_color": WHITE,
            "fill_opacity": 1,
        },
        "include_braces": False,
        "brace_direction": UP,
        "include_percentages": True,
        "percentage_background_stroke_width": 2,
    }

    def __init__(self, p=0.5, **kwargs):
        super().__init__(**kwargs)
        self.add_backbone()
        self.add_p_tracker(p)
        self.add_bars()
        if self.include_braces:
            self.braces = always_redraw(lambda: self.get_braces())
            self.add(self.braces)
        if self.include_percentages:
            self.percentages = always_redraw(lambda: self.get_percentages())
            self.add(self.percentages)

    def add_backbone(self):
        backbone = Line()
        backbone.set_opacity(0)
        backbone.set_width(self.width)
        self.backbone = backbone
        self.add(backbone)

    def add_p_tracker(self, p):
        self.p_tracker = ValueTracker(p)

    def add_bars(self):
        bars = VGroup(Rectangle(), Rectangle())
        bars.set_height(self.height)
        colors = [self.color1, self.color2]
        for bar, color in zip(bars, colors):
            bar.set_style(**self.rect_style)
            bar.set_fill(color=color)

        bars.add_updater(self.update_bars)
        self.bars = bars
        self.add(bars)

    def update_bars(self, bars):
        vects = [LEFT, RIGHT]
        p = self.p_tracker.get_value()
        values = [p, 1 - p]
        total_width = self.backbone.get_width()
        for bar, vect, value in zip(bars, vects, values):
            bar.set_width(value * total_width, stretch=True)
            bar.move_to(self.backbone, vect)
        return bars

    def get_braces(self):
        return VGroup(*[
            Brace(
                bar,
                self.brace_direction,
                min_num_quads=1,
                buff=SMALL_BUFF,
            )
            for bar in self.bars
        ])

    def get_percentages(self):
        p = self.p_tracker.get_value()
        labels = VGroup(*[
            Integer(value, unit="\\%")
            for value in [
                np.floor(p * 100),
                100 - np.floor(p * 100),
            ]
        ])
        for label, bar in zip(labels, self.bars):
            label.set_height(0.75 * bar.get_height())
            min_width = 0.75 * bar.get_width()
            if label.get_width() > min_width:
                label.set_width(min_width)
            label.move_to(bar)
            label.set_stroke(
                BLACK,
                self.percentage_background_stroke_width,
                background=True
            )
        return labels

    def add_icons(self, *icons, buff=SMALL_BUFF):
        if hasattr(self, "braces"):
            refs = self.braces
        else:
            refs = self.bars

        for icon, ref in zip(icons, refs):
            icon.ref = ref
            icon.add_updater(lambda i: i.next_to(
                i.ref,
                self.brace_direction,
                buff=buff
            ))
        self.icons = VGroup(*icons)
        self.add(self.icons)


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class Steve(SVGMobject):
    CONFIG = {
        "file_name": "steve",
        "fill_color": GREY,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "stroke_width": 0,
        "height": 3,
        "include_name": True,
        "name": "Steve"
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.include_name:
            self.add_name()

    def add_name(self):
        self.name = OldTexText(self.name)
        self.name.match_width(self)
        self.name.next_to(self, DOWN, SMALL_BUFF)
        self.add(self.name)


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


# CHANGE: pass the CONFIG styles to GL's SVG constructor; otherwise they come out black.
@cairo_svg_defaults
class FarmerIcon(SVGMobject):
    CONFIG = {
        "file_name": "farming",
        "stroke_width": 0,
        "fill_color": GREEN_E,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
        "height": 1.5,
    }


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


class Librarian(Person):
    CONFIG = {
        "IconClass": LibrarianIcon,
        "icon_style": {
            "background_stroke_width": 5,
            "background_stroke_color": BLACK,
        },
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        icon = self.IconClass()
        icon.set_style(**self.icon_style)
        icon.match_width(self)
        icon.move_to(self.get_corner(DR), DOWN)
        self.add(icon)


class Farmer(Librarian):
    CONFIG = {
        "IconClass": FarmerIcon,
        "icon_style": {
            "background_stroke_width": 2,
        },
        "fill_color": GREEN,
    }


class DescriptionOfSteve(Scene):
    def construct(self):
        self.write_description()
        self.compare_probabilities()

    def write_description(self):
        steve = Steve(height=3)
        steve.to_corner(UR)

        description = self.get_description()
        description.to_edge(LEFT)
        description.align_to(steve, UP)

        mt_parts = VGroup(
            description.get_part_by_tex("meek"),
            description.get_part_by_tex("soul"),
        )
        mt_parts.set_color(WHITE)

        self.add(steve)
        self.play(
            FadeIn(description),
            run_time=3,
            lag_ratio=0.01,
            rate_func=linear,
        )
        self.wait(3)

        lines = VGroup(*[
            Line(mob.get_corner(DL), mob.get_corner(DR), color=YELLOW)
            for mob in mt_parts
        ])
        self.play(
            ShowCreation(lines),
            mt_parts.set_color, YELLOW,
        )
        self.play(FadeOut(lines))
        self.wait()

    def compare_probabilities(self):
        bar = ProbabilityBar(
            0.5, width=10,
            include_braces=True,
            percentage_background_stroke_width=2,
        )
        icons = VGroup(
            LibrarianIcon(),
            FarmerIcon(),
        )
        for icon, text, half in zip(icons, ["Librarian", "Farmer"], bar.bars):
            icon.set_height(0.7)
            label = OldTexText(text)
            label.next_to(icon, DOWN, buff=SMALL_BUFF)
            label.set_color(
                interpolate_color(half.get_color(), WHITE, 0.5)
            )
            icon.add(label)

        bar.add_icons(*icons)
        bar.move_to(1.75 * DOWN)

        bar.icons.set_opacity(0)

        q_marks = OldTex(*"???")
        q_marks.scale(1.5)
        q_marks.space_out_submobjects(1.5)
        q_marks.next_to(bar, DOWN)

        self.play(FadeIn(bar))
        self.wait()
        self.play(
            bar.p_tracker.set_value, 0.9,
            bar.icons[0].set_opacity, 1,
        )
        self.wait()
        self.play(
            bar.p_tracker.set_value, 0.1,
            bar.icons[1].set_opacity, 1,
        )
        self.play(
            LaggedStartMap(
                FadeInFrom, q_marks,
                lambda m: (m, UP),
                run_time=2,
            ),
            ApplyMethod(
                bar.p_tracker.set_value, 0.7,
                run_time=8,
            )
        )
        for value in 0.3, 0.7:
            self.play(
                bar.p_tracker.set_value, 0.3,
                run_time=7,
            )

    def get_description(self):
        return OldTexText(
            """
            Steve is very shy and withdrawn,\\\\
            invariably helpful but with very\\\\
            little interest in people or in the\\\\
            world of reality. A meek and tidy\\\\
            soul, he has a need for order and\\\\
            structure, and a passion for detail.\\\\
            """,
            tex_to_color_map={
                "shy and withdrawn": BLUE,
                "meek and tidy": YELLOW,
                "soul": YELLOW,
            },
            alignment="",
        )


class HeartOfBayesTheorem(Scene):
    def construct(self):
        title = OldTexText("Heart of Bayes' theorem")
        title.scale(1.5)
        title.add(Underline(title))
        title.to_edge(UP)

        # Bayes diagrams
        # prior_tracker = ValueTracker(0.1)
        # likelihood_tracker = ValueTracker(0.4)
        # antilikelihood_tracker = ValueTracker(0.1)
        diagram = self.get_diagram(
            prior=0.1, likelihood=0.4, antilikelihood=0.1,
            # prior_tracker.get_value(),
            # likelihood_tracker.get_value(),
            # antilikelihood_tracker.get_value(),
        )
        diagram.nh_rect.set_fill(GREEN_E)
        diagram.hypothesis_split.set_opacity(1)
        diagram.evidence_split.set_opacity(0)
        restricted_diagram = self.get_restricted_diagram(diagram)
        diagram_copy = diagram.copy()
        diagram_copy.move_to(restricted_diagram)

        diagrams = VGroup(diagram, restricted_diagram)

        label1 = OldTexText("All possibilities")
        label2 = OldTexText(
            "All possibilities\\\\", "fitting the evidence",
            tex_to_color_map={"evidence": EVIDENCE_COLOR1},
        )
        labels = VGroup(label1, label2)
        labels.scale(diagram.get_width() / label1.get_width())

        for l, d in zip(labels, diagrams):
            l.next_to(d, UP)

        label2.save_state()
        label2[0].move_to(label2, DOWN)
        label2[1:].shift(0.25 * UP)
        label2[1:].set_opacity(0)

        # Final fraction written geometrically
        fraction = always_redraw(
            lambda: self.get_geometric_fraction(restricted_diagram)
        )
        frac_box = always_redraw(lambda: DashedVMobject(
            SurroundingRectangle(
                fraction,
                buff=MED_SMALL_BUFF,
                stroke_width=2,
                stroke_color=WHITE,
            ),
            num_dashes=100,
        ))
        prob = OldTex(
            "P\\left(",
            "{\\text{Librarian }",
            "\\text{given}", "\\over", "\\text{the evidence}}",
            "\\right)"
        )
        prob.set_color_by_tex("Librarian", HYPOTHESIS_COLOR)
        prob.set_color_by_tex("evidence", EVIDENCE_COLOR1)
        prob.get_part_by_tex("\\over").set_opacity(0)
        prob.match_width(frac_box)
        prob.next_to(frac_box, UP)

        updaters = VGroup(
            diagram, restricted_diagram, fraction, frac_box
        )
        updaters.suspend_updating()

        self.play(
            FadeIn(diagram),
            FadeInFromDown(label1),
        )
        self.play(
            TransformFromCopy(diagram, diagram_copy),
            TransformFromCopy(label1[0], label2[0]),
        )
        self.play(
            Restore(label2),
            ReplacementTransform(diagram_copy, restricted_diagram)
        )
        self.wait()

        self.play(
            TransformFromCopy(
                restricted_diagram.he_rect,
                fraction[0],
            ),
            TransformFromCopy(
                restricted_diagram.he_rect,
                fraction[2][0],
            ),
            TransformFromCopy(
                restricted_diagram.nhe_rect,
                fraction[2][2],
            ),
            ShowCreation(fraction[1]),
            Write(fraction[2][1]),
        )
        self.add(fraction)
        self.play(
            ShowCreation(frac_box),
            FadeIn(prob)
        )
        self.wait()

        self.play(Write(title, run_time=1))
        self.wait()

        # Mess with some numbers
        updaters.resume_updating()
        self.play(*[
            ApplyMethod(d.set_prior, 0.4, run_time=2)
            for d in diagrams
        ])
        self.play(*[
            ApplyMethod(d.set_likelihood, 0.3, run_time=2)
            for d in diagrams
        ])
        self.play(*[
            ApplyMethod(d.set_antilikelihood, 0.6, run_time=2)
            for d in diagrams
        ])
        # self.play(prior_tracker.set_value, 0.4, run_time=2)
        # self.play(antilikelihood_tracker.set_value, 0.3, run_time=2)
        # self.play(likelihood_tracker.set_value, 0.6, run_time=2)
        self.wait()
        updaters.suspend_updating()

        # Ask about a formula
        words = OldTexText("Write this more\\\\mathematically")
        words.scale(1.25)
        words.set_color(RED)
        words.to_corner(UR)
        arrow = Arrow(words.get_bottom(), frac_box.get_top(), buff=SMALL_BUFF)
        arrow.match_color(words)
        arrow.set_stroke(width=5)

        self.play(
            FadeIn(words, DOWN),
            GrowArrow(arrow),
            FadeOut(prob),
            title.to_edge, LEFT
        )
        self.wait()

    def get_diagram(self, prior, likelihood, antilikelihood):
        diagram = BayesDiagram(
            prior, likelihood, antilikelihood,
            not_evidence_color1=GREY,
            not_evidence_color2=GREEN_E,
        )
        diagram.set_height(3)
        diagram.move_to(5 * LEFT + DOWN)

        diagram.add_brace_attrs()
        braces = VGroup(diagram.h_brace, diagram.nh_brace)
        diagram.add(*braces)
        icons = VGroup(LibrarianIcon(), FarmerIcon())
        icons[0].set_color(YELLOW_D)
        for icon, brace in zip(icons, braces):
            icon.set_height(0.5)
            icon.brace = brace
            icon.add_updater(lambda m: m.next_to(m.brace, DOWN, SMALL_BUFF))
            diagram.add(icon)
        return diagram

    def get_restricted_diagram(self, diagram):
        restricted_diagram = diagram.deepcopy()
        restricted_diagram.set_x(0)
        restricted_diagram.hypothesis_split.set_opacity(0)
        restricted_diagram.evidence_split.set_opacity(1)
        restricted_diagram.hne_rect.set_opacity(0.1)
        restricted_diagram.nhne_rect.set_opacity(0.1)
        return restricted_diagram

    def get_geometric_fraction(self, diagram):
        fraction = VGroup(
            diagram.he_rect.copy(),
            Line(LEFT, RIGHT),
            VGroup(
                diagram.he_rect.copy(),
                OldTex("+"),
                diagram.nhe_rect.copy(),
            ).arrange(RIGHT, buff=SMALL_BUFF)
        )
        fraction.arrange(DOWN)
        fraction[1].match_width(fraction)
        fraction.to_edge(RIGHT)
        fraction.align_to(diagram.square, UP)
        return fraction


class QuestionSteveConclusion(HeartOfBayesTheorem, DescriptionOfSteve):
    def construct(self):
        # Setup
        steve = Steve()
        steve.shift(UP)
        self.add(steve)

        kt = Group(
            ImageMobject("kahneman"),
            ImageMobject("tversky"),
        )
        kt.arrange(DOWN)
        kt.set_height(6)
        randy = Randolph()
        kt.next_to(randy, RIGHT, LARGE_BUFF)
        randy.align_to(kt, DOWN)

        farmers = VGroup(*[Farmer() for x in range(20)])
        # CHANGE: preserve Cairo column order and spacing for indexed grid members.
        cairo_arrange_in_grid(farmers, n_cols=5)
        people = VGroup(Librarian(), farmers)
        people.arrange(RIGHT, aligned_edge=UP)
        people.set_height(3)
        people.next_to(randy.get_corner(UL), UP)
        cross = Cross(people)
        cross.set_stroke(RED, 8)

        # Question K&T
        self.play(
            steve.scale, 0.5,
            steve.to_corner, DL,
            FadeIn(randy),
            FadeInFromDown(kt, lag_ratio=0.3),
        )
        self.play(randy.change, "sassy")
        self.wait()
        self.play(
            FadeIn(people, RIGHT, lag_ratio=0.01),
            randy.change, "raise_left_hand", people,
        )
        self.wait()
        self.play(
            ShowCreation(cross),
            randy.change, "angry"
        )
        self.wait()

        # Who is Steve?
        people.add(cross)
        self.play(
            people.scale, 0.3,
            people.to_corner, UL,
            steve.scale, 1.5,
            steve.next_to, randy.get_corner(UL), LEFT,
            randy.change, "pondering", steve,
        )
        self.play(randy.look_at, steve)
        self.play(Blink(randy))

        kt.generate_target()
        steve.generate_target()
        steve.target.set_height(0.9 * kt[0].get_height())
        group = Group(kt.target[0], steve.target, kt.target[1])
        group.arrange(RIGHT)
        group.to_edge(RIGHT)

        self.play(
            MoveToTarget(kt),
            MoveToTarget(steve),
            randy.shift, 2 * LEFT,
            randy.change, 'erm', kt.target,
            FadeOut(people, 2 * LEFT),
        )
        self.remove(people, cross)
        self.play(Blink(randy))
        self.wait()

        jessy = Randolph(color=BLUE_B)
        jessy.next_to(randy, LEFT, MED_LARGE_BUFF)
        steve.target.match_height(randy)
        steve.target.next_to(randy, RIGHT, MED_LARGE_BUFF)
        morty = Mortimer()
        morty.next_to(steve.target, RIGHT, MED_LARGE_BUFF)
        morty.look_at(steve.target),
        jessy.look_at(steve.target),
        VGroup(jessy, morty, steve.target).to_edge(DOWN)
        pis = VGroup(randy, jessy, morty)

        self.play(
            LaggedStartMap(FadeOutAndShift, kt, lambda m: (m, 3 * UR)),
            MoveToTarget(steve),
            randy.to_edge, DOWN,
            randy.change, "happy", steve.target,
            FadeIn(jessy),
            FadeIn(morty),
        )
        self.play(LaggedStart(*[
            ApplyMethod(pi.change, "hooray", steve)
            for pi in pis
        ]))
        self.play(Blink(morty))
        self.play(Blink(jessy))

        # The assumption changes the prior
        diagram = self.get_diagram(0.05, 0.4, 0.1)
        diagram.nhne_rect.set_fill(GREY_D)
        diagram.set_height(3.5)
        diagram.center().to_edge(UP, buff=MED_SMALL_BUFF)

        self.play(
            FadeIn(diagram),
            *[
                ApplyMethod(pi.change, "pondering", diagram)
                for pi in pis
            ],
        )
        self.play(diagram.set_prior, 0.5)
        self.play(Blink(jessy))
        self.wait()
        self.play(Blink(morty))
        self.play(
            morty.change, "raise_right_hand", diagram,
            ApplyMethod(diagram.set_prior, 0.9, run_time=2),
        )
        self.play(Blink(randy))
        self.wait()

        # Likelihood of description
        description = self.get_description()
        description.scale(0.5)
        description.to_corner(UL)

        self.play(
            FadeIn(description),
            *[ApplyMethod(pi.change, "sassy", description) for pi in pis]
        )
        self.play(
            diagram.set_likelihood, 0.2,
            run_time=2,
        )
        self.play(
            diagram.set_antilikelihood, 0.5,
            run_time=2,
        )
        self.play(Blink(jessy))
        self.play(Blink(randy))
        self.wait()

        # Focus on diagram
        diagram.generate_target()
        diagram.target.set_height(6)
        diagram.target.move_to(3 * LEFT)

        formula = get_bayes_formula()
        formula.scale(0.75)
        formula.to_corner(UR)

        self.play(
            FadeInFromDown(formula),
            LaggedStart(*[
                ApplyMethod(pi.change, "thinking", formula)
                for pi in pis
            ])
        )
        self.play(Blink(randy))
        self.play(
            LaggedStartMap(
                FadeOutAndShiftDown,
                VGroup(description, *pis, steve),
            ),
            MoveToTarget(diagram, run_time=3),
            ApplyMethod(
                formula.scale, 1.5, {"about_edge": UR},
                run_time=2.5,
            ),
        )
        self.wait()

        kw = {"run_time": 2}
        self.play(diagram.set_prior, 0.1, **kw)
        self.play(diagram.set_prior, 0.6, **kw)
        self.play(diagram.set_likelihood, 0.5, **kw),
        self.play(diagram.set_antilikelihood, 0.1, **kw),
        self.wait()
