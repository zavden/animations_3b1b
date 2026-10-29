# ==============================================================================
# Scene:      EllipseLengthsLinedUp
# Source:     videos/_2018/dandelin.py (lines 1580-1626)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EllipseLengthsLinedUp.py EllipseLengthsLinedUp -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
# ==============================================================================

from manim_imports_ext import *

class ShowArrayOfEccentricities(Scene):
    def construct(self):
        eccentricities = np.linspace(0, 0.99, 6)
        eccentricity_labels = VGroup(*list(map(
            DecimalNumber, eccentricities
        )))
        ellipses = self.get_ellipse_row(eccentricities)
        ellipses.set_color_by_gradient(BLUE, YELLOW)
        ellipses.move_to(DOWN)

        for label, ellipse in zip(eccentricity_labels, ellipses):
            label.next_to(ellipse, UP)

        name = OldTexText("Eccentricity")
        name.scale(1.5)
        name.to_edge(UP)
        alt_name = OldTexText("(read ``squishification'')")
        alt_name.set_color(YELLOW)
        alt_name.next_to(name, RIGHT)
        alt_name.shift_onto_screen()
        name.generate_target()
        name.target.next_to(alt_name, LEFT)

        arrows = VGroup(*[
            Arrow(name.get_bottom(), label.get_top())
            for label in eccentricity_labels
        ])
        arrows.set_color_by_gradient(BLUE, YELLOW)

        for label, arrow in zip(eccentricity_labels, arrows):
            label.save_state()
            label.fade(1)
            label.scale(0.1)
            label.move_to(arrow.get_start())

        morty = Mortimer(height=2)
        morty.next_to(alt_name, DOWN)

        self.add(ellipses[0])
        for e1, e2 in zip(ellipses[:-1], ellipses[1:]):
            self.play(ReplacementTransform(
                e1.copy(), e2,
                path_arc=10 * DEGREES
            ))
        self.wait()

        self.play(
            Write(name),
            LaggedStartMap(GrowArrow, arrows),
            LaggedStartMap(Restore, eccentricity_labels)
        )
        self.wait()
        self.play(
            Write(alt_name),
            MoveToTarget(name),
            morty.change, "hooray", alt_name,
            VFadeIn(morty),
        )
        self.play(Blink(morty))
        self.play(morty.change, "thinking", ellipses)
        self.wait()
        self.play(Blink(morty))

        for i in 0, -1:
            e_copy = ellipses[i].copy()
            e_copy.set_color(RED)
            self.play(ShowCreation(e_copy))
            self.play(
                ShowCreationThenFadeAround(
                    eccentricity_labels[i],
                ),
                FadeOut(e_copy)
            )
        self.wait()

        circle = ellipses[0]
        group = VGroup(*it.chain(
            eccentricity_labels,
            ellipses[1:],
            arrows,
            name,
            alt_name,
            [morty]
        ))
        self.play(
            LaggedStartMap(FadeOutAndShiftDown, group),
            circle.set_height, 5,
            circle.center,
        )

    def get_ellipse(self, eccentricity, width=2):
        result = Circle(color=WHITE)
        result.set_width(width)
        a = width / 2.0
        c = eccentricity * a
        b = np.sqrt(a**2 - c**2)
        result.stretch(b / a, 1)
        result.shift(c * LEFT)

        result.eccentricity = eccentricity
        return result

    def get_ellipse_row(self, eccentricities, buff=MED_SMALL_BUFF, **kwargs):
        result = VGroup(*[
            self.get_ellipse(e, **kwargs)
            for e in eccentricities
        ])
        result.arrange(RIGHT, buff=buff)
        return result

    def get_eccentricity(self, ellipse):
        """
        Assumes that it's major/minor axes line up
        with x and y axes
        """
        a = ellipse.get_width()
        b = ellipse.get_height()
        if b > a:
            a, b = b, a
        c = np.sqrt(a**2 - b**2)
        return fdiv(c, a)


class EccentricityInThumbtackCase(ShowArrayOfEccentricities):
    def construct(self):
        ellipse = self.get_ellipse(0.2, width=5)
        ellipse_target = self.get_ellipse(0.9, width=5)
        ellipse_target.scale(fdiv(
            sum(self.get_abc(ellipse)),
            sum(self.get_abc(ellipse_target)),
        ))
        for mob in ellipse, ellipse_target:
            mob.center()
            mob.set_color(BLUE)
        thumbtack_update = self.get_thumbtack_update(ellipse)
        ellipse_point_update = self.get_ellipse_point_update(ellipse)
        focal_lines_update = self.get_focal_lines_update(
            # CHANGE: the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
            ellipse, ellipse_point_update
        )
        focus_to_focus_line_update = self.get_focus_to_focus_line_update(ellipse)
        eccentricity_label = self.get_eccentricity_label()
        eccentricity_value_update = self.get_eccentricity_value_update(
            eccentricity_label, ellipse,
        )
        inner_brace_update = self.get_focus_line_to_focus_line_brace_update(
            # CHANGE: the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
            focus_to_focus_line_update
        )
        outer_lines = self.get_outer_dashed_lines(ellipse)
        outer_lines_brace = Brace(outer_lines, DOWN)

        focus_distance = OldTexText("Focus distance")
        focus_distance.set_color(GREEN)
        # CHANGE: the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
        focus_distance.next_to(inner_brace_update, DOWN, SMALL_BUFF)
        focus_distance.add_to_back(focus_distance.copy().set_stroke(BLACK, 5))
        focus_distance_update = Mobject.add_updater(
            focus_distance,
            lambda m: m.set_width(
                # CHANGE: the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
                inner_brace_update.get_width(),
            # CHANGE: the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
            ).next_to(inner_brace_update, DOWN, SMALL_BUFF)
        )
        diameter = OldTexText("Diameter")
        diameter.set_color(RED)
        diameter.next_to(outer_lines_brace, DOWN, SMALL_BUFF)

        fraction = OldTex(
            "{\\text{Focus distance}", "\\over",
            "\\text{Diameter}}"
        )
        numerator = fraction.get_part_by_tex("Focus")
        numerator.set_color(GREEN)
        fraction.set_color_by_tex("Diameter", RED)
        fraction.move_to(2 * UP)
        fraction.to_edge(RIGHT, buff=MED_LARGE_BUFF)
        numerator_update = Mobject.add_updater(
            numerator,
            lambda m: m.set_width(focus_distance.get_width()).next_to(
                fraction[1], UP, MED_SMALL_BUFF
            )
        )

        fraction_arrow = Arrow(
            eccentricity_label.get_right(),
            fraction.get_top() + MED_SMALL_BUFF * UP,
            path_arc=-60 * DEGREES,
        )
        fraction_arrow.pointwise_become_partial(fraction_arrow, 0, 0.95)

        ellipse_transformation = Transform(
            ellipse, ellipse_target,
            rate_func=there_and_back,
            run_time=8,
        )

        self.add(ellipse)
        self.add(thumbtack_update)
        self.add(ellipse_point_update)
        self.add(focal_lines_update)
        self.add(focus_to_focus_line_update)
        self.add(eccentricity_label)
        self.add(eccentricity_value_update)

        self.play(ellipse_transformation)

        self.add(inner_brace_update)
        self.add(outer_lines)
        self.add(outer_lines_brace)

        self.add(fraction)
        self.add(fraction_arrow)
        self.add(focus_distance)
        self.add(diameter)

        self.add(focus_distance_update)
        self.add(numerator_update)

        self.play(
            ellipse_transformation,
            # CHANGE: the repo already turned these *_update helpers into updaters that return the mobject itself (Mobject.add_updater / cycle_animation), so there is no .mobject attribute
            VFadeIn(inner_brace_update),
            VFadeIn(outer_lines),
            VFadeIn(outer_lines_brace),
            VFadeIn(fraction),
            VFadeIn(fraction_arrow),
            VFadeIn(focus_distance),
            VFadeIn(diameter),
        )

    def get_thumbtack_update(self, ellipse):
        thumbtacks = VGroup(*[
            self.get_thumbtack()
            for x in range(2)
        ])

        def update_thumbtacks(thumbtacks):
            foci = self.get_foci(ellipse)
            for thumbtack, focus in zip(thumbtacks, foci):
                thumbtack.move_to(focus, DR)
            return thumbtacks

        return Mobject.add_updater(thumbtacks, update_thumbtacks)

    def get_ellipse_point_update(self, ellipse):
        dot = Dot(color=RED)
        return cycle_animation(MoveAlongPath(
            dot, ellipse,
            run_time=5,
            rate_func=linear
        ))

    def get_focal_lines_update(self, ellipse, ellipse_point):
        lines = VGroup(*[Line(LEFT, RIGHT) for x in range(2)])
        lines.set_color_by_gradient(YELLOW, PINK)

        def update_lines(lines):
            foci = self.get_foci(ellipse)
            Q = ellipse_point.get_center()
            for line, focus in zip(lines, foci):
                line.put_start_and_end_on(focus, Q)
            return lines

        return Mobject.add_updater(lines, update_lines)

    def get_focus_to_focus_line_update(self, ellipse):
        return Mobject.add_updater(
            Line(LEFT, RIGHT, color=WHITE),
            lambda m: m.put_start_and_end_on(*self.get_foci(ellipse))
        )

    def get_focus_line_to_focus_line_brace_update(self, line):
        brace = Brace(Line(LEFT, RIGHT))
        brace.add_to_back(brace.copy().set_stroke(BLACK, 5))
        return Mobject.add_updater(
            brace,
            lambda b: b.match_width(line, stretch=True).next_to(
                line, DOWN, buff=SMALL_BUFF
            )
        )

    def get_eccentricity_label(self):
        words = OldTexText("Eccentricity = ")
        decimal = DecimalNumber(0, num_decimal_places=2)
        group = VGroup(words, decimal)
        group.arrange(RIGHT)
        group.to_edge(UP)
        return group

    def get_eccentricity_value_update(self, eccentricity_label, ellipse):
        decimal = eccentricity_label[1]
        decimal.add_updater(lambda d: d.set_value(
            self.get_eccentricity(ellipse)
        ))
        return decimal

    def get_outer_dashed_lines(self, ellipse):
        line = DashedLine(2.5 * UP, 2.5 * DOWN)
        return VGroup(
            line.move_to(ellipse, RIGHT),
            line.copy().move_to(ellipse, LEFT),
        )

    #
    def get_abc(self, ellipse):
        a = ellipse.get_width() / 2
        b = ellipse.get_height() / 2
        c = np.sqrt(a**2 - b**2)
        return a, b, c

    def get_foci(self, ellipse):
        a, b, c = self.get_abc(ellipse)
        return [
            ellipse.get_center() + c * RIGHT,
            ellipse.get_center() + c * LEFT,
        ]

    def get_thumbtack(self):
        angle = 10 * DEGREES
        result = SVGMobject(file_name="push_pin")
        result.set_height(0.5)
        result.set_fill(GREY_B)
        result.rotate(angle)
        return result


class EllipseLengthsLinedUp(EccentricityInThumbtackCase):
    def construct(self):
        ellipse = self.get_ellipse(eccentricity=0.6)
        ellipse.scale(2)
        foci = self.get_foci(ellipse)

        point = VectorizedPoint()
        point_movement = cycle_animation(
            MoveAlongPath(
                point, ellipse,
                run_time=5,
                rate_func=linear,
            )
        )

        arrow = Vector(RIGHT, color=WHITE)
        arrow.to_edge(LEFT)
        q_mark = OldTex("?")
        q_mark.next_to(arrow, UP)

        lines = VGroup(*[Line(UP, DOWN) for x in range(2)])
        lines.set_color_by_gradient(PINK, GOLD)
        lines.set_stroke(width=5)

        h_line = Line(LEFT, RIGHT, color=WHITE)
        h_line.set_width(0.25)

        def update_lines(lines):
            for line, focus in zip(lines, foci):
                d = get_norm(point.get_center() - focus)
                line.put_start_and_end_on(
                    ORIGIN, d * UP
                )
            lines.arrange(DOWN, buff=0)
            lines.next_to(arrow, RIGHT)
            h_line.move_to(lines[0].get_bottom())
        lines_animation = Mobject.add_updater(
            lines, update_lines
        )

        self.add(point_movement)
        self.add(arrow)
        self.add(q_mark)
        self.add(h_line)
        self.add(lines_animation)

        self.wait(20)
