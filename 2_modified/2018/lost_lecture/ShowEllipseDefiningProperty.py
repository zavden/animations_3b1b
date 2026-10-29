# ==============================================================================
# Scene:      ShowEllipseDefiningProperty
# Source:     videos/_2018/lost_lecture.py (lines 1185-1465)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowEllipseDefiningProperty.py ShowEllipseDefiningProperty -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ImageMobject has no pixel_array in ManimGL; scaling the RGBA pixels by a is the same as set_opacity(a)
# ==============================================================================

from manim_imports_ext import *

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
