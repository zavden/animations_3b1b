# ==============================================================================
# Scene:      Lemma1With9Lighthouses
# Source:     videos/_2018/wallis.py (lines 1426-1429)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Lemma1With9Lighthouses.py Lemma1With9Lighthouses -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
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


class Lemma1(DistanceProductScene):
    CONFIG = {
        "circle_radius": 2.5,
        "observer_fraction": 0.5,
        "lighthouse_height": 0.25,
        "lemma_text": "distance product = 2",
        "include_distance_labels_background_rectangle": False,
        # "ambient_light_config": CHEAP_AMBIENT_LIGHT_CONFIG,
    }

    def construct(self):
        self.add_title()
        self.add_circle_group()
        self.state_lemma_premise()
        self.show_product()
        self.wiggle_observer()

    def add_title(self):
        title = self.title = OldTexText("Two lemmas:")
        title.set_color(YELLOW)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add(title)

    def add_circle_group(self):
        self.circle.to_corner(DL)
        circle_group = self.get_circle_group()
        self.play(LaggedStartMap(FadeIn, VGroup(
            *circle_group.family_members_with_points())))

    def state_lemma_premise(self):
        premise = OldTexText(
            "Lemma 1: If observer is halfway between lighthouses,")
        self.premise = premise
        premise.next_to(self.title, DOWN)

        frac = 1.0 / self.num_lighthouses
        arc1, arc2 = arcs = VGroup(VMobject(), VMobject())
        arc1.pointwise_become_partial(self.circle, 0, frac / 2)
        arc2.pointwise_become_partial(self.circle, frac / 2, frac)
        arc1.reverse_points()
        arcs.set_stroke(YELLOW, 5)
        show_arcs = ShowCreationThenDestruction(
            arcs,
            lag_ratio=0,
            run_time=2,
        )

        self.play(Write(premise), show_arcs, run_time=2)
        self.wait()
        self.play(show_arcs)
        self.wait()

    def show_product(self):
        lemma = OldTexText(self.lemma_text)
        lemma.set_color(BLUE)
        lemma.next_to(self.premise, DOWN)
        self.add_numeric_distance_labels()
        self.play(Write(lemma, run_time=1))
        self.show_distance_product_in_column()
        self.wait()

    def wiggle_observer(self):
        # Overwriting existing method
        self.get_observer_point = lambda dummy=None: self.observer_dot.get_center()

        center = self.circle.get_center()
        observer_angle = angle_of_vector(self.get_observer_point() - center)
        observer_angle_tracker = ValueTracker(observer_angle)

        def update_dot(dot):
            dot.move_to(self.get_circle_point_at_proportion(
                observer_angle_tracker.get_value() / TAU
            ))

        def update_distance_lines(lines):
            new_lines = self.get_distance_lines(start_point=self.get_observer_point())
            lines.submobjects = new_lines.submobjects

        def update_numeric_distance_labels(labels):
            new_labels = self.get_numeric_distance_labels(self.distance_lines)
            labels.submobjects = new_labels.submobjects

        def update_distance_product_column(column):
            new_column = self.get_distance_product_column()
            column.submobjects = new_column.submobjects

        self.remove(*VGroup(
            self.observer, self.observer_dot,
            self.distance_lines,
            self.numeric_distance_labels,
            self.distance_product_column,
        ).get_family())
        self.play(
            ApplyMethod(
                observer_angle_tracker.set_value, observer_angle + 0.05 * TAU,
                rate_func=wiggle
            ),
            UpdateFromFunc(self.observer_dot, update_dot),
            MaintainPositionRelativeTo(self.observer, self.observer_dot),
            UpdateFromFunc(self.distance_lines, update_distance_lines),
            UpdateFromFunc(self.numeric_distance_labels, update_numeric_distance_labels),
            UpdateFromFunc(self.distance_product_column, update_distance_product_column),
            run_time=5
        )
        self.distance_product_column[-1].set_color(BLUE).scale(1.05)
        self.wait()


class Lemma1With9Lighthouses(Lemma1):
    CONFIG = {
        "num_lighthouses": 9,
    }
