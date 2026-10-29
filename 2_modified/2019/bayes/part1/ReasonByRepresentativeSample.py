# ==============================================================================
# Scene:      ReasonByRepresentativeSample
# Source:     videos/_2019/bayes/part1.py (lines 1479-1819)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReasonByRepresentativeSample.py ReasonByRepresentativeSample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Pass the CONFIG styles of the Bayes SVG classes to the GL constructor to keep colors and strokes.
#   - Freeze the copies of the counters in TransformFromCopy to prevent their updaters from changing the geometry during interpolation.
# ==============================================================================

from manim_imports_ext import *

HYPOTHESIS_COLOR = YELLOW


EVIDENCE_COLOR1 = BLUE_C


EVIDENCE_COLOR2 = BLUE_E


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


class CorrectViewOfFarmersAndLibrarians(Scene):
    def construct(self):
        # Match last scene
        steves = VGroup(Steve(), Steve())
        book = LibrarianIcon()
        farm = FarmerIcon()
        icons = VGroup(book, farm)

        for mob in icons:
            mob.set_height(1)
            mob.move_to(DOWN + 2 * LEFT)
        farm.shift(4 * RIGHT)

        steves.match_width(book)
        steves.move_to(book, DOWN)
        steves.shift(3 * UP)
        steve1, steve2 = steves
        steve2.match_x(farm)

        self.add(steves, book, farm)

        # Add arrows
        arrows = VGroup(*[
            Arrow(s.get_bottom(), m.get_top())
            for s, m in zip(steves, icons)
        ])
        words = VGroup(
            OldTexText("Stereotype"),
            OldTexText("Unexpected"),
        )
        for arrow, word, vect in zip(arrows, words, [LEFT, RIGHT]):
            word.scale(1.5)
            word.next_to(arrow, vect)
            self.play(
                GrowArrow(arrow),
                FadeIn(word, UP),
            )
        self.wait()

        # Show people proportions
        librarian = Librarian()
        farmer = Farmer()

        librarian.move_to(LEFT).to_edge(UP)
        farmer.move_to(RIGHT).to_edge(UP)
        farmer_ul = farmer.get_corner(UL)

        farmers = VGroup(farmer, *[farmer.copy() for x in range(19)])
        farmers.arrange_in_grid(n_rows=4)
        farmers.move_to(farmer_ul, UL)

        farmer_outlines = farmers.copy()
        farmer_outlines.set_fill(opacity=0)
        farmer_outlines.set_stroke(YELLOW, 1)

        farmer_count = Integer(1)
        farmer_count.scale(2)
        farmer_count.set_color(GREEN)
        farmer_count.next_to(farmers, LEFT, buff=LARGE_BUFF)
        farmer_count.add_updater(lambda m: m.set_value(len(farmer_outlines)))

        for person, icon in zip([librarian, farmer], icons):
            person.save_state()
            person[:-1].set_opacity(0)
            person.scale(
                icon.get_height() / person[-1].get_height()
            )
            person.move_to(icon, DR)

        self.remove(*icons)
        self.play(
            LaggedStartMap(FadeOut, VGroup(steves, arrows, words)),
            Restore(librarian),
            Restore(farmer),
            run_time=1,
        )
        self.play(
            LaggedStartMap(FadeIn, farmers[1:])
        )
        self.wait()
        self.add(farmer_count)
        self.play(
            ShowIncreasingSubsets(farmer_outlines),
            int_func=np.ceil,
            rate_func=linear,
            run_time=2,
        )
        self.play(FadeOut(farmer_outlines))
        self.wait()

        # Show higher number of farmers
        farmers.save_state()
        farmers.generate_target()
        farmers.target.scale(0.5, about_edge=UL)
        new_farmers = VGroup(*it.chain(*[
            farmers.target.copy().next_to(
                farmers.target, vect, buff=SMALL_BUFF,
            )
            for vect in [RIGHT, DOWN]
        ]))
        new_farmers[-10:].align_to(new_farmers, RIGHT)
        new_farmers[-10:].align_to(new_farmers[-20], UP)

        farmer_count.clear_updaters()
        self.play(
            MoveToTarget(farmers),
            ShowIncreasingSubsets(new_farmers),
            ChangeDecimalToValue(farmer_count, 60),
        )
        self.wait()
        self.play(
            FadeOut(new_farmers),
            Restore(farmers),
            ChangeDecimalToValue(farmer_count, 20),
        )
        self.wait()

        # Organize into a representative sample
        farmers.generate_target()
        librarian.generate_target()
        group = VGroup(librarian.target, *farmers.target)
        self.arrange_bottom_row(group)

        l_brace = self.get_count_brace(VGroup(librarian.target))
        f_brace = self.get_count_brace(farmers.target)

        self.play(
            MoveToTarget(librarian),
            MoveToTarget(farmers),
            ReplacementTransform(farmer_count, f_brace[-1]),
            GrowFromCenter(f_brace[:-1]),
        )
        self.play(GrowFromCenter(l_brace))
        self.wait()

    def get_count_brace(self, people):
        brace = Brace(people, UP, buff=SMALL_BUFF)
        count = Integer(len(people), edge_to_fix=DOWN)
        count.next_to(brace, UP, SMALL_BUFF)
        brace.add(count)
        brace.count = count
        return brace

    def arrange_bottom_row(self, group):
        group.arrange(RIGHT, buff=0.5)
        group.set_width(FRAME_WIDTH - 3)
        group.to_edge(DOWN)
        for person in group:
            person[-1].set_stroke(BLACK, 1, background=True)


class ReasonByRepresentativeSample(CorrectViewOfFarmersAndLibrarians):
    CONFIG = {
        "ignore_icons": False,
        # "ignore_icons": True,
    }

    def construct(self):
        # Match previous scene
        librarians = VGroup(Librarian())
        farmers = VGroup(*[Farmer() for x in range(20)])
        everyone = VGroup(*librarians, *farmers)
        self.arrange_bottom_row(everyone)
        self.add(everyone)

        if self.ignore_icons:
            for person in everyone:
                person.submobjects.pop()

        l_brace = self.get_count_brace(librarians)
        f_brace = self.get_count_brace(farmers)
        braces = VGroup(l_brace, f_brace)
        for brace in braces:
            brace.count.set_stroke(BLACK, 3, background=True)
            brace.count.brace = brace
            brace.remove(brace.count)
            brace.count_tracker = ValueTracker(brace.count.get_value())
            brace.count.add_updater(
                lambda c: c.set_value(
                    c.brace.count_tracker.get_value(),
                ).next_to(c.brace, UP, SMALL_BUFF)
            )
            self.add(brace, brace.count)

        # Multiply by 10
        new_people = VGroup()
        for group in [librarians, farmers]:
            new_rows = VGroup(*[group.copy() for x in range(9)])
            new_rows.arrange(UP, buff=SMALL_BUFF)
            new_rows.next_to(group, UP, SMALL_BUFF)
            new_people.add(new_rows)
        new_librarians, new_farmers = new_people

        self.play(
            *[
                FadeIn(new_rows, lag_ratio=0.1)
                for new_rows in new_people
            ],
            *[
                ApplyMethod(brace.next_to, new_rows, UP, {"buff": SMALL_BUFF})
                for brace, new_rows in zip(braces, new_people)
            ],
            *[
                ApplyMethod(
                    brace.count_tracker.set_value,
                    10 * brace.count_tracker.get_value(),
                )
                for brace in braces
            ],
        )

        farmers = VGroup(farmers, *new_farmers)
        librarians = VGroup(librarians, *new_librarians)
        everyone = VGroup(farmers, librarians)

        # Add background rectangles
        big_rect = SurroundingRectangle(
            everyone,
            buff=0.05,
            stroke_width=1,
            stroke_color=WHITE,
            fill_opacity=1,
            fill_color=GREY_E,
        )
        left_rect = big_rect.copy()
        prior = 1 / 21
        left_rect.stretch(prior, 0, about_edge=LEFT)
        right_rect = big_rect.copy()
        right_rect.stretch(1 - prior, 0, about_edge=RIGHT)

        dl_rect = left_rect.copy()
        ul_rect = left_rect.copy()
        dl_rect.stretch(0.4, 1, about_edge=DOWN)
        ul_rect.stretch(0.6, 1, about_edge=UP)

        dr_rect = right_rect.copy()
        ur_rect = right_rect.copy()
        dr_rect.stretch(0.1, 1, about_edge=DOWN)
        ur_rect.stretch(0.9, 1, about_edge=UP)

        colors = [
            interpolate_color(color, BLACK, 0.5)
            for color in [EVIDENCE_COLOR1, EVIDENCE_COLOR2]
        ]
        for rect, color in zip([dl_rect, dr_rect], colors):
            rect.set_fill(color)

        all_rects = VGroup(
            left_rect, right_rect,
            dl_rect, ul_rect, dr_rect, ur_rect,
        )
        all_rects.set_opacity(0)

        self.add(all_rects, everyone)
        self.play(
            left_rect.set_opacity, 1,
            right_rect.set_opacity, 1,
        )
        self.wait()

        # 40% of librarians and 10% of farmers
        for rect, vect in zip([dl_rect, dr_rect], [LEFT, RIGHT]):
            rect.set_opacity(1)
            rect.save_state()
            rect.brace = Brace(rect, vect, buff=SMALL_BUFF)
            rect.brace.save_state()

            rect.number = Integer(0, unit="\\%")
            rect.number.scale(0.75)
            rect.number.next_to(rect.brace, vect, SMALL_BUFF)
            rect.number.brace = rect.brace
            rect.number.vect = vect

            rect.number.add_updater(
                lambda d: d.set_value(100 * d.brace.get_height() / big_rect.get_height())
            )
            rect.number.add_updater(lambda d: d.next_to(d.brace, d.vect, SMALL_BUFF))

            for mob in [rect, rect.brace]:
                mob.stretch(0, 1, about_edge=DOWN)

        for rect, to_fade in [(dl_rect, librarians[4:]), (dr_rect, farmers[1:])]:
            self.add(rect.brace, rect.number)
            self.play(
                Restore(rect),
                Restore(rect.brace),
                to_fade.set_opacity, 0.1,
            )
            self.wait()

        # Emphasize restricted set
        highlighted_librarians = librarians[:4].copy()
        highlighted_farmers = farmers[0].copy()
        for highlights in [highlighted_librarians, highlighted_farmers]:
            highlights.set_color(YELLOW)

        self.add(braces, *[b.count for b in braces])
        self.play(
            l_brace.next_to, librarians[:4], UP, SMALL_BUFF,
            l_brace.count_tracker.set_value, 4,
            ShowIncreasingSubsets(highlighted_librarians)
        )
        self.play(FadeOut(highlighted_librarians))
        self.play(
            f_brace.next_to, farmers[:1], UP, SMALL_BUFF,
            f_brace.count_tracker.set_value, 20,
            ShowIncreasingSubsets(highlighted_farmers),
            run_time=2,
        )
        self.play(FadeOut(highlighted_farmers))
        self.wait()

        # Write answer
        equation = OldTex(
            "P\\left(",
            "\\text{Librarian }",
            "\\text{given }",
            "\\text{description}",
            "\\right)",
            "=",
            "{4", "\\over", " 4", "+", "20}",
            "\\approx", "16.7\\%",
        )
        equation.set_color_by_tex_to_color_map({
            "Librarian": HYPOTHESIS_COLOR,
            "description": EVIDENCE_COLOR1,
        })

        equation.set_width(FRAME_WIDTH - 2)
        equation.to_edge(UP)
        equation_rect = BackgroundRectangle(equation, buff=MED_SMALL_BUFF)
        equation_rect.set_fill(opacity=1)
        equation_rect.set_stroke(WHITE, width=1, opacity=1)

        self.play(
            FadeIn(equation_rect),
            FadeInFromDown(equation[:6])
        )
        self.wait()
        self.play(
            TransformFromCopy(
                # CHANGE: freeze the counter's copy so that its updater does not replace the points during the morph.
                l_brace.count.copy().clear_updaters(),
                equation.get_parts_by_tex("4")[0],
            ),
            Write(equation.get_part_by_tex("\\over")),
        )
        self.play(
            Write(equation.get_part_by_tex("+")),
            TransformFromCopy(
                # CHANGE: freeze the counter's copy so that its updater does not replace the points during the morph.
                f_brace.count.copy().clear_updaters(),
                equation.get_part_by_tex("20"),
            ),
            TransformFromCopy(
                # CHANGE: freeze the counter's copy so that its updater does not replace the points during the morph.
                l_brace.count.copy().clear_updaters(),
                equation.get_parts_by_tex("4")[1],
            ),
        )

        self.wait()
        self.play(FadeIn(equation[-2:]))
        self.wait()

        # Compare raw likelihoods
        axes = Axes(
            x_min=0,
            x_max=10,
            y_min=0,
            y_max=100,
            y_axis_config={
                "unit_size": 0.07,
                "tick_frequency": 10,
            },
            axis_config={
                "include_tip": False,
            },
        )
        axes.x_axis.tick_marks.set_opacity(0)
        axes.y_axis.add_numbers(
            *range(20, 120, 20),
            unit="\\%"
        )
        axes.center().to_edge(DOWN)

        title = OldTexText("Likelihood of fitting the description")
        title.scale(1.25)
        title.to_edge(UP)
        title.shift(RIGHT)
        axes.add(title)

        lines = VGroup(
            Line(axes.c2p(3, 0), axes.c2p(3, 40)),
            Line(axes.c2p(7, 0), axes.c2p(7, 10)),
        )
        rects = VGroup(*[Rectangle() for x in range(2)])
        rects.set_fill(EVIDENCE_COLOR1, 1)
        rects[1].set_fill(GREEN)
        rects.set_stroke(WHITE, 1)
        icons = VGroup(LibrarianIcon(), FarmerIcon())

        for rect, line, icon in zip(rects, lines, icons):
            rect.replace(line, dim_to_match=1)
            rect.set_width(1, stretch=True)
            icon.set_width(1)
            icon.next_to(rect, UP)
            y = axes.y_axis.p2n(rect.get_top())
            y_point = axes.y_axis.n2p(y)
            rect.line = DashedLine(y_point, rect.get_corner(UL))

        pre_rects = VGroup()
        for r in dl_rect, dr_rect:
            r_copy = r.deepcopy()
            pre_rects.add(r_copy)

        people_copy = VGroup(librarians[:4], farmers[:1]).copy()
        everything = self.get_mobjects()

        self.play(
            *[FadeOut(mob) for mob in everything],
            FadeIn(axes),
            FadeIn(icons),
            *[
                TransformFromCopy(pr, r)
                for pr, r in zip(pre_rects, rects)
            ],
            FadeOut(people_copy),
        )
        self.play(*[
            ShowCreation(rect.line)
            for rect in rects
        ])
        self.wait()
        self.play(
            FadeOut(axes),
            FadeOut(rects[0].line),
            FadeOut(rects[1].line),
            FadeOut(icons),
            *[
                ReplacementTransform(r, pr)
                for pr, r in zip(pre_rects, rects)
            ],
            # FadeOut(fsfr),
            *[FadeIn(mob) for mob in everything],
        )
        self.remove(*pre_rects)
        self.wait()

        # Emphasize prior belief
        prior_equation = OldTex(
            "P\\left(",
            "\\text{Librarian}",
            "\\right)",
            "=",
            "{1", "\\over", "21}",
            "\\approx", "4.8\\%",
        )
        prior_equation.set_color_by_tex_to_color_map({
            "Librarian": HYPOTHESIS_COLOR,
        })

        prior_equation.match_height(equation)

        prior_rect = BackgroundRectangle(prior_equation, buff=MED_SMALL_BUFF)
        prior_rect.match_style(equation_rect)

        group = VGroup(prior_equation, prior_rect)
        group.align_to(equation_rect, UP)
        group.shift(
            (
                equation.get_part_by_tex("\\over").get_x() -
                prior_equation.get_part_by_tex("\\over").get_x()
            ) * RIGHT
        )

        prior_label = OldTexText("Prior belief")
        prior_label.scale(1.5)
        prior_label.next_to(prior_rect, LEFT, buff=1.5)
        prior_label.to_edge(UP, buff=0.25)
        prior_label.set_stroke(BLACK, 5, background=True)
        prior_arrow = Arrow(
            prior_label.get_right(),
            prior_equation.get_left(),
            buff=SMALL_BUFF,
        )

        self.play(
            VGroup(equation_rect, equation).shift, prior_rect.get_height() * DOWN,
            FadeIn(prior_rect),
            FadeIn(prior_equation),
            FadeIn(prior_label, RIGHT),
            GrowArrow(prior_arrow),
        )
        self.wait()
