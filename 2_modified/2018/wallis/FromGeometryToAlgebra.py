# ==============================================================================
# Scene:      FromGeometryToAlgebra
# Source:     videos/_2018/wallis.py (lines 1508-1927)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FromGeometryToAlgebra.py FromGeometryToAlgebra -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
#   - OldTex parts are one nesting level flatter in GL: [background rect, glyphs...] instead of [rect, VGroup(glyphs)]
# ==============================================================================

from manim_imports_ext import *
from once_useful_constructs.light import AmbientLight
from once_useful_constructs.light import Lighthouse
from once_useful_constructs.light import SwitchOn
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


class FromGeometryToAlgebra(DistanceProductScene):
    CONFIG = {
        "num_lighthouses": 7,
        # "ambient_light_config": CHEAP_AMBIENT_LIGHT_CONFIG,
    }

    def construct(self):
        self.setup_lights()
        self.point_out_evenly_spaced()
        self.transition_to_complex_plane()
        self.discuss_powers()
        self.raise_everything_to_the_nth()

    def setup_lights(self):
        circle = self.circle
        circle.set_height(5, about_edge=DOWN)
        lights = self.get_lights()
        dots = VGroup(*[Dot(point) for point in self.get_lh_points()])
        for dot, light in zip(dots, lights):
            light.add_to_back(dot)

        self.add(circle, lights)

    def point_out_evenly_spaced(self):
        circle = self.circle
        step = 1.0 / self.num_lighthouses / 2
        alpha_range = np.arange(0, 1 + step, step)
        arcs = VGroup(*[
            VMobject().pointwise_become_partial(circle, a1, a2)
            for a1, a2 in zip(alpha_range, alpha_range[1:])
        ])
        arcs.set_stroke(YELLOW, 5)

        for arc in arcs[::2]:
            arc.reverse_points()

        arcs_anim = ShowCreationThenDestruction(
            arcs, lag_ratio=0, run_time=2
        )

        spacing_words = self.spacing_words = OldTexText("Evenly-spaced")
        spacing_words.set_width(self.get_radius())
        spacing_words.move_to(circle)

        arrows = self.get_arrows()

        geometric_words = self.geometric_words = OldTexText(
            "Geometric property")
        geometric_words.to_edge(UP)
        geometric_words.add_background_rectangle()

        self.add(geometric_words)
        self.play(
            FadeIn(spacing_words),
            arcs_anim,
            *list(map(GrowArrow, arrows))
        )
        self.play(FadeOut(arrows), arcs_anim)
        self.wait()

    def transition_to_complex_plane(self):
        plane = self.complex_plane = ComplexPlane(
            unit_size=2, y_radius=6, x_radius=9,
        )
        plane.shift(1.5 * RIGHT)
        plane.add_coordinates()
        origin = plane.number_to_point(0)
        h_line = Line(plane.number_to_point(-1), plane.number_to_point(1))

        circle = self.circle
        circle_group = VGroup(circle, self.lights)
        circle_group.generate_target()
        circle_group.target.scale(h_line.get_width() / circle.get_width())
        circle_group.target.shift(
            origin - circle_group.target[0].get_center()
        )
        circle_group.target[0].set_stroke(RED)

        geometric_words = self.geometric_words
        geometric_words.generate_target()
        arrow = OldTex("\\rightarrow")
        arrow.add_background_rectangle()
        algebraic_words = OldTexText("Algebraic property")
        algebraic_words.add_background_rectangle()
        word_group = VGroup(geometric_words.target, arrow, algebraic_words)
        word_group.arrange(RIGHT)
        word_group.move_to(origin)
        word_group.to_edge(UP)

        unit_circle_words = OldTexText("Unit circle", "")
        unit_circle_words.match_color(circle_group.target[0])
        for part in unit_circle_words:
            part.add_background_rectangle()
        unit_circle_words.next_to(origin, UP)

        complex_plane_words = OldTexText("Complex Plane")
        self.complex_plane_words = complex_plane_words
        complex_plane_words.move_to(word_group)
        complex_plane_words.add_background_rectangle()

        roots_of_unity_words = OldTexText("Roots of\\\\", "unity")
        roots_of_unity_words.move_to(origin)
        roots_of_unity_words.set_color(YELLOW)
        for part in roots_of_unity_words:
            part.add_background_rectangle()

        self.play(
            Write(plane),
            MoveToTarget(circle_group),
            FadeOut(self.spacing_words),
            MoveToTarget(geometric_words),
            FadeIn(arrow),
            FadeIn(algebraic_words),
        )
        word_group.submobjects[0] = geometric_words
        self.play(Write(unit_circle_words, run_time=1))

        # Show complex values
        outer_arrows = self.outer_arrows = self.get_arrows()
        for arrow, point in zip(outer_arrows, self.get_lh_points()):
            arrow.rotate(np.pi, about_point=point)
        outer_arrow = self.outer_arrow = outer_arrows[3].copy()

        values = list(map(plane.point_to_number, self.get_lh_points()))
        complex_decimal = self.complex_decimal = DecimalNumber(
            values[3],
            num_decimal_places=3,
            include_background_rectangle=True
        )
        complex_decimal.next_to(outer_arrow.get_start(), LEFT, SMALL_BUFF)
        complex_decimal_rect = SurroundingRectangle(complex_decimal)
        complex_decimal_rect.fade(1)

        self.play(
            FadeIn(complex_plane_words),
            FadeOut(word_group),
            FadeIn(complex_decimal),
            FadeIn(outer_arrow)
        )
        self.wait(2)
        self.play(
            ChangeDecimalToValue(
                complex_decimal, values[1],
                tracked_mobject=complex_decimal_rect
            ),
            complex_decimal_rect.next_to, outer_arrows[1].get_start(
            ), UP, SMALL_BUFF,
            Transform(outer_arrow, outer_arrows[1]),
            run_time=1.5
        )
        self.wait()

        arrows = self.get_arrows()
        arrows.set_color(YELLOW)
        self.play(
            ReplacementTransform(unit_circle_words, roots_of_unity_words),
            LaggedStartMap(GrowArrow, arrows)
        )
        self.wait()
        self.play(
            complex_plane_words.move_to, word_group,
            LaggedStartMap(FadeOut, VGroup(*it.chain(
                arrows, roots_of_unity_words
            )))
        )

        # Turn decimal into z
        x_term = self.x_term = OldTex("x")
        x_term.add_background_rectangle()
        x_term.move_to(complex_decimal, DOWN)
        x_term.shift(0.5 * SMALL_BUFF * (DR))
        self.play(ReplacementTransform(complex_decimal, x_term))

    def discuss_powers(self):
        x_term = self.x_term
        outer_arrows = self.outer_arrows
        outer_arrows.add(outer_arrows[0].copy())
        plane = self.complex_plane
        origin = plane.number_to_point(0)

        question = OldTexText("What is $x^2$")
        question.next_to(x_term, RIGHT, LARGE_BUFF)
        question.set_color(YELLOW)

        lh_points = list(self.get_lh_points())
        lh_points.append(lh_points[0])
        lines = VGroup(*[
            Line(origin, point)
            for point in lh_points
        ])
        lines.set_color(GREEN)
        step = 1.0 / self.num_lighthouses
        angle_arcs = VGroup(*[
            Arc(angle=alpha * TAU, radius=0.35).shift(origin)
            for alpha in np.arange(0, 1 + step, step)
        ])
        angle_labels = VGroup()
        for i, arc in enumerate(angle_arcs):
            label = OldTex("(%d / %d)\\tau" % (i, self.num_lighthouses))
            label.scale(0.5)
            label.add_background_rectangle()
            point = arc.point_from_proportion(0.5)
            point += 1.2 * (point - origin)
            label.move_to(point)
            angle_labels.add(label)
            if i == 0:
                label.shift(0.75 * label.get_height() * DOWN)

        line = self.angle_line = lines[1].copy()
        line_ghost = DashedLine(line.get_start(), line.get_end())
        self.ghost_angle_line = line_ghost
        line_ghost.set_stroke(line.get_color(), 2)
        angle_arc = angle_arcs[1].copy()
        angle_label = angle_labels[1].copy()
        angle_label.shift(0.25 * SMALL_BUFF * DR)

        magnitude_label = OldTex("1")
        magnitude_label.next_to(line.get_center(), UL, buff=SMALL_BUFF)

        power_labels = VGroup()
        for i, arrow in enumerate(outer_arrows[:-1]):
            label = OldTex("x^%d" % i)
            label.next_to(
                arrow.get_start(), -arrow.get_vector(),
                submobject_to_align=label[0]
            )
            label.add_background_rectangle()
            power_labels.add(label)
        power_labels[0].next_to(outer_arrows[-1].get_start(), UR, SMALL_BUFF)
        power_labels.submobjects[1] = x_term

        L_labels = self.L_labels = VGroup(*[
            OldTex("L_%d" % i).move_to(power_label, DOWN).add_background_rectangle(
                opacity=1
            )
            for i, power_label in enumerate(power_labels)
        ])

        # Ask about squaring
        self.play(Write(question))
        self.wait()
        self.play(
            ShowCreation(line),
            Write(magnitude_label)
        )
        self.wait()
        self.play(
            ShowCreation(angle_arc),
            Write(angle_label)
        )
        self.wait()
        self.add(line_ghost)
        for i in list(range(2, self.num_lighthouses)) + [0]:
            anims = [
                Transform(angle_arc, angle_arcs[i]),
                Transform(angle_label, angle_labels[i]),
                Transform(line, lines[i], path_arc=TAU / self.num_lighthouses),
            ]
            if i == 2:
                anims.append(FadeOut(magnitude_label))
            if i == 3:
                anims.append(FadeOut(question))
            self.play(*anims)
            new_anims = [
                GrowArrow(outer_arrows[i]),
                Write(power_labels[i]),
            ]
            if i == 2:
                new_anims.append(FadeOut(self.complex_plane_words))
            self.play(*new_anims)
            self.wait()
        self.play(ReplacementTransform(power_labels, L_labels))
        self.wait()
        self.play(
            Rotate(self.lights, TAU / self.num_lighthouses / 2),
            rate_func=wiggle
        )
        self.wait()
        self.play(
            FadeOut(angle_arc),
            FadeOut(angle_label),
            *list(map(ShowCreationThenDestruction, lines))
        )
        self.wait()

    def raise_everything_to_the_nth(self):
        func_label = OldTex("L \\rightarrow L^7")
        func_label.set_color(YELLOW)
        func_label.to_corner(UL, buff=LARGE_BUFF)
        func_label.add_background_rectangle()

        polynomial_scale_factor = 0.8

        polynomial = OldTex("x^%d - 1" % self.num_lighthouses, "=", "0")
        polynomial.scale(polynomial_scale_factor)
        polynomial.next_to(func_label, UP)
        polynomial.to_edge(LEFT)

        factored_polynomial = OldTex(
            "(x-L_0)(x-L_1)\\cdots(x-L_{%d - 1})" % self.num_lighthouses, "=", "0"
        )
        factored_polynomial.scale(polynomial_scale_factor)
        factored_polynomial.next_to(polynomial, DOWN, aligned_edge=LEFT)
        for group in polynomial, factored_polynomial:
            for part in group:
                part.add_background_rectangle()

        origin = self.complex_plane.number_to_point(0)

        lights = self.lights
        lights.save_state()
        rotations = []
        for i, light in enumerate(lights):
            rotations.append(Rotating(
                light,
                radians=(i * TAU - i * TAU / self.num_lighthouses),
                about_point=origin,
                rate_func=bezier([0, 0, 1, 1]),
            ))

        self.play(Write(func_label, run_time=1))
        for i, rotation in enumerate(rotations[:4]):
            if i == 3:
                rect = SurroundingRectangle(polynomial)
                rect.set_color(YELLOW)
                self.play(
                    FadeIn(polynomial),
                    ShowCreationThenDestruction(rect)
                )
            self.play(
                rotation,
                run_time=np.sqrt(i + 1)
            )
        self.play(*rotations[4:], run_time=3)
        self.wait()

        self.play(lights.restore)
        self.play(
            FadeOut(func_label),
            FadeIn(factored_polynomial)
        )
        self.wait(3)
        self.play(
            factored_polynomial[0].next_to, polynomial[1], RIGHT, 1.5 * SMALL_BUFF,
            FadeOut(polynomial[2]),
            FadeOut(factored_polynomial[1:]),
        )

        # Comment on formula
        formula = VGroup(polynomial[0], polynomial[1], factored_polynomial[0])
        rect = SurroundingRectangle(formula)

        brace = Brace(factored_polynomial[0], DOWN)
        brace2 = Brace(polynomial[0], DOWN)

        morty = PiCreature(color=GREY_BROWN)
        morty.scale(0.5)
        morty.next_to(brace.get_center(), DL, buff=LARGE_BUFF)

        L1_rhs = OldTex("= \\cos(\\tau / 7) + \\\\", "\\sin(\\tau / 7)i")
        L1_rhs.next_to(self.L_labels[1], RIGHT, aligned_edge=UP)
        for part in L1_rhs:
            part.add_background_rectangle()

        self.play(ShowCreation(rect))
        self.play(FadeOut(rect))
        self.wait()
        self.play(GrowFromCenter(brace))
        self.play(FadeIn(morty))
        self.play(morty.change, "horrified", brace)
        self.play(Blink(morty))
        self.wait()
        self.play(
            Write(L1_rhs),
            morty.change, "confused", L1_rhs
        )
        self.play(Blink(morty))
        self.wait()
        self.play(
            Transform(brace, brace2),
            morty.change, "hooray", brace2
        )
        self.play(Blink(morty))
        self.wait()

        # Nothing special about 7
        new_lights = self.lights.copy()
        new_lights.rotate(
            TAU / self.num_lighthouses / 2,
            about_point=origin
        )
        # CHANGE: OldTex parts are one nesting level flatter in GL: [background rect, glyphs...] instead of [rect, VGroup(glyphs)]
        sevens = VGroup(polynomial[0][2], factored_polynomial[0][-4])
        n_terms = VGroup()
        for seven in sevens:
            n_term = OldTex("N")
            n_term.replace(seven, dim_to_match=1)
            n_term.scale(0.9)
            n_term.shift(0.25 * SMALL_BUFF * DR)
            n_terms.add(n_term)

        self.play(LaggedStartMap(FadeOut, VGroup(*it.chain(
            L1_rhs, self.outer_arrows, self.L_labels, self.outer_arrow,
            self.angle_line, self.ghost_angle_line
        ))))
        self.play(LaggedStartMap(SwitchOn, new_lights), morty.look_at, new_lights)
        self.play(Transform(sevens, n_terms))
        self.wait()
        self.play(Blink(morty))
        self.wait()
    #

    def get_arrows(self):
        return VGroup(*[
            Arrow(
                interpolate(self.circle.get_center(), point, 0.6),
                interpolate(self.circle.get_center(), point, 0.9),
                buff=0
            )
            for point in self.get_lh_points()
        ])
