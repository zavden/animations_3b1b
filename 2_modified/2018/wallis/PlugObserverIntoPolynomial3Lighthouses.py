# ==============================================================================
# Scene:      PlugObserverIntoPolynomial3Lighthouses
# Source:     videos/_2018/wallis.py (lines 2373-2376)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PlugObserverIntoPolynomial3Lighthouses.py PlugObserverIntoPolynomial3Lighthouses -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
#   - OldTex.add_background_rectangle() puts the rectangle at [0] and the parts directly after it (Cairo nested them in polynomial[1]); split the parts of the equation accordingly
#   - var_name = OldTex("O") is a single glyph in GL (no extra VGroup level), so var_name[1] is the glyph
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import AmbientLight
from once_useful_constructs.light import Lighthouse
from functools import reduce

PRODUCT_COLOR = BLUE


# CHANGE: inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
from once_useful_constructs.light import inverse_power_law
DEFAULT_OPACITY_FUNCTION = inverse_power_law(1, 1.5, 1, 4)


HIGHT_QUALITY_AMBIENT_LIGHT_CONFIG = {
    "opacity_function": DEFAULT_OPACITY_FUNCTION,
    "num_levels": 100,
    "radius": 5,
    "max_opacity": 0.8,
    "color": PRODUCT_COLOR,
}


class DistanceProductScene(MovingCameraScene):
    CONFIG = {
        "ambient_light_config": HIGHT_QUALITY_AMBIENT_LIGHT_CONFIG,
        "circle_color": BLUE,
        "circle_radius": 3,
        "num_lighthouses": 6,
        "lighthouse_height": 0.5,
        "ignored_lighthouse_indices": [],
        "observer_config": {
            "color": MAROON_B,
            "mode": "pondering",
            "height": 0.25,
            "flip_at_start": True,
        },
        "observer_fraction": 1.0 / 3,
        "d_label_height": 0.35,
        "numeric_distance_label_height": 0.25,
        "default_product_column_top": FRAME_WIDTH * RIGHT / 4 + 1.5 * UP,
        "include_lighthouses": True,
        "include_distance_labels_background_rectangle": True,
    }

    def setup(self):
        super(DistanceProductScene, self).setup()
        self.circle = Circle(
            color=self.circle_color,
            radius=self.circle_radius,
        )

    def get_circle_point_at_proportion(self, alpha):
        radius = self.get_radius()
        center = self.circle.get_center()
        angle = alpha * TAU
        unit_circle_point = np.cos(angle) * RIGHT + np.sin(angle) * UP
        return radius * unit_circle_point + center

    def get_lh_points(self):
        return np.array([
            self.get_circle_point_at_proportion(fdiv(i, self.num_lighthouses))
            for i in range(self.num_lighthouses)
            if i not in self.ignored_lighthouse_indices
        ])

    def get_observer_point(self, fraction=None):
        if fraction is None:
            fraction = self.observer_fraction
        return self.get_circle_point_at_proportion(fraction / self.num_lighthouses)

    def get_observer(self):
        observer = self.observer = PiCreature(**self.observer_config)
        observer.next_to(self.get_observer_point(), RIGHT, buff=SMALL_BUFF)
        return observer

    def get_observer_dot(self):
        self.observer_dot = Dot(
            self.get_observer_point(),
            color=self.observer_config["color"]
        )
        return self.observer_dot

    def get_lighthouses(self):
        self.lighthouses = VGroup()
        for point in self.get_lh_points():
            lighthouse = Lighthouse()
            lighthouse.set_height(self.lighthouse_height)
            lighthouse.move_to(point)
            self.lighthouses.add(lighthouse)
        return self.lighthouses

    def get_lights(self):
        self.lights = VGroup()
        for point in self.get_lh_points():
            light = AmbientLight(
                source_point=VectorizedPoint(point),
                **self.ambient_light_config
            )
            self.lights.add(light)
        return self.lights

    def get_distance_lines(self, start_point=None, line_class=Line):
        if start_point is None:
            start_point = self.get_observer_point()
        lines = VGroup(*[
            line_class(start_point, point)
            for point in self.get_lh_points()
        ])
        lines.set_stroke(width=2)
        self.distance_lines = lines
        return self.distance_lines

    def get_symbolic_distance_labels(self):
        if not hasattr(self, "distance_lines"):
            self.get_distance_lines()
        self.d_labels = VGroup()
        for i, line in enumerate(self.distance_lines):
            d_label = OldTex("d_%d" % i)
            d_label.set_height(self.d_label_height)
            vect = rotate_vector(line.get_vector(), 90 * DEGREES)
            vect *= 2.5 * SMALL_BUFF / get_norm(vect)
            d_label.move_to(line.get_center() + vect)
            self.d_labels.add(d_label)
        return self.d_labels

    def get_numeric_distance_labels(self, lines=None, num_decimal_places=3, show_ellipsis=True):
        radius = self.circle.get_width() / 2
        if lines is None:
            if not hasattr(self, "distance_lines"):
                self.get_distance_lines()
            lines = self.distance_lines
        labels = self.numeric_distance_labels = VGroup()
        for line in lines:
            label = DecimalNumber(
                line.get_length() / radius,
                num_decimal_places=num_decimal_places,
                show_ellipsis=show_ellipsis,
                include_background_rectangle=self.include_distance_labels_background_rectangle,
            )
            label.set_height(self.numeric_distance_label_height)
            max_width = 0.5 * max(line.get_length(), 0.1)
            if label.get_width() > max_width:
                label.set_width(max_width)
            angle = (line.get_angle() % TAU) - TAU / 2
            if np.abs(angle) > TAU / 4:
                angle += np.sign(angle) * np.pi
            label.angle = angle
            label.next_to(line.get_center(), UP, SMALL_BUFF)
            label.rotate(angle, about_point=line.get_center())
            labels.add(label)
        return labels

    def get_distance_product_column(self, column_top=None, labels=None, fraction=None):
        if column_top is None:
            column_top = self.default_product_column_top
        if labels is None:
            if not hasattr(self, "numeric_distance_labels"):
                self.get_numeric_distance_labels()
            labels = self.numeric_distance_labels
        stacked_labels = labels.copy()
        for label in stacked_labels:
            label.rotate(-label.angle)
            label.set_height(self.numeric_distance_label_height)
        stacked_labels.arrange(DOWN)
        stacked_labels.move_to(column_top, UP)

        h_line = Line(LEFT, RIGHT)
        h_line.set_width(1.5 * stacked_labels.get_width())
        h_line.next_to(stacked_labels, DOWN, aligned_edge=RIGHT)
        times = OldTex("\\times")
        times.next_to(h_line, UP, SMALL_BUFF, aligned_edge=LEFT)

        product_decimal = DecimalNumber(
            self.get_distance_product(fraction),
            num_decimal_places=3,
            show_ellipsis=True,
            include_background_rectangle=self.include_distance_labels_background_rectangle,
        )
        product_decimal.set_height(self.numeric_distance_label_height)
        product_decimal.next_to(h_line, DOWN)
        product_decimal.align_to(stacked_labels, RIGHT)
        product_decimal[1].set_color(BLUE)
        self.distance_product_column = VGroup(
            stacked_labels, h_line, times, product_decimal
        )
        return self.distance_product_column

    def get_fractional_arc(self, fraction, start_fraction=0):
        arc = Arc(
            angle=fraction * TAU,
            start_angle=start_fraction * TAU,
            radius=self.get_radius(),
        )
        arc.shift(self.circle.get_center())
        return arc

    def get_halfway_indication_arcs(self):
        fraction = 0.5 / self.num_lighthouses
        arcs = VGroup(
            self.get_fractional_arc(fraction),
            self.get_fractional_arc(-fraction, start_fraction=2 * fraction),
        )
        arcs.set_stroke(YELLOW, 4)
        return arcs

    def get_circle_group(self):
        group = VGroup(self.circle)
        if not hasattr(self, "observer_dot"):
            self.get_observer_dot()
        if not hasattr(self, "observer"):
            self.get_observer()
        if not hasattr(self, "lighthouses"):
            self.get_lighthouses()
        if not hasattr(self, "lights"):
            self.get_lights()
        group.add(self.observer_dot, self.observer)
        if self.include_lighthouses:
            group.add(self.lighthouses)
        group.add(self.lights)
        return group

    def setup_lighthouses_and_observer(self):
        self.add(*self.get_circle_group())

    # Numerical results

    def get_radius(self):
        return self.circle.get_width() / 2.0

    def get_distance_product(self, fraction=None):
        radius = self.get_radius()
        observer_point = self.get_observer_point(fraction)
        distances = [
            get_norm(point - observer_point) / radius
            for point in self.get_lh_points()
        ]
        return reduce(op.mul, distances, 1.0)

    # Animating methods

    def add_numeric_distance_labels(self, show_line_creation=True):
        anims = []
        if not hasattr(self, "distance_lines"):
            self.get_distance_lines()
        if not hasattr(self, "numeric_distance_labels"):
            self.get_numeric_distance_labels()
        if show_line_creation:
            anims.append(LaggedStartMap(ShowCreation, self.distance_lines))
        anims.append(LaggedStartMap(FadeIn, self.numeric_distance_labels))

        self.play(*anims)

    def show_distance_product_in_column(self, **kwargs):
        group = self.get_distance_product_column(**kwargs)
        stacked_labels, h_line, times, product_decimal = group
        labels = self.numeric_distance_labels

        self.play(ReplacementTransform(labels.copy(), stacked_labels))
        self.play(
            ShowCreation(h_line),
            Write(times)
        )
        self.play(
            ReplacementTransform(
                stacked_labels.copy(),
                VGroup(product_decimal)
            )
        )


class PlugObserverIntoPolynomial(DistanceProductScene):
    CONFIG = {
        # "ambient_light_config": CHEAP_AMBIENT_LIGHT_CONFIG,
        "num_lighthouses": 7,
        # This makes it look slightly better, but renders much slower
        "add_lights_in_foreground": True,
    }

    def construct(self):
        self.add_plane()
        self.add_circle_group()
        self.label_roots()
        self.add_polynomial()
        self.point_out_rhs()
        self.introduce_observer()
        self.raise_observer_to_the_N()

    def add_plane(self):
        plane = self.plane = ComplexPlane(
            unit_size=2,
            y_radius=5,
        )
        plane.shift(DOWN)
        plane.add_coordinates()
        plane.coordinate_labels.submobjects.pop(-4)
        self.origin = plane.number_to_point(0)

        self.add(plane)

    def add_circle_group(self):
        self.circle.set_color(RED)
        self.circle.set_width(
            2 * get_norm(self.plane.number_to_point(1) - self.origin)
        )
        self.circle.move_to(self.origin)

        lights = self.lights = self.get_lights()
        dots = VGroup(*[
            Dot(point) for point in self.get_lh_points()
        ])
        for dot, light in zip(dots, lights):
            light.add_to_back(dot)

        self.add(self.circle, lights)
        if self.add_lights_in_foreground:
            self.add_foreground_mobject(lights)

    def label_roots(self):
        origin = self.origin
        labels = VGroup(*[
            OldTex("L_%d" % d)
            for d in range(self.num_lighthouses)
        ])
        self.root_labels = labels
        points = self.get_lh_points()
        for label, point in zip(labels, points):
            label.move_to(interpolate(origin, point, 1.2))
        labels[0].align_to(origin, UP)
        labels[0].shift(SMALL_BUFF * DOWN)
        self.add(labels)

    def add_polynomial(self, arg="x"):
        self.polynomial = self.get_polynomial_equation(arg)
        self.add(self.polynomial)

    def point_out_rhs(self):
        rhs = self.get_polynomial_rhs(self.polynomial)
        brace = Brace(rhs, DOWN, buff=SMALL_BUFF)
        brace_text = brace.get_text(
            "Useful for distance product", buff=SMALL_BUFF)
        brace_text.set_color(YELLOW)
        brace_text.add_background_rectangle()

        self.play(
            GrowFromCenter(brace),
            Write(brace_text)
        )
        self.wait()
        self.play(FadeOut(VGroup(brace, brace_text)))

    def introduce_observer(self):
        dot = self.observer_dot = Dot()
        dot.move_to(self.plane.coords_to_point(1.6, 0.8))
        observer = PiCreature(**self.observer_config)
        observer.move_to(dot)
        dot.match_color(observer)

        vect = 2 * DOWN + LEFT
        vect /= get_norm(vect)
        arrow = self.arrow = Vector(0.5 * vect)
        arrow.next_to(observer, -vect, buff=SMALL_BUFF)
        arrow.set_color(WHITE)

        full_name = OldTexText("Observer")
        var_name = self.var_name = OldTex("O")
        for mob in full_name, var_name:
            mob.match_color(observer)
            mob.next_to(arrow.get_start(), UP, SMALL_BUFF)
            mob.add_background_rectangle()

        complex_decimal = DecimalNumber(0, include_background_rectangle=True)
        equals = OldTex("=")
        complex_decimal_animation = ChangingDecimal(
            complex_decimal,
            lambda a: self.plane.point_to_number(dot.get_center()),
            position_update_func=lambda m: m.next_to(equals, RIGHT, SMALL_BUFF)
        )
        complex_decimal_animation.update(0)
        equals_decimal = VGroup(equals, complex_decimal)
        equals_decimal.next_to(var_name, RIGHT)

        new_polynomial = self.get_polynomial_equation("O")
        O_terms = new_polynomial.get_parts_by_tex("O")

        lhs, poly_eq, rhs = self.get_polynomial_split(new_polynomial)
        lhs_rect = SurroundingRectangle(lhs, color=YELLOW)
        rhs_rect = SurroundingRectangle(rhs, color=YELLOW)
        self.lhs, self.rhs = lhs, rhs
        self.lhs_rect, self.rhs_rect = lhs_rect, rhs_rect

        lines = self.lines = self.get_lines()
        lines_update = self.lines_update = UpdateFromFunc(
            lines, lambda l: Transform(l, self.get_lines()).update(1)
        )

        anims_for_dot_movement = self.anims_for_dot_movement = [
            MaintainPositionRelativeTo(arrow, dot),
            MaintainPositionRelativeTo(var_name, arrow),
            MaintainPositionRelativeTo(equals, var_name),
            complex_decimal_animation,
            lines_update,
        ]

        self.play(
            FadeIn(observer, direction=-vect),
            GrowArrow(arrow)
        )
        self.play(Write(full_name))
        self.wait()
        self.play(
            ReplacementTransform(full_name[0], var_name[0]),
            # CHANGE: var_name = OldTex("O") is a single glyph in GL (no extra VGroup level), so var_name[1] is the glyph
            ReplacementTransform(full_name[1][0], var_name[1]),
            FadeOut(full_name[1][1:]),
            ReplacementTransform(observer, dot),
            FadeIn(equals_decimal)
        )
        self.add_foreground_mobject(dot)

        # Substitute
        self.wait()
        self.play(
            ReplacementTransform(var_name.copy(), O_terms),
            ReplacementTransform(self.polynomial, new_polynomial)
        )
        self.polynomial = new_polynomial
        self.wait()

        # Show distances
        self.play(ShowCreation(rhs_rect))
        self.play(
            LaggedStartMap(ShowCreation, lines),
            Animation(dot)
        )

        self.play(
            Rotating(
                dot,
                radians=TAU,
                rate_func=smooth,
                about_point=dot.get_center() + MED_LARGE_BUFF * LEFT,
                run_time=4
            ),
            *anims_for_dot_movement
        )
        self.wait()

        self.remove(rhs_rect)
        self.play(ReplacementTransform(rhs_rect.copy(), lhs_rect))
        self.wait()

        # Move onto circle
        angle = self.observer_angle = TAU / self.num_lighthouses / 3.0
        target_point = self.plane.number_to_point(
            np.exp(complex(0, angle))
        )
        self.play(
            dot.move_to, target_point,
            *anims_for_dot_movement
        )
        self.play(FadeOut(VGroup(
            equals, complex_decimal,
            var_name, arrow,
        )))

    def raise_observer_to_the_N(self):
        dot = self.observer_dot
        origin = self.origin
        radius = self.get_radius()

        text_scale_val = 0.8

        question = OldTexText(
            "What fraction \\\\", "between $L_0$ and $L_1$", "?",
            arg_separator=""
        )
        question.scale(text_scale_val)
        question.next_to(dot, RIGHT)
        question.add_background_rectangle_to_submobjects()

        f_words = OldTexText("$f$", "of the way")
        third_words = OldTexText("$\\frac{1}{3}$", "of the way")
        for words in f_words, third_words:
            words.scale(text_scale_val)
            words.move_to(question[0])
            words[0].set_color(YELLOW)
            words.add_background_rectangle()

        obs_angle = self.observer_angle
        full_angle = TAU / self.num_lighthouses

        def get_arc(angle):
            result = Arc(angle=angle, radius=radius,
                         color=YELLOW, stroke_width=4)
            result.shift(origin)
            return result

        arc = get_arc(obs_angle)
        O_to_N_arc = get_arc(obs_angle * self.num_lighthouses)

        O_to_N_dot = dot.copy().move_to(O_to_N_arc.point_from_proportion(1))
        O_to_N_arrow = Vector(0.5 * DR).next_to(O_to_N_dot, UL, SMALL_BUFF)
        O_to_N_arrow.set_color(WHITE)
        O_to_N_label = OldTex("O", "^N")
        O_to_N_label.set_color_by_tex("O", dot.get_color())
        O_to_N_label.next_to(O_to_N_arrow.get_start(), UP, SMALL_BUFF)
        O_to_N_label.shift(SMALL_BUFF * RIGHT)
        O_to_N_group = VGroup(O_to_N_arc, O_to_N_arrow, O_to_N_label)

        around_circle_words = OldTexText("around the circle")
        around_circle_words.scale(text_scale_val)
        around_circle_words.add_background_rectangle()
        around_circle_words.next_to(self.circle.get_top(), UR)

        chord = Line(O_to_N_dot.get_center(), self.circle.get_right())
        chord.set_stroke(GREEN)

        chord_halves = VGroup(
            Line(chord.get_center(), chord.get_start()),
            Line(chord.get_center(), chord.get_end()),
        )
        chord_halves.set_stroke(WHITE, 5)

        chord_label = OldTex("|", "O", "^N", "-", "1", "|")
        chord_label.set_color_by_tex("O", MAROON_B)
        chord_label.add_background_rectangle()
        chord_label.next_to(chord.get_center(), DOWN, SMALL_BUFF)
        chord_label.rotate(
            chord.get_angle(), about_point=chord.get_center()
        )

        numeric_chord_label = DecimalNumber(
            np.sqrt(3),
            num_decimal_places=4,
            include_background_rectangle=True,
            show_ellipsis=True,
        )
        numeric_chord_label.rotate(chord.get_angle())
        numeric_chord_label.move_to(chord_label)

        self.play(
            FadeIn(question),
            ShowCreation(arc),
        )
        for angle in [full_angle - obs_angle, -full_angle, obs_angle]:
            last_angle = angle_of_vector(dot.get_center() - origin)
            self.play(
                self.lines_update,
                UpdateFromAlphaFunc(
                    arc, lambda arc, a: Transform(
                        arc, get_arc(last_angle + a * angle)
                    ).update(1)
                ),
                Rotate(dot, angle, about_point=origin),
                run_time=2
            )
        self.play(
            FadeOut(question[0]),
            FadeOut(question[2]),
            FadeIn(f_words),
        )
        self.wait()
        self.play(
            FadeOut(self.lines),
            FadeOut(self.root_labels),
        )
        self.play(
            ReplacementTransform(dot.copy(), O_to_N_dot),
            ReplacementTransform(arc, O_to_N_arc),
            path_arc=O_to_N_arc.angle - arc.angle,
        )
        self.add_foreground_mobject(O_to_N_dot)
        self.play(
            FadeIn(O_to_N_label),
            GrowArrow(O_to_N_arrow),
        )
        self.wait()
        self.play(
            FadeOut(question[1]),
            f_words.next_to, around_circle_words, UP, SMALL_BUFF,
            FadeIn(around_circle_words)
        )
        self.wait()
        self.play(
            FadeIn(chord_label[0]),
            ReplacementTransform(self.lhs.copy(), chord_label[1]),
            ShowCreation(chord)
        )
        self.wait()

        # Talk through current example
        light_rings = VGroup(*it.chain(self.lights))
        self.play(LaggedStartMap(
            ApplyMethod, light_rings,
            lambda m: (m.shift, MED_SMALL_BUFF * UP),
            rate_func=wiggle
        ))
        self.play(
            FadeOut(around_circle_words),
            FadeIn(question[1]),
            ReplacementTransform(f_words, third_words)
        )
        self.play(
            Rotate(dot, 0.05 * TAU, about_point=origin, rate_func=wiggle)
        )
        self.wait(2)
        self.play(ReplacementTransform(
            dot.copy(), O_to_N_dot, path_arc=TAU / 3))
        self.play(
            third_words.next_to, around_circle_words, UP, SMALL_BUFF,
            FadeIn(around_circle_words),
            FadeOut(question[1])
        )
        self.wait()
        self.play(Indicate(self.lhs))
        for x in range(2):
            self.play(ShowCreationThenDestruction(chord_halves))
        self.play(
            FadeOut(chord_label),
            FadeIn(numeric_chord_label)
        )
        self.wait()
        self.remove(self.lhs_rect)
        self.play(
            FadeOut(chord),
            FadeOut(numeric_chord_label),
            FadeOut(O_to_N_group),
            FadeIn(self.lines),
            ReplacementTransform(self.lhs_rect.copy(), self.rhs_rect)
        )
        self.wait()

        # Add new lights
        for light in self.lights:
            light[1:].fade(0.5)
        added_lights = self.lights.copy()
        added_lights.rotate(full_angle / 2, about_point=origin)
        new_lights = VGroup(*it.chain(*list(zip(self.lights, added_lights))))
        self.num_lighthouses *= 2
        dot.generate_target()
        dot.target.move_to(self.get_circle_point_at_proportion(
            obs_angle / TAU / 2
        ))
        dot.save_state()
        dot.move_to(dot.target)
        new_lines = self.get_lines()
        dot.restore()

        self.play(Transform(self.lights, new_lights))
        self.play(
            MoveToTarget(dot),
            Transform(self.lines, new_lines)
        )
        self.wait()
        self.play(
            third_words.next_to, question[1], UP, SMALL_BUFF,
            FadeOut(around_circle_words),
            FadeIn(question[1]),
        )
        self.wait()

        chord_group = VGroup(chord, numeric_chord_label[1])
        chord_group.set_color(YELLOW)
        self.add_foreground_mobjects(*chord_group)
        self.play(
            FadeIn(chord),
            FadeIn(numeric_chord_label),
        )
        self.wait()

    # Helpers

    def get_polynomial_equation(self, var="x", color=None):
        if color is None:
            color = self.observer_config["color"]
        equation = OldTex(
            "\\left(", var, "^N", "-", "1", "\\right)", "=",
            "\\left(", var, "-", "L_0", "\\right)",
            "\\left(", var, "-", "L_1", "\\right)",
            "\\cdots",
            "\\left(", var, "-", "L_{N-1}", "\\right)",
        )
        equation.set_color_by_tex(var, color)
        equation.to_edge(UP)
        equation.add_background_rectangle()
        return equation

    def get_polynomial_rhs(self, polynomial):
        return self.get_polynomial_split(polynomial)[2]

    def get_polynomial_lhs(self, polynomial):
        return self.get_polynomial_split(polynomial)[0]

    def get_polynomial_split(self, polynomial):
        eq = polynomial.get_part_by_tex("=")
        # CHANGE: OldTex.add_background_rectangle() puts the rectangle at [0] and the parts directly after it (Cairo nested them in polynomial[1]); split the parts of the equation accordingly
        # in GL the tex parts are direct submobjects (after the background rectangle at index 0)
        i = polynomial.submobjects.index(eq)
        return VGroup(*polynomial[1:i]), polynomial[i], VGroup(*polynomial[i + 1:])

    def get_lines(self, start_point=None):
        return self.get_distance_lines(
            start_point=start_point,
            line_class=DashedLine
        )

    def get_observer_point(self, dummy_arg=None):
        return self.observer_dot.get_center()


class PlugObserverIntoPolynomial3Lighthouses(PlugObserverIntoPolynomial):
    CONFIG = {
        "num_lighthouses": 3,
    }
