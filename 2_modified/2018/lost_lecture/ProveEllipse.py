# ==============================================================================
# Scene:      ProveEllipse
# Source:     videos/_2018/lost_lecture.py (lines 1525-2102)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ProveEllipse.py ProveEllipse -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
#   - Mobject.get_color(vmobject) reads data[rgba] which VMobjects do not have in GL; call the bound get_color
# ==============================================================================

from manim_imports_ext import *

COBALT = "#0047AB"


# TODO, this is untested after turning it from a
# ContinualAnimation into a VGroup
class Orbiting(VGroup):
    CONFIG = {
        "rate": 7.5,
    }

    def __init__(self, planet, star, ellipse, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.add(planet)
        self.planet = planet
        self.star = star
        self.ellipse = ellipse
        # Proportion of the way around the ellipse
        self.proportion = 0
        planet.move_to(ellipse.point_from_proportion(0))

        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        # time = self.internal_time

        planet = self.planet
        star = self.star
        ellipse = self.ellipse

        rate = self.rate
        radius_vector = planet.get_center() - star.get_center()
        rate *= 1.0 / get_norm(radius_vector)

        prop = self.proportion
        d_prop = 0.001
        ds = get_norm(op.add(
            ellipse.point_from_proportion((prop + d_prop) % 1),
            -ellipse.point_from_proportion(prop),
        ))

        delta_prop = (d_prop / ds) * rate * dt

        self.proportion = (self.proportion + delta_prop) % 1
        planet.move_to(
            ellipse.point_from_proportion(self.proportion)
        )


# TODO, this is untested after turning it from a
# ContinualAnimation into a Group
class SunAnimation(Group):
    CONFIG = {
        "rate": 0.2,
        "angle": 60 * DEGREES,
    }

    def __init__(self, sun, **kwargs):
        Group.__init__(self, **kwargs)
        self.sun = sun
        self.rotated_sun = sun.deepcopy()
        self.rotated_sun.rotate(60 * DEGREES)
        self.time = 0

        self.add(self.sun, self.rotated_sun)
        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        time = self.time
        self.time += dt
        a = (np.sin(self.rate * time * TAU) + 1) / 2.0
        self.rotated_sun.rotate(-self.angle)
        self.rotated_sun.move_to(self.sun)
        self.rotated_sun.rotate(self.angle)
        # CHANGE: ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
        self.rotated_sun.set_opacity(a)


class ShowEmergingEllipse(Scene):
    CONFIG = {
        "circle_radius": 3,
        "circle_color": BLUE,
        "num_lines": 150,
        "lines_stroke_width": 1,
        "eccentricity_vector": 2 * RIGHT,
        "ghost_lines_stroke_color": GREY_B,
        "ghost_lines_stroke_width": 0.5,
        "ellipse_color": PINK,
    }

    def construct(self):
        circle = self.get_circle()
        e_point = self.get_eccentricity_point()
        e_dot = Dot(e_point, color=YELLOW)
        lines = self.get_lines()
        ellipse = self.get_ellipse()

        fade_rect = FullScreenFadeRectangle()

        line = lines[len(lines) // 5]
        line_dot = Dot(line.get_center(), color=YELLOW)
        line_dot.scale(0.5)

        ghost_line = self.get_ghost_lines(line)
        ghost_lines = self.get_ghost_lines(lines)

        rot_words = OldTexText("Rotate $90^\\circ$ \\\\ about center")
        rot_words.next_to(line_dot, RIGHT)

        elbow = self.get_elbow(line)

        eccentric_words = OldTexText("``Eccentric'' point")
        eccentric_words.next_to(circle.get_center(), DOWN)

        ellipse_words = OldTexText("Perfect ellipse")
        ellipse_words.next_to(ellipse, UP, SMALL_BUFF)

        for text in rot_words, ellipse_words:
            text.add_to_back(text.copy().set_stroke(BLACK, 5))

        shuffled_lines = VGroup(*lines)
        random.shuffle(shuffled_lines.submobjects)

        self.play(ShowCreation(circle))
        self.play(
            FadeIn(e_dot, LEFT),
            Write(eccentric_words, run_time=1)
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, shuffled_lines),
            Animation(VGroup(e_dot, circle)),
            FadeOut(eccentric_words)
        )
        self.add(ghost_lines)
        self.add(e_dot, circle)
        self.wait()
        self.play(
            FadeIn(fade_rect),
            Animation(line),
            GrowFromCenter(line_dot),
            FadeInFromDown(rot_words),
        )
        self.wait()
        self.add(ghost_line)
        self.play(
            MoveToTarget(line, path_arc=90 * DEGREES),
            Animation(rot_words),
            ShowCreation(elbow)
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
            FadeOut(line_dot),
            FadeOut(rot_words),
            FadeOut(elbow),
            Animation(line),
            Animation(ghost_line)
        )
        self.play(
            LaggedStartMap(MoveToTarget, lines, run_time=4),
            Animation(VGroup(e_dot, circle))
        )
        self.wait()
        self.play(
            ShowCreation(ellipse),
            FadeInFromDown(ellipse_words)
        )
        self.wait()

    def get_circle(self):
        circle = self.circle = Circle(
            radius=self.circle_radius,
            color=self.circle_color
        )
        return circle

    def get_eccentricity_point(self):
        return self.circle.get_center() + self.eccentricity_vector

    def get_lines(self):
        center = self.circle.get_center()
        radius = self.circle.get_width() / 2
        e_point = self.get_eccentricity_point()
        lines = VGroup(*[
            Line(
                e_point,
                center + rotate_vector(radius * RIGHT, angle)
            )
            for angle in np.linspace(0, TAU, self.num_lines)
        ])
        lines.set_stroke(width=self.lines_stroke_width)
        for line in lines:
            line.generate_target()
            line.target.rotate(90 * DEGREES)
        return lines

    def get_ghost_lines(self, lines):
        return lines.copy().set_stroke(
            color=self.ghost_lines_stroke_color,
            width=self.ghost_lines_stroke_width
        )

    def get_elbow(self, line):
        elbow = VGroup(Line(UP, UL), Line(UL, LEFT))
        elbow.set_stroke(width=1)
        elbow.scale(0.2, about_point=ORIGIN)
        elbow.rotate(
            line.get_angle() - 90 * DEGREES,
            about_point=ORIGIN
        )
        elbow.shift(line.get_center())
        return elbow

    def get_ellipse(self):
        center = self.circle.get_center()
        e_point = self.get_eccentricity_point()
        radius = self.circle.get_width() / 2

        # Ellipse parameters
        a = radius / 2
        c = get_norm(e_point - center) / 2
        b = np.sqrt(a**2 - c**2)

        result = Circle(radius=b, color=self.ellipse_color)
        result.stretch(a / b, 0)
        result.move_to(Line(center, e_point))
        return result


class ShowEllipseDefiningProperty(Scene):
    CONFIG = {
        "camera_config": {"background_opacity": 1},
        "ellipse_color": BLUE,
        "a": 4.0,
        "b": 3.0,
        "distance_labels_scale_factor": 1.0,
    }

    def construct(self):
        self.add_ellipse()
        self.add_focal_lines()
        self.add_distance_labels()
        self.label_foci()
        self.label_focal_sum()

    def add_ellipse(self):
        a = self.a
        b = self.b
        ellipse = Circle(radius=a, color=self.ellipse_color)
        ellipse.stretch(fdiv(b, a), dim=1)
        ellipse.to_edge(LEFT, buff=LARGE_BUFF)
        self.ellipse = ellipse
        self.add(ellipse)

    def add_focal_lines(self):
        push_pins = VGroup(*[
            SVGMobject(
                file_name="push_pin",
                color=GREY_B,
                fill_opacity=0.8,
                height=0.5,
            ).move_to(point, DR).shift(0.05 * RIGHT)
            for point in self.get_foci()
        ])

        dot = Dot()
        dot.scale(0.5)
        position_tracker = ValueTracker(0.125)
        dot_update = Mobject.add_updater(
            dot,
            lambda d: d.move_to(
                self.ellipse.point_from_proportion(
                    position_tracker.get_value() % 1
                )
            )
        )
        always_shift(position_tracker, rate=0.05)

        lines, lines_update_animation = self.get_focal_lines_and_update(
            self.get_foci, dot
        )

        self.add_foreground_mobjects(push_pins, dot)
        self.add(dot_update)
        self.play(LaggedStartMap(
            FadeInFrom, push_pins,
            lambda m: (m, 2 * UP + LEFT),
            run_time=1,
            lag_ratio=0.75
        ))
        self.play(ShowCreation(lines))
        self.add(lines_update_animation)
        self.add(position_tracker)
        self.wait(2)

        self.position_tracker = position_tracker
        self.focal_lines = lines

    def add_distance_labels(self):
        lines = self.focal_lines
        colors = [YELLOW, PINK]

        distance_labels, distance_labels_animation = \
            self.get_distance_labels_and_update(lines, colors)

        sum_expression, numbers, number_updates = \
            self.get_sum_expression_and_update(
                lines, colors, lambda mob: mob.to_corner(UR)
            )

        sum_expression_fading_rect = BackgroundRectangle(
            sum_expression, fill_opacity=1
        )

        sum_rect = SurroundingRectangle(numbers[-1])
        constant_words = OldTexText("Stays constant")
        constant_words.next_to(sum_rect, DOWN, aligned_edge=RIGHT)
        VGroup(sum_rect, constant_words).set_color(BLUE)

        self.add(distance_labels_animation)
        self.add(*number_updates)
        self.add(sum_expression)
        self.add_foreground_mobjects(sum_expression_fading_rect)
        self.play(
            VFadeIn(distance_labels),
            FadeOut(sum_expression_fading_rect),
        )
        self.remove_foreground_mobject(sum_expression_fading_rect)
        self.wait(7)
        self.play(
            ShowCreation(sum_rect),
            Write(constant_words)
        )
        self.wait(7)
        self.play(FadeOut(sum_rect), FadeOut(constant_words))

        self.sum_expression = sum_expression
        self.sum_rect = sum_rect

    def label_foci(self):
        foci = self.get_foci()
        focus_words = VGroup(*[
            OldTexText("Focus").next_to(focus, DOWN)
            for focus in foci
        ])
        foci_word = OldTexText("Foci")
        foci_word.move_to(focus_words)
        foci_word.shift(MED_SMALL_BUFF * UP)
        connecting_lines = VGroup(*[
            Arrow(
                foci_word.get_edge_center(-edge),
                focus_word.get_edge_center(edge),
                buff=MED_SMALL_BUFF,
                stroke_width=2,
            )
            for focus_word, edge in zip(focus_words, [LEFT, RIGHT])
        ])

        translation = OldTexText(
            "``Foco'' $\\rightarrow$ Fireplace"
        )
        translation.to_edge(RIGHT)
        translation.shift(UP)
        sun = ImageMobject("sun", height=0.5)
        sun.move_to(foci[0])
        sun_animation = SunAnimation(sun)

        self.play(FadeInFromDown(focus_words))
        self.wait(2)
        self.play(
            ReplacementTransform(focus_words.copy(), foci_word),
        )
        self.play(*list(map(ShowCreation, connecting_lines)))
        for word in list(focus_words) + [foci_word]:
            word.add_background_rectangle()
            self.add_foreground_mobjects(word)
        self.wait(4)
        self.play(Write(translation))
        self.wait(2)
        self.play(GrowFromCenter(sun))
        self.add(sun_animation)
        self.wait(8)

    def label_focal_sum(self):
        sum_rect = self.sum_rect

        focal_sum = OldTexText("``Focal sum''")
        focal_sum.scale(1.5)
        focal_sum.next_to(sum_rect, DOWN, aligned_edge=RIGHT)
        VGroup(sum_rect, focal_sum).set_color(RED)

        footnote = OldTexText(
            """
            \\Large
            *This happens to equal the longest distance
            across the ellipse, so perhaps the more standard
            terminology would be ``major axis'', but I want
            some terminology that conveys the idea of adding
            two distances to the foci.
            """,
            alignment="",
        )
        footnote.set_width(5)
        footnote.to_corner(DR)
        footnote.set_stroke(WHITE, 0.5)

        self.play(FadeInFromDown(focal_sum))
        self.play(Write(sum_rect))
        self.wait()
        self.play(FadeIn(footnote))
        self.wait(2)
        self.play(FadeOut(footnote))
        self.wait(8)

    # Helpers
    def get_foci(self):
        ellipse = self.ellipse
        a = ellipse.get_width() / 2
        b = ellipse.get_height() / 2
        c = np.sqrt(a**2 - b**2)
        center = ellipse.get_center()
        return [
            center + c * RIGHT,
            center + c * LEFT,
        ]

    def get_focal_lines_and_update(self, get_foci, focal_sum_point):
        lines = VGroup(Line(LEFT, RIGHT), Line(LEFT, RIGHT))
        lines.set_stroke(width=2)

        def update_lines(lines):
            foci = get_foci()
            for line, focus in zip(lines, foci):
                line.put_start_and_end_on(
                    focus, focal_sum_point.get_center()
                )
            lines[1].rotate(np.pi)
        lines_update_animation = Mobject.add_updater(
            lines, update_lines
        )
        return lines, lines_update_animation

    def get_distance_labels_and_update(self, lines, colors):
        distance_labels = VGroup(
            DecimalNumber(0), DecimalNumber(0),
        )
        for label in distance_labels:
            label.scale(self.distance_labels_scale_factor)

        def update_distance_labels(labels):
            for label, line, color in zip(labels, lines, colors):
                angle = -line.get_angle()
                if np.abs(angle) > 90 * DEGREES:
                    angle = 180 * DEGREES + angle
                line.rotate(angle, about_point=ORIGIN)
                new_decimal = DecimalNumber(line.get_length())
                new_decimal.scale(
                    self.distance_labels_scale_factor
                )
                max_width = 0.6 * line.get_width()
                if new_decimal.get_width() > max_width:
                    new_decimal.set_width(max_width)
                new_decimal.next_to(line, UP, SMALL_BUFF)
                new_decimal.set_color(color)
                new_decimal.add_to_back(
                    new_decimal.copy().set_stroke(BLACK, 5)
                )
                VGroup(new_decimal, line).rotate(
                    -angle, about_point=ORIGIN
                )
                label.submobjects = list(new_decimal.submobjects)

        distance_labels_animation = Mobject.add_updater(
            distance_labels, update_distance_labels
        )

        return distance_labels, distance_labels_animation

    def get_sum_expression_and_update(self, lines, colors, sum_position_func):
        sum_expression = OldTex("0.00", "+", "0.00", "=", "0.00")
        sum_position_func(sum_expression)
        number_refs = sum_expression.get_parts_by_tex("0.00")
        number_refs.set_fill(opacity=0)
        numbers = VGroup(*[DecimalNumber(0) for ref in number_refs])
        for number, color in zip(numbers, colors):
            number.set_color(color)

        # Not the most elegant...
        number_updates = [
            ContinualChangingDecimal(
                numbers[0], lambda a: lines[0].get_length(),
                position_update_func=lambda m: m.move_to(
                    number_refs[1], LEFT
                )
            ),
            ContinualChangingDecimal(
                numbers[1], lambda a: lines[1].get_length(),
                position_update_func=lambda m: m.move_to(
                    number_refs[0], LEFT
                )
            ),
            ContinualChangingDecimal(
                numbers[2], lambda a: sum(map(Line.get_length, lines)),
                position_update_func=lambda m: m.move_to(
                    number_refs[2], LEFT
                )
            ),
        ]

        return sum_expression, numbers, number_updates


class ProveEllipse(ShowEmergingEllipse, ShowEllipseDefiningProperty):
    CONFIG = {
        "eccentricity_vector": 1.5 * RIGHT,
        "ellipse_color": PINK,
        "distance_labels_scale_factor": 0.7,
    }

    def construct(self):
        self.setup_ellipse()
        self.hypothesize_foci()
        self.setup_and_show_focal_sum()
        self.show_circle_radius()
        self.limit_to_just_one_line()
        self.look_at_perpendicular_bisector()
        self.show_orbiting_planet()

    def setup_ellipse(self):
        circle = self.circle = self.get_circle()
        circle.to_edge(LEFT)
        ep = self.get_eccentricity_point()
        ep_dot = self.ep_dot = Dot(ep, color=YELLOW)
        lines = self.lines = self.get_lines()
        for line in lines:
            line.save_state()
        ghost_lines = self.ghost_lines = self.get_ghost_lines(lines)
        ellipse = self.ellipse = self.get_ellipse()

        self.add(ghost_lines, circle, lines, ep_dot)
        self.play(
            LaggedStartMap(MoveToTarget, lines),
            Animation(ep_dot),
        )
        self.play(ShowCreation(ellipse))
        self.wait()

    def hypothesize_foci(self):
        circle = self.circle
        ghost_lines = self.ghost_lines
        ghost_lines_copy = ghost_lines.copy().set_stroke(YELLOW, 3)

        center = circle.get_center()
        center_dot = Dot(center, color=RED)
        # ep = self.get_eccentricity_point()
        ep_dot = self.ep_dot
        dots = VGroup(center_dot, ep_dot)

        center_label = OldTexText("Circle center")
        ep_label = OldTexText("Eccentric point")
        labels = VGroup(center_label, ep_label)
        vects = [UL, DR]
        arrows = VGroup()
        for label, dot, vect in zip(labels, dots, vects):
            label.next_to(dot, vect, MED_LARGE_BUFF)
            label.match_color(dot)
            label.add_to_back(
                label.copy().set_stroke(BLACK, 5)
            )
            arrow = Arrow(
                label.get_corner(-vect),
                dot.get_corner(vect),
                buff=SMALL_BUFF
            )
            arrow.match_color(dot)
            arrow.add_to_back(arrow.copy().set_stroke(BLACK, 5))
            arrows.add(arrow)

        labels_target = labels.copy()
        labels_target.arrange(
            DOWN, aligned_edge=LEFT
        )
        guess_start = OldTexText("Guess: Foci = ")
        brace = Brace(labels_target, LEFT)
        full_guess = VGroup(guess_start, brace, labels_target)
        full_guess.arrange(RIGHT)
        full_guess.to_corner(UR)

        self.play(
            FadeInFromDown(labels[1]),
            GrowArrow(arrows[1]),
        )
        self.play(LaggedStartMap(
            ShowPassingFlash, ghost_lines_copy
        ))
        self.wait()
        self.play(ReplacementTransform(circle.copy(), center_dot))
        self.add_foreground_mobjects(dots)
        self.play(
            FadeInFromDown(labels[0]),
            GrowArrow(arrows[0]),
        )
        self.wait()
        self.play(
            Write(guess_start),
            GrowFromCenter(brace),
            run_time=1
        )
        self.play(
            ReplacementTransform(labels.copy(), labels_target)
        )
        self.wait()
        self.play(FadeOut(labels), FadeOut(arrows))

        self.center_dot = center_dot

    def setup_and_show_focal_sum(self):
        circle = self.circle
        ellipse = self.ellipse

        focal_sum_point = VectorizedPoint()
        focal_sum_point.move_to(circle.get_top())
        dots = [self.ep_dot, self.center_dot]
        # CHANGE: Mobject.get_color(vmobject) reads data[rgba] which VMobjects do not have in GL; call the bound get_color
        colors = [dot.get_color() for dot in dots]

        def get_foci():
            return list(map(Mobject.get_center, dots))

        focal_lines, focal_lines_update_animation = \
            self.get_focal_lines_and_update(get_foci, focal_sum_point)
        distance_labels, distance_labels_update_animation = \
            self.get_distance_labels_and_update(focal_lines, colors)
        sum_expression, numbers, number_updates = \
            self.get_sum_expression_and_update(
                focal_lines, colors,
                lambda mob: mob.to_edge(RIGHT).shift(UP)
            )

        to_add = self.focal_sum_things_to_add = [
            focal_lines_update_animation,
            distance_labels_update_animation,
            sum_expression,
        ] + list(number_updates)

        self.play(
            ShowCreation(focal_lines),
            Write(distance_labels),
            FadeIn(sum_expression),
            Write(numbers),
            run_time=1
        )
        self.wait()
        self.add(*to_add)

        points = [
            ellipse.get_top(),
            circle.point_from_proportion(0.2),
            ellipse.point_from_proportion(0.2),
            ellipse.point_from_proportion(0.4),
        ]
        for point in points:
            self.play(
                focal_sum_point.move_to, point
            )
            self.wait()
        self.remove(*to_add)
        self.play(*list(map(FadeOut, [
            focal_lines, distance_labels,
            sum_expression, numbers
        ])))

        self.set_variables_as_attrs(
            focal_lines, focal_lines_update_animation,
            focal_sum_point,
            distance_labels, distance_labels_update_animation,
            sum_expression,
            numbers, number_updates
        )

    def show_circle_radius(self):
        circle = self.circle
        center = circle.get_center()
        point = circle.get_right()
        color = GREEN
        radius = Line(center, point, color=color)
        radius_measurement = DecimalNumber(radius.get_length())
        radius_measurement.set_color(color)
        radius_measurement.next_to(radius, UP, SMALL_BUFF)
        radius_measurement.add_to_back(
            radius_measurement.copy().set_stroke(BLACK, 5)
        )
        group = VGroup(radius, radius_measurement)
        group.rotate(30 * DEGREES, about_point=center)

        self.play(ShowCreation(radius))
        self.play(Write(radius_measurement))
        self.wait()
        self.play(Rotating(
            group,
            rate_func=smooth,
            run_time=7,
            about_point=center
        ))
        self.play(FadeOut(group))

    def limit_to_just_one_line(self):
        lines = self.lines
        ghost_lines = self.ghost_lines
        ep_dot = self.ep_dot

        index = int(0.2 * len(lines))
        line = lines[index]
        ghost_line = ghost_lines[index]
        to_fade = VGroup(*list(lines) + list(ghost_lines))
        to_fade.remove(line, ghost_line)

        P_dot = Dot(line.saved_state.get_end())
        P_label = OldTex("P")
        P_label.next_to(P_dot, UP, SMALL_BUFF)

        self.add_foreground_mobjects(self.ellipse)
        self.play(LaggedStartMap(Restore, lines))
        self.play(
            FadeOut(to_fade),
            ghost_line.set_stroke, YELLOW, 3,
            line.set_stroke, WHITE, 3,
            ReplacementTransform(ep_dot.copy(), P_dot),
        )
        self.play(FadeInFromDown(P_label))
        self.wait()

        for l in lines:
            l.generate_target()
            l.target.rotate(
                90 * DEGREES,
                about_point=l.get_center()
            )

        self.set_variables_as_attrs(
            line, ghost_line,
            P_dot, P_label
        )

    def look_at_perpendicular_bisector(self):
        # Alright, this method's gonna blow up.  Let's go!
        circle = self.circle
        ellipse = self.ellipse
        ellipse.save_state()
        lines = self.lines
        line = self.line
        ghost_lines = self.ghost_lines
        ghost_line = self.ghost_line
        P_dot = self.P_dot
        P_label = self.P_label

        elbow = self.get_elbow(line)
        self.play(
            MoveToTarget(line, path_arc=90 * DEGREES),
            ShowCreation(elbow)
        )

        # Perpendicular bisector label
        label = OldTexText("``Perpendicular bisector''")
        label.scale(0.75)
        label.set_color(YELLOW)
        label.next_to(ORIGIN, UP, MED_SMALL_BUFF)
        label.add_background_rectangle()
        angle = line.get_angle() + np.pi
        label.rotate(angle, about_point=ORIGIN)
        label.shift(line.get_center())

        # Dot defining Q point
        Q_dot = Dot(color=GREEN)
        Q_dot.move_to(self.focal_sum_point)
        focal_sum_point_animation = turn_animation_into_updater(
            MaintainPositionRelativeTo(
                self.focal_sum_point, Q_dot
            )
        )
        self.add(focal_sum_point_animation)
        Q_dot.move_to(line.point_from_proportion(0.9))
        Q_dot.save_state()

        Q_label = OldTex("Q")
        Q_label.scale(0.7)
        Q_label.match_color(Q_dot)
        Q_label.add_to_back(Q_label.copy().set_stroke(BLACK, 5))
        Q_label.next_to(Q_dot, UL, buff=0)
        Q_label_animation = turn_animation_into_updater(
            MaintainPositionRelativeTo(Q_label, Q_dot)
        )

        # Pretty hacky...
        def distance_label_shift_update(label):
            line = self.focal_lines[0]
            if line.get_end()[0] > line.get_start()[0]:
                vect = label.get_center() - line.get_center()
                label.shift(-2 * vect)
        distance_label_shift_update_animation = Mobject.add_updater(
            self.distance_labels[0],
            distance_label_shift_update
        )
        self.focal_sum_things_to_add.append(
            distance_label_shift_update_animation
        )

        # Define QP line
        QP_line = Line(LEFT, RIGHT)
        QP_line.match_style(self.focal_lines)
        QP_line_update = Mobject.add_updater(
            QP_line, lambda l: l.put_start_and_end_on(
                Q_dot.get_center(), P_dot.get_center(),
            )
        )

        QE_line = Line(LEFT, RIGHT)
        QE_line.set_stroke(YELLOW, 3)
        QE_line_update = Mobject.add_updater(
            QE_line, lambda l: l.put_start_and_end_on(
                Q_dot.get_center(),
                self.get_eccentricity_point()
            )
        )

        # Define similar triangles
        triangles = VGroup(*[
            Polygon(
                Q_dot.get_center(),
                line.get_center(),
                end_point,
                fill_opacity=1,
            )
            for end_point in [
                P_dot.get_center(),
                self.get_eccentricity_point()
            ]
        ])
        triangles.set_color_by_gradient(RED_C, COBALT)
        triangles.set_stroke(WHITE, 2)

        # Add even more distant label updates
        def distance_label_rotate_update(label):
            QE_line_update.update(0)
            angle = QP_line.get_angle() - QE_line.get_angle()
            label.rotate(angle, about_point=Q_dot.get_center())
            return label

        distance_label_rotate_update_animation = Mobject.add_updater(
            self.distance_labels[0],
            distance_label_rotate_update
        )

        # Hook up line to P to P_dot
        radial_line = DashedLine(ORIGIN, 3 * RIGHT)
        radial_line_update = UpdateFromFunc(
            radial_line, lambda l: l.put_start_and_end_on(
                circle.get_center(),
                P_dot.get_center()
            )
        )

        def put_dot_at_intersection(dot):
            point = line_intersection(
                line.get_start_and_end(),
                radial_line.get_start_and_end()
            )
            dot.move_to(point)
            return dot

        keep_Q_dot_at_intersection = UpdateFromFunc(
            Q_dot, put_dot_at_intersection
        )
        Q_dot.restore()

        ghost_line_update_animation = UpdateFromFunc(
            ghost_line, lambda l: l.put_start_and_end_on(
                self.get_eccentricity_point(),
                P_dot.get_center()
            )
        )

        def update_perp_bisector(line):
            line.scale(ghost_line.get_length() / line.get_length())
            line.rotate(ghost_line.get_angle() - line.get_angle())
            line.rotate(90 * DEGREES)
            line.move_to(ghost_line)
        perp_bisector_update_animation = UpdateFromFunc(
            line, update_perp_bisector
        )
        elbow_update_animation = UpdateFromFunc(
            elbow,
            lambda e: Transform(e, self.get_elbow(ghost_line)).update(1)
        )

        P_dot_movement_updates = [
            radial_line_update,
            keep_Q_dot_at_intersection,
            MaintainPositionRelativeTo(
                P_label, P_dot
            ),
            ghost_line_update_animation,
            perp_bisector_update_animation,
            elbow_update_animation,
        ]

        # Comment for tangency
        sum_rect = SurroundingRectangle(
            self.numbers[-1]
        )
        tangency_comment = OldTexText(
            "Always $\\ge$ radius"
        )
        tangency_comment.next_to(
            sum_rect, DOWN,
            aligned_edge=RIGHT
        )
        VGroup(sum_rect, tangency_comment).set_color(GREEN)

        # Why is this needed?!?
        self.add(*self.focal_sum_things_to_add)
        self.wait(0.01)
        self.remove(*self.focal_sum_things_to_add)

        # Show label
        self.play(Write(label))
        self.wait()

        # Show Q_dot moving about a little
        self.play(
            FadeOut(label),
            FadeIn(self.focal_lines),
            FadeIn(self.distance_labels),
            FadeIn(self.sum_expression),
            FadeIn(self.numbers),
            ellipse.set_stroke, {"width": 0.5},
        )
        self.add(*self.focal_sum_things_to_add)
        self.play(
            FadeInFromDown(Q_label),
            GrowFromCenter(Q_dot)
        )
        self.wait()
        self.add_foreground_mobjects(Q_dot)
        self.add(Q_label_animation)
        self.play(
            Q_dot.move_to, line.point_from_proportion(0.05),
            rate_func=there_and_back,
            run_time=4
        )
        self.wait()

        # Show similar triangles
        self.play(
            FadeIn(triangles[0]),
            ShowCreation(QP_line),
            Animation(elbow),
        )
        self.add(QP_line_update)
        for i in range(3):
            self.play(
                FadeIn(triangles[(i + 1) % 2]),
                FadeOut(triangles[i % 2]),
                Animation(self.distance_labels),
                Animation(elbow)
            )
        self.play(
            FadeOut(triangles[1]),
            Animation(self.distance_labels)
        )

        # Move first distance label
        # (boy, this got messy...hopefully no one ever has
        # to read this.)
        angle = QP_line.get_angle() - QE_line.get_angle()
        Q_point = Q_dot.get_center()
        for x in range(2):
            self.play(ShowCreationThenDestruction(QE_line))
        distance_label_copy = self.distance_labels[0].copy()
        self.play(
            ApplyFunction(
                distance_label_rotate_update,
                distance_label_copy,
                path_arc=angle
            ),
            Rotate(QE_line, angle, about_point=Q_point)
        )
        self.play(FadeOut(QE_line))
        self.remove(distance_label_copy)
        self.add(distance_label_rotate_update_animation)
        self.focal_sum_things_to_add.append(
            distance_label_rotate_update_animation
        )
        self.wait()
        self.play(
            Q_dot.move_to, line.point_from_proportion(0),
            run_time=4,
            rate_func=there_and_back
        )

        # Trace out ellipse
        self.play(ShowCreation(radial_line))
        self.wait()
        self.play(
            ApplyFunction(put_dot_at_intersection, Q_dot),
            run_time=3,
        )
        self.wait()
        self.play(
            Rotating(
                P_dot,
                about_point=circle.get_center(),
                rate_func=bezier([0, 0, 1, 1]),
                run_time=10,
            ),
            ellipse.restore,
            *P_dot_movement_updates
        )
        self.wait()

        # Talk through tangency
        self.play(
            ShowCreation(sum_rect),
            Write(tangency_comment),
        )
        points = [line.get_end(), line.get_start(), Q_dot.get_center()]
        run_times = [1, 3, 2]
        for point, run_time in zip(points, run_times):
            self.play(Q_dot.move_to, point, run_time=run_time)
        self.wait()

        self.remove(*self.focal_sum_things_to_add)
        self.play(*list(map(FadeOut, [
            radial_line,
            QP_line,
            P_dot, P_label,
            Q_dot, Q_label,
            elbow,
            self.distance_labels,
            self.numbers,
            self.sum_expression,
            sum_rect,
            tangency_comment,
        ])))
        self.wait()

        # Show all lines
        lines.remove(line)
        ghost_lines.remove(ghost_line)
        for line in lines:
            line.generate_target()
            line.target.rotate(90 * DEGREES)
        self.play(
            LaggedStartMap(FadeIn, ghost_lines),
            LaggedStartMap(FadeIn, lines),
        )
        self.play(LaggedStartMap(MoveToTarget, lines))
        self.wait()

    def show_orbiting_planet(self):
        ellipse = self.ellipse
        ep_dot = self.ep_dot
        planet = ImageMobject("earth")
        planet.set_height(0.25)
        orbit = Orbiting(planet, ep_dot, ellipse)

        lines = self.lines

        def update_lines(lines):
            for gl, line in zip(self.ghost_lines, lines):
                intersection = line_intersection(
                    [self.circle.get_center(), gl.get_end()],
                    line.get_start_and_end()
                )
                distance = get_norm(
                    intersection - planet.get_center()
                )
                if distance < 0.025:
                    line.set_stroke(BLUE, 3)
                    self.add(line)
                else:
                    line.set_stroke(WHITE, 1)

        lines_update_animation = Mobject.add_updater(
            lines, update_lines
        )

        self.add(orbit)
        self.add(lines_update_animation)
        self.add_foreground_mobjects(planet)
        self.wait(12)
