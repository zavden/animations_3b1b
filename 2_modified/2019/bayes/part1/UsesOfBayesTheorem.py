# ==============================================================================
# Scene:      UsesOfBayesTheorem
# Source:     videos/_2019/bayes/part1.py (lines 3181-3269)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl UsesOfBayesTheorem.py UsesOfBayesTheorem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Identify the probabilities of get_bayes_formula by LaTeX parts, avoiding Cairo's glyph indices.
# ==============================================================================

from manim_imports_ext import *

HYPOTHESIS_COLOR = YELLOW


NOT_HYPOTHESIS_COLOR = GREY


EVIDENCE_COLOR1 = BLUE_C


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


class UsesOfBayesTheorem(Scene):
    def construct(self):
        formula = get_bayes_formula()
        formula.to_corner(UL)
        rhs = formula[7:]

        bubble = ThoughtBubble(direction=RIGHT)
        bubble.set_fill(opacity=0)
        arrow = Vector(RIGHT)
        arrow.next_to(formula, RIGHT, MED_LARGE_BUFF)
        bubble.set_height(2)
        bubble.next_to(arrow, RIGHT, MED_LARGE_BUFF)
        bubble.align_to(formula, UP)
        bar = ProbabilityBar(
            0.1,
            percentage_background_stroke_width=1,
            include_braces=False,
        )
        bar.set_width(0.8 * bubble[-1].get_width())
        bar.move_to(bubble.get_bubble_center())

        scientist = SVGMobject(file_name="scientist")
        programmer = SVGMobject(file_name="programmer")
        randy = Randolph().flip()

        people = VGroup(scientist, programmer, randy)
        people.set_stroke(width=0)
        for person in people:
            person.set_height(2.5)
            if person is not randy:
                person.set_fill(GREY)
                person.set_sheen(0.5, UL)

        people.arrange(RIGHT, buff=2.5)
        # programmer.shift(0.5 * RIGHT)
        people.to_edge(DOWN, buff=LARGE_BUFF)

        self.add(formula)
        self.wait()
        self.play(GrowArrow(arrow))
        self.play(ShowCreation(bubble), FadeIn(bar))
        self.play(bar.p_tracker.set_value, 0.8)
        self.wait()

        # Add people
        for person in [scientist, programmer]:
            self.play(FadeIn(person, DOWN))
            rhs_copy = rhs.copy()
            rhs_copy.add_to_back(
                SurroundingRectangle(
                    rhs_copy,
                    fill_color=BLACK,
                    fill_opacity=0.8,
                    stroke_color=WHITE,
                    stroke_width=2,
                )
            )
            rhs_copy.generate_target()
            rhs_copy[0].set_stroke(width=0)
            rhs_copy.target.scale(0.5)
            rhs_copy.target.move_to(person.get_corner(DR))
            self.add(rhs_copy, formula)
            self.play(MoveToTarget(rhs_copy))
            self.wait()
            person.add(rhs_copy)

        self.play(FadeInFromDown(randy))
        self.play(randy.change, "pondering")
        self.play(Blink(randy))
        bubble_group = VGroup(bubble, bar)
        self.play(
            bubble_group.scale, 1.4,
            bubble_group.move_to, randy.get_corner(UL), DR,
            randy.look_at, bubble,
            FadeOut(arrow),
        )
        self.wait()
        self.play(Blink(randy))
        self.play(bar.p_tracker.set_value, 0.3, run_time=3)
        self.play(randy.change, "thinking")
        self.play(Blink(randy))
        self.wait()

        self.play(LaggedStartMap(
            FadeOutAndShift,
            VGroup(*people, bubble_group),
            lambda m: (m, DOWN),
            lag_ratio=0.15,
        ))
