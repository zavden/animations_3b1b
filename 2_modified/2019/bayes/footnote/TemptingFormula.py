# ==============================================================================
# Scene:      TemptingFormula
# Source:     videos/_2019/bayes/footnote.py (lines 675-1009)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/bayes/part1.py
#
# Run from this folder:
#     manimgl TemptingFormula.py TemptingFormula -w -m --fps 15
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
class Person(SVGMobject):
    CONFIG = {
        "file_name": "person",
        "height": 1.5,
        "stroke_width": 0,
        "fill_opacity": 1,
        "fill_color": GREY_B,
    }


class RandomnessVsProportions(Scene):
    def construct(self):
        prob_word = OldTexText("Probability")
        unc_word = OldTexText("Uncertainty")
        prop_word = OldTexText("Proportions")
        words = VGroup(prop_word, prob_word, unc_word)
        words.arrange(RIGHT, buff=LARGE_BUFF)
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(UP)
        arrows = VGroup()
        for w1, w2 in zip(words, words[1:]):
            arrow = OldTex("\\rightarrow")
            arrow.move_to(midpoint(w1.get_right(), w2.get_left()))
            arrows.add(arrow)

        random_dice = self.get_random_dice()
        random_dice.next_to(unc_word, DOWN, LARGE_BUFF)

        diagram = self.get_dice_diagram()
        diagram.next_to(prop_word, DOWN, LARGE_BUFF)
        diagram.shift_onto_screen()

        grid = diagram[0]
        border = grid[0][0].copy()
        border.set_stroke(BLACK, 3)
        border.set_fill(WHITE, opacity=0.2)
        border.scale(1.02)

        def update_border(border):
            r1, r2 = random_dice
            i = len(r1[1]) - 1
            j = len(r2[1]) - 1
            border.move_to(diagram[0][i][j])
        border.add_updater(update_border)

        example = VGroup(
            OldTexText("P(X = 5)", tex_to_color_map={"5": YELLOW}),
            Line(LEFT, RIGHT)
        )
        example.arrange(RIGHT)
        example.next_to(grid, RIGHT, LARGE_BUFF)
        example.align_to(random_dice, RIGHT)
        example.shift(0.5 * DOWN)
        grid_copy = grid.copy()
        five_part = VGroup(*[
            square
            for i, row in enumerate(grid_copy)
            for j, square in enumerate(row)
            if i + j == 3
        ])

        self.play(FadeInFromDown(prob_word))
        self.play(
            FadeIn(unc_word, LEFT),
            Write(arrows[1]),
        )
        self.add(random_dice)
        self.wait(9)
        self.play(
            FadeIn(prop_word, RIGHT),
            Write(arrows[0])
        )
        self.play(FadeIn(diagram))
        self.add(border)
        self.wait(2)

        self.play(FadeIn(example))
        self.add(grid_copy, diagram[1])
        self.play(
            grid_copy.set_width, 0.8 * example[1].get_width(),
            grid_copy.next_to, example[1], DOWN,
        )
        self.play(five_part.copy().next_to, example[1], UP)
        self.wait(6)

    def get_die_faces(self):
        dot = Dot()
        dot.set_width(0.15)
        dot.set_color(BLUE_B)

        square = Square()
        square.round_corners(0.25)
        square.set_stroke(WHITE, 2)
        square.set_fill(GREY_E, 1)
        square.set_width(0.6)

        edge_groups = [
            (ORIGIN,),
            (UL, DR),
            (UL, ORIGIN, DR),
            (UL, UR, DL, DR),
            (UL, UR, ORIGIN, DL, DR),
            (UL, UR, LEFT, RIGHT, DL, DR),
        ]

        arrangements = VGroup(*[
            VGroup(*[
                dot.copy().move_to(square.get_bounding_box_point(ec))
                for ec in edge_group
            ])
            for edge_group in edge_groups
        ])
        square.set_width(1)

        faces = VGroup(*[
            VGroup(square.copy(), arrangement)
            for arrangement in arrangements
        ])
        faces.arrange(RIGHT)

        return faces

    def get_random_dice(self):
        faces = list(self.get_die_faces())

        def get_random_pair():
            result = VGroup(*random.sample(faces, 2)).copy()
            result.arrange(RIGHT)
            for mob in result:
                mob.shift(random.random() * RIGHT * MED_SMALL_BUFF)
                mob.shift(random.random() * UP * MED_SMALL_BUFF)
            return result

        result = VGroup(*get_random_pair())
        result.time = 0
        result.iter_count = 0

        def update_result(group, dt):
            group.time += dt
            group.iter_count += 1
            if int(group.time) % 3 == 2:
                group.set_stroke(YELLOW)
                return group
            elif result.iter_count % 3 != 0:
                return group
            else:
                pair = get_random_pair()
                pair.move_to(group)
                group.submobjects = [*pair]

        result.add_updater(update_result)
        result.update()
        return result

    def get_dice_diagram(self):
        grid = VGroup(*[
            VGroup(*[
                Square() for x in range(6)
            ]).arrange(RIGHT, buff=0)
            for y in range(6)
        ]).arrange(DOWN, buff=0)
        grid.set_stroke(WHITE, 1)
        grid.set_height(5)

        colors = color_gradient([RED, YELLOW, GREEN, BLUE], 11)

        numbers = VGroup()
        for i, row in enumerate(grid):
            for j, square in enumerate(row):
                num = Integer(i + j + 2)
                num.set_height(square.get_height() - MED_LARGE_BUFF)
                num.move_to(square)
                # num.set_stroke(BLACK, 2, background=True)
                num.set_fill(GREY_D)
                square.set_fill(colors[i + j], 0.9)
                numbers.add(num)

        faces = VGroup()
        face_templates = self.get_die_faces()
        face_templates.scale(0.5)
        for face, row in zip(face_templates, grid):
            face.next_to(row, LEFT, MED_SMALL_BUFF)
            faces.add(face)
        for face, square in zip(faces.copy(), grid[0]):
            face.next_to(square, UP, MED_SMALL_BUFF)
            faces.add(face)

        result = VGroup(grid, numbers, faces)
        return result



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


class TemptingFormula(ShowTwoPerspectives, RandomnessVsProportions):
    def construct(self):
        # Show venn diagram
        kw = {
            "tex_to_color_map": TEX_TO_COLOR_MAP,
            "isolate": list("P()"),
        }
        formula = VGroup(
            OldTex("P(A \\text{ and } B)", **kw),
            OldTex("="),
            OldTex("P(A)P(B)", "\\,", "\\,", **kw),
        )
        formula.arrange(RIGHT)
        formula.scale(1.5)
        formula.to_edge(UP)

        q_marks = OldTex("???")[0]
        q_marks.scale(1.25)
        q_marks.next_to(formula[1], UP, SMALL_BUFF)

        formula.save_state()
        for part in formula:
            part.set_x(0)
        formula[1:].set_opacity(0)
        and_part = formula[0][2:5].copy()

        venn = self.get_venn_diagram()
        venn.next_to(formula, DOWN, LARGE_BUFF)

        self.add(formula)

        for i in 0, 1:
            self.play(
                DrawBorderThenFill(venn[0][i]),
                FadeIn(venn[1][i]),
            )
        self.play(
            and_part.scale, 0.5,
            and_part.move_to, venn,
        )
        self.remove(and_part)
        venn.add(and_part)
        self.add(venn)
        self.wait()
        self.play(Restore(formula))
        self.play(LaggedStartMap(FadeInFromDown, q_marks))

        # 1 in 4 heart disease related deaths
        people = VGroup(*[Person() for x in range(4)])
        people.arrange(RIGHT)
        people.set_height(2)
        people[0].set_color(RED)
        heart = SuitSymbol("hearts")
        heart.set_fill(BLACK)
        heart.set_height(0.25)
        heart.move_to(people[0])
        heart.shift(0.2 * UR)
        people[0].add(heart)

        grid = self.get_grid(4, 4, height=4)
        grid.to_corner(DL, buff=LARGE_BUFF)
        both_square = grid[0][0].copy()

        people.generate_target()
        people.target.set_height(both_square.get_height() - SMALL_BUFF)
        left_people = people.target.copy()
        self.label_grid(grid, left_people, people.target)
        pairs = self.get_grid_entries(grid, left_people, people.target)
        for pair in pairs:
            pair.generate_target()
            pair.restore()

        pair = pairs[0].target.copy()
        prob = OldTex(
            "P(", "OO", ")", "= \\frac{1}{4} \\cdot \\frac{1}{4} = \\frac{1}{16}",
        )
        pair.move_to(prob[1])
        prob.submobjects[1] = pair
        prob.scale(1.5)
        prob.next_to(grid, RIGHT, LARGE_BUFF)

        self.play(
            FadeOut(venn),
            LaggedStartMap(FadeInFromDown, people),
        )
        self.play(WiggleOutThenIn(heart))
        self.wait()
        self.play(
            MoveToTarget(people),
            TransformFromCopy(people, left_people),
            Write(grid),
            FadeIn(prob[:3]),
            run_time=1,
        )
        self.add(both_square, pairs)
        self.play(
            LaggedStartMap(MoveToTarget, pairs, path_arc=30 * DEGREES),
            both_square.set_stroke, YELLOW, 5,
            both_square.set_fill, YELLOW, 0.25,
        )
        self.play(FadeIn(prob[3:]))
        self.wait()

        grid_group = VGroup(grid, people, left_people, both_square, pairs)

        # Coin flips
        ht_grid = self.get_grid(2, 2, height=3)
        ht_grid.move_to(grid)
        ht_labels = VGroup(OldTexText("H"), OldTexText("T"))
        ht_labels.set_submobject_colors_by_gradient(BLUE, RED)
        ht_labels.scale(2)
        left_ht_labels = ht_labels.copy()
        self.label_grid(ht_grid, left_ht_labels, ht_labels)
        ht_pairs = self.get_grid_entries(ht_grid, left_ht_labels, ht_labels)

        ht_both_square = ht_grid[1][1].copy()
        ht_both_square.set_stroke(YELLOW, 5)
        ht_both_square.set_fill(YELLOW, 0.25)

        ht_prob = OldTex(
            "P(\\text{TT}) = \\frac{1}{2} \\cdot \\frac{1}{2} = \\frac{1}{4}",
            tex_to_color_map={"\\text{TT}": RED}
        )
        ht_prob.scale(1.5)
        ht_prob.next_to(ht_grid, RIGHT, LARGE_BUFF)

        ht_grid_group = VGroup(
            ht_grid, ht_labels, left_ht_labels,
            ht_both_square, ht_pairs,
        )

        self.play(
            FadeOut(grid_group),
            FadeOut(prob),
            FadeIn(ht_grid_group),
            FadeIn(ht_prob),
        )
        self.wait()

        # Dice throws
        dice_grid = self.get_grid(6, 6, height=4)
        dice_grid.set_stroke(WHITE, 1)
        dice_grid.move_to(grid)
        dice_labels = self.get_die_faces()
        dice_labels.set_height(0.5)
        left_dice_labels = dice_labels.copy()
        self.label_grid(dice_grid, left_dice_labels, dice_labels)
        dice_pairs = self.get_grid_entries(dice_grid, left_dice_labels, dice_labels)
        for pair in dice_pairs:
            pair.space_out_submobjects(0.9)
            pair.scale(0.75)

        dice_both_square = dice_grid[0][0].copy()
        dice_both_square.set_stroke(YELLOW, 5)
        dice_both_square.set_fill(YELLOW, 0.25)

        dice_prob = OldTex(
            "P(", "OO", ") = \\frac{1}{6} \\cdot \\frac{1}{6} = \\frac{1}{36}",
        )
        pair = dice_pairs[0].copy()
        pair.scale(1.5)
        pair.move_to(dice_prob[1])
        dice_prob.submobjects[1] = pair
        dice_prob.scale(1.5)
        dice_prob.next_to(dice_grid, RIGHT, LARGE_BUFF)

        dice_grid_group = VGroup(
            dice_grid, dice_labels, left_dice_labels,
            dice_both_square, dice_pairs,
        )

        self.play(
            FadeOut(ht_grid_group),
            FadeOut(ht_prob),
            FadeIn(dice_grid_group),
            FadeIn(dice_prob),
        )
        self.wait()

        # Show correlation
        self.play(
            FadeOut(dice_grid_group),
            FadeOut(dice_prob),
            FadeIn(prob),
            FadeIn(grid_group),
        )
        self.wait()

        cross = Cross(prob[3])

        for pair in pairs:
            pair.add_updater(lambda m: m.move_to(m.square))
        for person, square in zip(people, grid[0]):
            person.square = square
            person.add_updater(lambda m: m.next_to(m.square, UP))

        row_rect = SurroundingRectangle(
            VGroup(grid[0], left_people[0]),
            buff=SMALL_BUFF
        )
        row_rect.set_stroke(RED, 3)

        self.play(ShowCreation(cross))
        self.play(
            FadeOut(prob),
            FadeOut(cross),
        )
        self.play(
            ShowCreation(row_rect)
        )
        self.wait()
        self.play(
            grid[0][0].stretch, 2, 0, {"about_edge": LEFT},
            grid[0][1:].stretch, 2 / 3, 0, {"about_edge": RIGHT},
            both_square.stretch, 2, 0, {"about_edge": LEFT},
            *[
                ApplyMethod(grid[i][0].stretch, 2 / 3, 0, {"about_edge": LEFT})
                for i in range(1, 4)
            ],
            *[
                ApplyMethod(grid[i][1:].stretch, 10 / 9, 0, {"about_edge": RIGHT})
                for i in range(1, 4)
            ],
        )
        self.wait()
        grid_group.add(row_rect)

        # Show correct formula
        cross = Cross(formula)
        cross.set_stroke(RED, 6)

        real_rhs = OldTex("P(A)P(B|A)", **kw)
        real_rhs.scale(1.5)
        real_formula = VGroup(*formula[:2].copy(), real_rhs)
        real_formula.shift(1.5 * DOWN)
        real_rhs.next_to(real_formula[:2], RIGHT)

        real_rect = SurroundingRectangle(real_formula, buff=SMALL_BUFF)
        real_rect.set_stroke(GREEN)
        check = OldTex("\\checkmark")
        check.set_color(GREEN)
        check.match_height(real_formula)
        check.next_to(real_rect, LEFT)

        small_cross = Cross(check)
        small_cross.match_style(cross)
        small_cross.next_to(formula, LEFT)

        self.play(
            ShowCreationThenFadeAround(formula),
            FadeOut(q_marks),
        )
        self.play(ShowCreation(cross))
        self.wait()
        self.play(
            TransformFromCopy(formula, real_formula),
            grid_group.scale, 0.7,
            grid_group.to_corner, DL,
        )
        self.play(
            FadeIn(real_rect),
            FadeIn(check, RIGHT),
        )
        self.wait()

        # Show other grid
        ht_grid_group.scale(0.7)
        ht_grid_group.next_to(grid_group, RIGHT, buff=1.5)
        dice_grid_group.scale(0.7)
        dice_grid_group.next_to(ht_grid_group, RIGHT, buff=1.5)

        Bs = VGroup(formula[2][4:], real_formula[2][4:])
        B_rect = SurroundingRectangle(
            Bs,
            stroke_color=BLUE,
            # buff=SMALL_BUFF,
            buff=0,
        )
        B_rect.scale(1.1, about_edge=LEFT)
        B_rect.set_fill(BLUE, 0.5)
        B_rect.set_stroke(width=0)

        big_rect = SurroundingRectangle(
            VGroup(ht_grid_group, dice_grid_group),
            buff=MED_LARGE_BUFF,
            color=BLUE,
        )
        # B_rect.get_points()[0] += 0.2 * RIGHT
        # B_rect.get_points()[-1] += 0.2 * RIGHT
        # B_rect.get_points()[3] += 0.2 * LEFT
        # B_rect.get_points()[4] += 0.2 * LEFT
        # B_rect.make_jagged()

        self.play(FadeIn(ht_grid_group))
        self.play(FadeIn(dice_grid_group))
        self.wait()
        self.add(B_rect, Bs.copy())
        self.play(
            FadeIn(B_rect),
            FadeIn(big_rect),
            Transform(cross, small_cross),
            FadeOut(real_rect),
        )
        self.wait()

    def get_grid(self, n, m, height=4):
        grid = VGroup(*[
            VGroup(
                *[Square() for x in range(m)]
            ).arrange(RIGHT, buff=0)
            for y in range(n)
        ]).arrange(DOWN, buff=0)
        grid.set_height(height)
        grid.set_stroke(WHITE, 2)
        return grid

    def label_grid(self, grid, row_labels, col_labels):
        for label, row in zip(row_labels, grid):
            label.next_to(row, LEFT)

        for label, square in zip(col_labels, grid[0]):
            label.next_to(square, UP)

    def get_grid_entries(self, grid, row_labels, col_labels):
        pairs = VGroup()
        for i, p1 in enumerate(row_labels):
            for j, p2 in enumerate(col_labels):
                pair = VGroup(p1, p2).copy()
                pair.save_state()
                pair.scale(0.6)
                pair.arrange(RIGHT, buff=0.05)
                pair.square = grid[i][j]
                pair.move_to(grid[i][j])
                pairs.add(pair)
        return pairs
