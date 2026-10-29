# ==============================================================================
# Scene:      ArmedWithTwoKeyFacts
# Source:     videos/_2018/wallis.py (lines 2979-3039)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ArmedWithTwoKeyFacts.py ArmedWithTwoKeyFacts -w -m --fps 15
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


class WallisNumeratorDenominatorGenerator(object):
    def __init__(self):
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        return next(self)

    def __next__(self):
        n = self.n
        self.n += 1
        if n % 2 == 0:
            return (n + 2, n + 1)
        else:
            return (n + 1, n + 2)


def get_wallis_product(n_terms=6, show_result=True):
    tex_mob_args = []
    nd_generator = WallisNumeratorDenominatorGenerator()
    for x in range(n_terms):
        numerator, denominator = next(nd_generator)
        tex_mob_args += [
            "{%d" % numerator, "\\over", "%d}" % denominator, "\\cdot"
        ]
    tex_mob_args[-1] = "\\cdots"
    if show_result:
        tex_mob_args += ["=", "{\\pi", "\\over", "2}"]

    result = OldTex(*tex_mob_args)
    return result


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


class ArmedWithTwoKeyFacts(TeacherStudentsScene, DistanceProductScene):
    CONFIG = {
        "num_lighthouses": 6,
        "ambient_light_config": {
            "opacity_function": inverse_power_law(1, 1, 1, 6),
            "radius": 1,
            "num_levels": 100,
            "max_opacity": 1,
        },
    }

    def setup(self):
        TeacherStudentsScene.setup(self)
        DistanceProductScene.setup(self)

    def construct(self):
        circle1 = self.circle
        circle1.set_height(1.5)
        circle1.to_corner(UL)
        circle2 = circle1.copy()
        circle2.next_to(circle1, DOWN, MED_LARGE_BUFF)

        wallis_product = get_wallis_product(n_terms=8)

        N = self.num_lighthouses
        labels = VGroup()
        for circle, f, dp in (circle1, 0.5, "2"), (circle2, 0, "N"):
            self.circle = circle
            lights = self.get_lights()
            if f == 0:
                lights.submobjects.pop(0)
            observer = Dot(color=MAROON_B)
            frac = f / N
            point = self.get_circle_point_at_proportion(frac)
            observer.move_to(point)
            lines = self.get_distance_lines(point, line_class=DashedLine)

            label = OldTexText("Distance product = %s" % dp)
            label.scale(0.7)
            label.next_to(circle, RIGHT)
            labels.add(label)

            group = VGroup(lines, observer, label)
            self.play(
                FadeIn(circle),
                LaggedStartMap(FadeIn, VGroup(*it.chain(lights))),
                LaggedStartMap(
                    FadeIn, VGroup(
                        *it.chain(group.family_members_with_points()))
                ),
                self.teacher.change, "raise_right_hand",
                self.change_students(*["pondering"] * 3)
            )
        wallis_product.move_to(labels).to_edge(RIGHT)
        self.play(
            LaggedStartMap(FadeIn, wallis_product),
            self.teacher.change_mode, "hooray",
            self.change_students(
                *["thinking"] * 3, look_at=wallis_product)
        )
        self.wait(2)
