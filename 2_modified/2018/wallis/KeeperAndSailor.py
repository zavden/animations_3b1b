# ==============================================================================
# Scene:      KeeperAndSailor
# Source:     videos/_2018/wallis.py (lines 3075-4040)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl KeeperAndSailor.py KeeperAndSailor -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - inverse_power_law was never imported in the original file (NameError there too); import it from once_useful_constructs.light
#   - Python 2 integer division: half_N is used as a list index/range bound, so it must be an int
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


class Sailor(PiCreature):
    CONFIG = {
        "flip_at_start": True,
        "color": YELLOW_D,
        "hat_height_factor": 1.0 / 6,
    }

    def __init__(self, *args, **kwargs):
        PiCreature.__init__(self, *args, **kwargs)
        height = self.get_height() * self.hat_height_factor
        sailor_hat = SVGMobject(file_name="sailor_hat", height=height)
        # Rhombus is a horrible hack...
        rhombus = Polygon(
            UP, UP + 2 * RIGHT,
            1.75 * RIGHT + 0.5 * UP, 0.5 * RIGHT + 0.1 * DOWN,
            1.25 * LEFT + 0.15 * DOWN,
        )
        rhombus.set_fill(BLACK, opacity=1)
        rhombus.set_stroke(width=0)
        rhombus.set_height(sailor_hat.get_height() / 3)
        rhombus.rotate(5 * DEGREES)
        rhombus.move_to(sailor_hat, DR)
        rhombus.shift(0.05 * sailor_hat.get_width() * LEFT)
        sailor_hat.add_to_back(rhombus)
        sailor_hat.rotate(-15 * DEGREES)
        sailor_hat.move_to(self.eyes.get_center(), DOWN)
        sailor_hat.shift(
            0.1 * self.eyes.get_width() * RIGHT,
            0.1 * self.eyes.get_height() * UP,
        )
        self.add(sailor_hat)


class KeeperAndSailor(DistanceProductScene, PiCreatureScene):
    CONFIG = {
        "num_lighthouses": 9,
        "circle_radius": 2.75,
        # "ambient_light_config": CHEAP_AMBIENT_LIGHT_CONFIG,
        "add_lights_in_foreground": False,  # Keep this way
        "text_scale_val": 0.7,
        "observer_fraction": 0.5,
        "keeper_color": BLUE,
        "sailor_color": YELLOW_D,
        "include_distance_labels_background_rectangle": False,
        "big_circle_center": FRAME_WIDTH * LEFT / 2 + SMALL_BUFF * RIGHT,
    }

    def setup(self):
        DistanceProductScene.setup(self)
        PiCreatureScene.setup(self)
        self.remove(*self.pi_creatures)

    def construct(self):
        self.place_lighthouses()
        self.introduce_observers()
        self.write_distance_product_fraction()
        self.break_down_distance_product_by_parts()
        self.grow_circle_and_N()
        self.show_limit_for_each_fraction()
        self.show_limit_of_lhs()

    def place_lighthouses(self):
        circle = self.circle
        circle.to_corner(DL)
        circle.shift(MED_SMALL_BUFF * UR)
        circle.set_color(RED)

        lighthouses = self.get_lighthouses()
        lights = self.get_lights()
        for light in lights:
            dot = Dot(radius=0.06).move_to(light)
            dot.match_color(light)
            light.add_to_back(dot)
        origin = circle.get_center()
        arrows = VGroup(*[
            Arrow(0.6 * (p - origin), 0.9 * (p - origin), buff=0).shift(origin)
            for p in self.get_lh_points()
        ])
        arrows.set_color(WHITE)

        words = OldTexText("N evenly-spaced \\\\ lighthouses")
        words.scale(0.8)
        words.move_to(origin)

        self.add(circle)
        if self.add_lights_in_foreground:
            self.add_foreground_mobject(lights)
        self.add_foreground_mobject(words)
        self.play(
            LaggedStartMap(FadeIn, VGroup(*it.chain(lights))),
            LaggedStartMap(FadeIn, lighthouses),
            LaggedStartMap(GrowArrow, arrows),
        )
        self.remove_foreground_mobjects(words)
        self.play(FadeOut(words), FadeOut(arrows))
        self.wait()

    def introduce_observers(self):
        keeper, sailor = observers = self.observers
        keeper.target_point = self.get_keeper_point()
        sailor.target_point = self.get_sailor_point()

        for pi, text in (keeper, "Keeper"), (sailor, "Sailor"):
            pi.title = OldTexText(text)
            pi.title.next_to(pi, DOWN)
            pi.dot = Dot()
            pi.dot.match_color(pi)
            pi.dot.next_to(pi, LEFT)
            pi.dot.set_fill(opacity=0)

        self.play(LaggedStartMap(
            Succession, observers,
            lambda m: (FadeIn, m, ApplyMethod, m.change, "wave_1")
        ))
        for pi in observers:
            self.play(
                FadeIn(pi.title),
                pi.change, "plain"
            )
        self.wait()
        if self.add_lights_in_foreground:
            self.add_foreground_mobjects(keeper, keeper.dot, keeper.title)
        for pi in observers:
            self.play(
                pi.set_height, 0.5,
                pi.next_to, pi.target_point, RIGHT, SMALL_BUFF,
                pi.dot.move_to, pi.target_point,
                pi.dot.set_fill, {"opacity": 1},
                pi.title.scale, self.text_scale_val,
                pi.title.next_to, pi.target_point, RIGHT, {"buff": 0.6},
            )
            if pi is sailor:
                arcs = self.get_halfway_indication_arcs()
                self.play(*list(map(ShowCreationThenDestruction, arcs)))
            self.wait()

    def write_distance_product_fraction(self):
        fraction = self.distance_product_fraction = OldTex(
            "{\\text{Keeper's distance product}", "\\over",
            "\\text{Sailor's distance product}}"
        )
        fraction.scale(self.text_scale_val)
        fraction.to_corner(UR)

        keeper_lines = self.get_distance_lines(
            self.get_keeper_point(),
            line_class=DashedLine
        )
        sailor_lines = self.get_distance_lines(
            self.get_sailor_point(),
            line_class=DashedLine
        )
        sailor_line_lengths = self.get_numeric_distance_labels(sailor_lines)
        keeper_line_lengths = self.get_numeric_distance_labels(keeper_lines)
        sailor_dp_column, keeper_dp_column = [
            self.get_distance_product_column(
                4 * RIGHT + 1.5 * UP, labels, frac
            )
            for labels, frac in [
                (sailor_line_lengths, 0.5),
                (keeper_line_lengths, 0),
            ]
        ]
        sailor_dp_decimal = sailor_dp_column[-1]
        sailor_dp_decimal_rect = SurroundingRectangle(sailor_dp_decimal)
        keeper_dp_decimal = keeper_dp_column[-1]
        keeper_dp_decimal_rect = SurroundingRectangle(keeper_dp_decimal)
        keeper_top_zero_rect = SurroundingRectangle(keeper_dp_column[0][0])

        # stacked_labels, h_line, times, product_decimal = column

        # Define result fraction
        equals = self.distance_product_equals = OldTex("=")
        result_fraction = self.result_fraction = OldTex(
            "{N", "{\\text{distance} \\choose \\text{between obs.}}", "\\over", "2}"
        )
        N, dist, frac_line, two = result_fraction
        result_fraction.to_corner(UR)
        equals.next_to(frac_line, LEFT)
        for part in result_fraction:
            part.save_state()
            part.generate_target()
        div = OldTex("/")
        first_denom = VGroup(two.target, div, dist)
        first_denom.arrange(RIGHT, buff=SMALL_BUFF)
        first_denom.move_to(two, UP)
        N.next_to(frac_line, UP, SMALL_BUFF)

        # Define terms to be removed
        first_light_group = VGroup(self.lights[0], self.lighthouses[0])
        keeper_top_zero_group = VGroup(
            keeper_dp_column[0][0], keeper_top_zero_rect)

        new_keeper_dp_decimal = DecimalNumber(
            self.num_lighthouses,
            num_decimal_places=3,
        )
        new_keeper_dp_decimal.replace(keeper_dp_decimal, dim_to_match=1)
        new_keeper_dp_decimal.set_color(YELLOW)

        self.play(*list(map(ShowCreation, keeper_lines)))
        self.play(ReplacementTransform(
            keeper_lines.copy(), VGroup(fraction[0])
        ))
        self.play(FadeOut(keeper_lines))
        self.play(*list(map(ShowCreation, sailor_lines)))
        self.play(
            ReplacementTransform(
                sailor_lines.copy(),
                VGroup(fraction[2])
            ),
            ShowCreation(fraction[1])
        )
        self.wait()
        self.play(LaggedStartMap(FadeIn, sailor_line_lengths))
        self.play(ReplacementTransform(
            sailor_line_lengths.copy(), sailor_dp_column[0]
        ))
        self.play(FadeIn(sailor_dp_column[1:]))
        self.play(ShowCreation(sailor_dp_decimal_rect))
        self.play(
            fraction.next_to, equals, LEFT,
            FadeIn(equals),
            ShowCreation(frac_line),
            ReplacementTransform(sailor_dp_decimal.copy(), two),
            FadeOut(sailor_dp_decimal_rect)
        )
        self.wait()

        # Note, sailor_lines and sailor_line_lengths get changed here
        self.remove(*list(sailor_lines) + list(sailor_line_lengths))
        self.play(
            FadeOut(sailor_dp_column),
            ReplacementTransform(sailor_lines.deepcopy(), keeper_lines),
            ReplacementTransform(
                sailor_line_lengths.deepcopy(), keeper_line_lengths),
        )
        self.play(ReplacementTransform(
            keeper_line_lengths.copy(), keeper_dp_column[0]
        ))
        self.play(FadeIn(keeper_dp_column[1:]))
        self.wait()
        self.play(
            ShowCreation(keeper_dp_decimal_rect),
            ShowCreation(keeper_top_zero_rect)
        )
        self.wait(2)

        # Remove first lighthouse
        self.play(
            first_light_group.shift, 0.6 * FRAME_WIDTH * RIGHT,
            keeper_top_zero_group.shift, 0.4 * FRAME_WIDTH * RIGHT,
            FadeOut(keeper_dp_decimal),
            FadeOut(keeper_dp_decimal_rect),
            path_arc=-30 * DEGREES,
            rate_func=running_start,
        )
        self.remove(first_light_group, keeper_top_zero_group)
        self.wait()
        self.play(ReplacementTransform(
            keeper_dp_column[0][1:].copy(),
            VGroup(new_keeper_dp_decimal),
        ))
        self.wait()
        self.play(ReplacementTransform(new_keeper_dp_decimal.copy(), N,))
        self.wait(2)

        sailor_lines[0].set_color(RED)
        sailor_line_lengths[0].set_color(RED)
        sailor_line_lengths[0].set_stroke(RED, 1)
        self.remove(*list(keeper_lines) + list(keeper_line_lengths))
        self.play(
            ReplacementTransform(keeper_lines.copy(), sailor_lines),
            ReplacementTransform(
                keeper_line_lengths.copy(), sailor_line_lengths),
            FadeOut(keeper_dp_column[:-1]),
            FadeOut(new_keeper_dp_decimal),
        )
        self.play(
            Rotate(sailor_line_lengths[0], 30 * DEGREES, rate_func=wiggle)
        )
        self.wait()
        self.play(
            ReplacementTransform(sailor_lines[0].copy(), dist),
            FadeIn(div),
            MoveToTarget(two),
        )
        self.wait()
        self.play(
            two.restore,
            FadeOut(div),
            dist.restore,
            N.restore,
        )
        self.play(
            FadeOut(sailor_lines),
            FadeOut(sailor_line_lengths),
        )
        self.wait()

    def break_down_distance_product_by_parts(self):
        result_fraction = self.result_fraction
        result_fraction_rect = SurroundingRectangle(result_fraction)

        product_parts = self.product_parts = OldTex(
            "{|L_1 - K|", "\\over", "|L_1 - S|}", "\\cdot",
            "{|L_2 - K|", "\\over", "|L_2 - S|}", "\\cdot",
            "{|L_3 - K|", "\\over", "|L_3 - S|}", "\\cdots",
        )
        product_parts.set_color_by_tex_to_color_map({
            "K": BLUE,
            "S": YELLOW,
        })
        product_parts.set_width(0.4 * FRAME_WIDTH)
        product_parts.next_to(result_fraction, DOWN, LARGE_BUFF, RIGHT)
        product_parts.shift(MED_SMALL_BUFF * RIGHT)

        sailor_lines = self.get_sailor_lines()
        sailor_lines.save_state()
        keeper_lines = self.get_keeper_lines()
        keeper_lines.save_state()

        sailor_length_braces = VGroup(VMobject())  # Add fluff first object
        keeper_length_braces = VGroup(VMobject())  # Add fluff first object
        triplets = [
            ("S", sailor_length_braces, DOWN),
            ("K", keeper_length_braces, UP),
        ]
        for char, brace_group, vect in triplets:
            for part in product_parts.get_parts_by_tex(char):
                brace = Brace(part, vect, buff=SMALL_BUFF)
                brace.match_color(part)
                brace_group.add(brace)

        # Animations
        self.replace_lighthouses_with_labels()
        self.play(
            LaggedStartMap(FadeIn, product_parts),
            LaggedStartMap(FadeIn, sailor_lines,
                        rate_func=there_and_back, remover=True),
            LaggedStartMap(FadeIn, keeper_lines,
                        rate_func=there_and_back, remover=True),
        )
        sailor_lines.restore()
        keeper_lines.restore()
        self.wait()

        keeper_line = self.keeper_line = keeper_lines[1].copy()
        sailor_line = self.sailor_line = sailor_lines[1].copy()
        keeper_brace = keeper_length_braces[1].copy()
        sailor_brace = sailor_length_braces[1].copy()
        self.play(
            ShowCreation(keeper_line),
            GrowFromCenter(keeper_brace),
        )
        self.wait()
        self.play(
            ShowCreation(sailor_line),
            GrowFromCenter(sailor_brace),
        )
        self.wait()
        for i in range(2, 4):
            self.play(
                Transform(keeper_line, keeper_lines[i]),
                Transform(keeper_brace, keeper_length_braces[i]),
            )
            self.play(
                Transform(sailor_line, sailor_lines[i]),
                Transform(sailor_brace, sailor_length_braces[i]),
            )
            self.wait()
        for i in range(4, self.num_lighthouses):
            anims = [
                Transform(keeper_line, keeper_lines[i]),
                Transform(sailor_line, sailor_lines[i]),
            ]
            if i == 4:
                anims += [
                    FadeOut(sailor_brace),
                    FadeOut(keeper_brace),
                ]
            self.play(*anims)
        self.play(FocusOn(result_fraction))
        self.play(ShowPassingFlash(result_fraction_rect))
        self.wait(3)

    def grow_circle_and_N(self, circle_scale_factor=2, N_multiple=3, added_anims=None):
        if added_anims is None:
            added_anims = []
        circle = self.circle
        lights = self.lights
        labels = self.lighthouse_labels
        keeper = self.keeper
        sailor = self.sailor
        # CHANGE: Python 2 integer division: half_N is used as a list index/range bound, so it must be an int
        half_N = self.num_lighthouses // 2

        anims = []

        circle.generate_target()
        for pi in keeper, sailor:
            for mob in pi, pi.dot, pi.title:
                mob.generate_target()

        circle.target.scale(circle_scale_factor)
        circle.target.move_to(self.big_circle_center)
        self.circle = circle.target
        anims.append(MoveToTarget(circle))

        self.num_lighthouses = int(N_multiple * self.num_lighthouses)
        new_lights = self.get_lights()
        for light in new_lights:
            light.scale(1.0 / circle_scale_factor)
        new_labels = self.get_light_labels()
        anims.append(ReplacementTransform(labels[1:], new_labels[1:]))

        if hasattr(self, "keeper_line"):
            keeper_line = self.keeper_line
            sailor_line = self.sailor_line
            self.keeper_lines = self.get_keeper_lines()
            self.sailor_lines = self.get_sailor_lines()
            anims += [
                Transform(keeper_line, self.keeper_lines[-1]),
                Transform(sailor_line, self.sailor_lines[-1]),
            ]

        for group in lights, labels, new_lights, new_labels:
            group[0].fade(1)

        for mob in lights, labels:
            for x in range(len(new_lights) - len(mob)):
                mob.submobjects.insert(
                    half_N + 1, VectorizedPoint(circle.get_left()))
        anims.append(ReplacementTransform(lights, new_lights))

        keeper.dot.target.move_to(self.get_keeper_point())
        sailor.dot.target.move_to(self.get_sailor_point())
        for pi in keeper, sailor:
            pi.target.scale(0)
            pi.target.move_to(pi.dot.target)
            pi.title.target.scale(0.85)
            pi.title.target.next_to(pi.dot.target, RIGHT, SMALL_BUFF)
        anims += [
            MoveToTarget(part)
            for pi in self.observers
            for part in [pi, pi.dot, pi.title]
        ]

        anims += added_anims

        self.circle = circle

        self.play(*anims, run_time=2)
        if self.add_lights_in_foreground:
            self.remove_foreground_mobjects(*self.lights)
            self.remove_foreground_mobjects(*self.lighthouse_labels)
            self.add_foreground_mobjects(new_lights, new_labels)
        self.wait()
        self.lights = new_lights
        self.lighthouse_labels = new_labels

    def show_limit_for_each_fraction(self):
        product_parts = self.product_parts
        keeper_line = self.keeper_line
        keeper_lines = self.keeper_lines
        sailor_line = self.sailor_line
        sailor_lines = self.sailor_lines
        labels = self.lighthouse_labels

        center = self.circle.get_center()
        center_dot = Dot(center)
        lh_points = self.get_lh_points()
        sailor_point = self.get_sailor_point()
        keeper_point = self.get_keeper_point()

        def get_angle_mob(p1, p2):
            angle1 = angle_of_vector(p1 - center)
            angle2 = angle_of_vector(p2 - center)
            arc = Arc(start_angle=angle1, angle=(angle2 - angle1), radius=1)
            arc.shift(center)
            return VGroup(
                center_dot,
                Line(center, p1),
                Line(center, p2),
                arc,
            )

        angle_mob = get_angle_mob(lh_points[1], keeper_point)

        ratios = VGroup(*[
            product_parts[i:i + 3]
            for i in [0, 4, 8]
        ])
        term_rects = self.get_term_rects(ratios)

        limit_fractions = VGroup(
            OldTex("{2", "\\over", "1}"),
            OldTex("{4", "\\over", "3}"),
            OldTex("{6", "\\over", "5}"),
        )
        limit_arrows = VGroup()
        for rect, fraction in zip(term_rects, limit_fractions):
            fraction.next_to(rect, DOWN, LARGE_BUFF)
            arrow = Arrow(rect, fraction, color=WHITE)
            limit_arrows.add(arrow)

        approx = OldTex("\\approx")
        approx.scale(1.5)
        approx.rotate(90 * DEGREES)
        approx.move_to(limit_arrows[0])

        braces = self.get_all_circle_braces()

        # Show first lighthouse
        term_rect = term_rects[0].copy()
        self.play(
            Transform(keeper_line, keeper_lines[1]),
            Transform(sailor_line, sailor_lines[1]),
            FadeIn(term_rect),
            path_arc=-180 * DEGREES
        )
        self.wait(2)
        self.play(
            FadeOut(VGroup(keeper_line, sailor_line)),
            FadeIn(braces[:2]),
            FadeIn(angle_mob)
        )
        self.wait()
        self.play(Transform(angle_mob, get_angle_mob(
            lh_points[1], sailor_point)))
        self.wait(2)
        self.play(
            Write(approx),
            ReplacementTransform(ratios[0].copy(), limit_fractions[0]),
            FadeOut(angle_mob)
        )
        self.wait()
        self.play(ReplacementTransform(approx, limit_arrows[0]))
        self.let_N_approach_infinity(braces[:2])

        # Show second lighthouse
        self.play(
            Transform(term_rect, term_rects[1]),
            ReplacementTransform(limit_arrows[0].copy(), limit_arrows[1]),
            FadeIn(braces[2:4])
        )
        for group, color in (braces[:4], self.keeper_color), (braces[1:4], self.sailor_color):
            self.play(
                group.scale, 0.95, {"about_point": center},
                group.set_color, color,
                rate_func=there_and_back
            )
            self.wait(0.5)
        self.play(
            ReplacementTransform(ratios[1].copy(), limit_fractions[1])
        )
        self.wait()

        # Show third lighthouse
        braces[4:6].set_color(YELLOW)
        self.play(
            Transform(term_rect, term_rects[2]),
            ReplacementTransform(limit_arrows[1].copy(), limit_arrows[2]),
            FadeIn(braces[4:6]),
            braces[1:4].set_color, YELLOW,
            ReplacementTransform(limit_fractions[1].copy(), limit_fractions[2])
        )
        self.let_N_approach_infinity(braces[:6])
        self.wait()

        # Set up for lighthouse "before" keeper
        ccw_product_group = VGroup(
            product_parts, limit_arrows, limit_fractions)
        cw_product_parts = OldTex(
            "\\cdots", "{|L_{-3} - K|", "\\over", "|L_{-3} - S|}",
            "\\cdot", "{|L_{-2} - K|", "\\over", "|L_{-2} - S|}",
            "\\cdot", "{|L_{-1} - K|", "\\over", "|L_{-1} - S|}",
        )
        cw_product_parts.match_height(product_parts)
        cw_product_parts.set_color_by_tex_to_color_map({
            "K": BLUE,
            "S": YELLOW,
        })
        cw_product_parts.move_to(ratios, RIGHT)
        cw_ratios = VGroup(*[cw_product_parts[i:i + 3] for i in (9, 5, 1)])
        cw_term_rects = self.get_term_rects(cw_ratios)
        cw_limit_fractions = VGroup(
            OldTex("{2", "\\over", "3}"),
            OldTex("{4", "\\over", "5}"),
            OldTex("{6", "\\over", "7}"),
        )
        cw_limit_arrows = VGroup()
        for rect, fraction in zip(cw_term_rects, cw_limit_fractions):
            fraction.next_to(rect, DOWN, LARGE_BUFF)
            arrow = Arrow(rect, fraction, color=WHITE)
            cw_limit_arrows.add(arrow)

        cw_product_parts.save_state()
        cw_product_parts.next_to(product_parts, RIGHT, LARGE_BUFF)

        cw_label_rects = self.get_term_rects(labels[-1:-5:-1])
        cw_label_rects.set_color(RED)

        braces[-8:].set_color(BLUE)
        braces[0].set_color(YELLOW)

        def show_braces(n):
            cw_group = braces[-2 * n:]
            for group in cw_group, VGroup(braces[0], *cw_group):
                self.play(
                    group.scale, 0.95, {"about_point": center},
                    rate_func=there_and_back
                )
                self.wait(0.5)

        # Animated clockwise-from-keeper terms
        self.play(
            ccw_product_group.scale, 0.5, {"about_edge": UL},
            ccw_product_group.to_corner, UL,
            FadeOut(term_rect),
            FadeOut(braces[:6]),
            cw_product_parts.restore,
        )
        term_rect = cw_term_rects[0].copy()
        self.play(LaggedStartMap(ShowCreationThenDestruction, cw_label_rects))
        self.wait()
        self.play(
            FadeIn(term_rect),
            FadeIn(braces[-2:]),
            FadeIn(braces[0]),
        )
        show_braces(1)
        self.play(
            GrowArrow(cw_limit_arrows[0]),
            FadeIn(cw_limit_fractions[0])
        )
        self.wait()

        # Second and third lighthouse before
        self.play(
            Transform(term_rect, cw_term_rects[1]),
            ReplacementTransform(
                cw_limit_arrows[0].copy(), cw_limit_arrows[1]),
            FadeIn(braces[-4:-2]),
            Write(cw_limit_fractions[1])
        )
        show_braces(2)
        self.wait()
        self.play(
            Transform(term_rect, cw_term_rects[2]),
            ReplacementTransform(
                cw_limit_arrows[1].copy(), cw_limit_arrows[2]),
            FadeIn(braces[-6:-4]),
            Write(cw_limit_fractions[2])
        )
        show_braces(3)
        self.let_N_approach_infinity(VGroup(braces[0], *braces[-6:]))
        self.wait()

        # Organize fractions
        fractions = VGroup(*it.chain(*list(zip(
            limit_fractions, cw_limit_fractions,
        ))))
        fractions.generate_target()
        wallis_product = VGroup()
        dots = VGroup()
        for fraction in fractions.target:
            fraction.match_height(cw_limit_fractions[0])
            wallis_product.add(fraction)
            dot = OldTex("\\cdot")
            wallis_product.add(dot)
            dots.add(dot)
        final_dot = OldTex("\\cdots")
        for group in wallis_product, dots:
            group.submobjects[-1] = final_dot
        wallis_product.arrange(RIGHT, buff=MED_SMALL_BUFF)
        wallis_product.to_edge(RIGHT)

        self.play(
            FadeOut(limit_arrows),
            FadeOut(cw_limit_arrows),
            FadeOut(braces[-6:]),
            FadeOut(braces[0]),
            FadeOut(term_rect),
        )
        self.play(
            cw_product_parts.scale, 0.5,
            cw_product_parts.next_to, product_parts, DOWN, {
                "aligned_edge": LEFT},
            MoveToTarget(fractions),
            Write(dots),
            run_time=2,
            path_arc=90 * DEGREES
        )
        self.wait()

        self.wallis_product = VGroup(dots, fractions)
        self.observers_brace = braces[0]

    def show_limit_of_lhs(self):
        brace = self.observers_brace
        wallis_product = self.wallis_product
        result_fraction = self.result_fraction
        N, dist, over, two = result_fraction
        distance_product_equals = self.distance_product_equals

        result_rect = SurroundingRectangle(result_fraction)
        result_rect.set_color(WHITE)

        equals = OldTex("=")
        equals.next_to(brace, LEFT, SMALL_BUFF)
        approx1, approx2, approx3 = [Tex("\\approx") for x in range(3)]
        approx1.next_to(brace, LEFT, SMALL_BUFF)
        half_two_pi_over_N = OldTex(
            "{1", "\\over", "2}", "{2", "\\pi", "\\over", "N}",
        )
        pi = half_two_pi_over_N.get_part_by_tex("\\pi")
        half_two_pi_over_N.next_to(approx1, LEFT)
        approx2.next_to(half_two_pi_over_N, LEFT, SMALL_BUFF)

        approx3.move_to(distance_product_equals)

        pi_over_N = OldTex("(", "\\pi", "/", "N", ")")
        pi_over_N.next_to(N, RIGHT)
        N_shift = MED_LARGE_BUFF * RIGHT
        pi_over_N.shift(N_shift)

        pi_halves = OldTex("{\\pi", "\\over", "2}")
        pi_halves.next_to(result_rect, DOWN, LARGE_BUFF)
        pi_halves.shift(RIGHT)
        pi_halves_arrow = Arrow(
            result_rect.get_bottom(),
            pi_halves.get_top(),
            color=WHITE,
            buff=SMALL_BUFF
        )

        last_equals = OldTex("=")
        last_equals.next_to(pi_halves, LEFT)

        self.play(ShowCreation(result_rect))
        self.wait()
        self.play(
            dist.next_to, equals, LEFT,
            FadeIn(equals),
            GrowFromCenter(brace),
        )
        self.wait()
        approx2.next_to(dist, LEFT, SMALL_BUFF)
        half_two_pi_over_N.next_to(approx2, LEFT)
        self.play(
            Write(half_two_pi_over_N),
            FadeIn(approx2)
        )
        self.wait()
        self.play(
            FadeOut(half_two_pi_over_N[:4]),
            pi.shift, SMALL_BUFF * LEFT,
        )
        self.wait()
        self.play(
            ReplacementTransform(
                half_two_pi_over_N[-3:].copy(),
                pi_over_N[1:4]
            ),
            FadeIn(pi_over_N[0]),
            FadeIn(pi_over_N[-1]),
            N.shift, N_shift * RIGHT,
            ReplacementTransform(distance_product_equals, approx3)
        )
        self.wait()
        self.play(
            GrowArrow(pi_halves_arrow),
            wallis_product.shift, DOWN,
        )
        self.play(Write(pi_halves))
        self.wait(2)
        self.play(
            wallis_product.next_to, last_equals, LEFT, 2 * SMALL_BUFF,
            FadeIn(last_equals)
        )
        final_rect = SurroundingRectangle(
            VGroup(wallis_product, pi_halves),
            buff=MED_SMALL_BUFF
        )
        final_rect.set_color(YELLOW)
        self.play(ShowCreation(final_rect))
        self.wait(2)

    #

    def let_N_approach_infinity(self, braces=None, factor=4, run_time=5, zoom_in_after=False):
        lights = self.lights
        labels = self.lighthouse_labels
        keeper, sailor = self.observers
        circle = self.circle

        if braces is None:
            braces = VGroup()

        start_fraction = 1.0 / self.num_lighthouses
        target_fraction = start_fraction / factor
        # CHANGE: Python 2 integer division: half_N is used as a list index/range bound, so it must be an int
        half_N = self.num_lighthouses // 2

        fraction_tracker = ValueTracker(start_fraction)

        def get_fraction():
            return fraction_tracker.get_value()

        def get_ks_distance():
            return get_norm(keeper.dot.get_center() - sailor.dot.get_center())

        def update_title_heights(*titles):
            for title in titles:
                if not hasattr(title, "original_height"):
                    title.original_height = title.get_height()
                title.set_height(min(
                    title.original_height,
                    0.8 * get_ks_distance(),
                ))
            if len(titles) > 1:
                return titles
            else:
                return titles[0]

        initial_light_width = lights[0].get_width()

        def update_lights(lights):
            for k in range(-half_N, half_N + 1):
                if k == 0:
                    continue
                light = lights[k]
                light = light.set_width(
                    (get_fraction() / start_fraction) * initial_light_width
                )
                point = self.get_circle_point_at_proportion(k * get_fraction())
                light.move_source_to(point)
            return lights

        def update_braces(braces):
            for brace in braces:
                f1 = brace.fraction1 * (get_fraction() / start_fraction)
                f2 = brace.fraction2 * (get_fraction() / start_fraction)
                new_brace = self.get_circle_brace(f1, f2)
                new_brace.match_style(brace)
                Transform(brace, new_brace).update(1)
            return braces

        light_update_anim = UpdateFromFunc(lights, update_lights)
        label_update_anim = UpdateFromFunc(
            labels,
            lambda ls: self.position_labels_outside_lights(
                update_title_heights(*ls)),
        )
        sailor_dot_anim = UpdateFromFunc(
            sailor.dot,
            lambda d: d.move_to(
                self.get_circle_point_at_proportion(get_fraction() / 2))
        )
        sailor_title_anim = UpdateFromFunc(
            sailor.title,
            lambda m: update_title_heights(m).next_to(
                sailor.dot, RIGHT, SMALL_BUFF)
        )
        keeper_title_anim = UpdateFromFunc(
            keeper.title,
            lambda m: update_title_heights(m).next_to(
                keeper.dot, RIGHT, SMALL_BUFF)
        )
        braces_update_anim = UpdateFromFunc(braces, update_braces)

        lights[0].fade(1)
        labels[0].fade(1)

        all_updates = [
            light_update_anim,
            label_update_anim,
            sailor_dot_anim,
            sailor_title_anim,
            keeper_title_anim,
            braces_update_anim,
        ]

        self.play(
            fraction_tracker.set_value, target_fraction,
            *all_updates,
            run_time=run_time
        )
        if zoom_in_after:
            self.play(
                circle.scale, factor, {"about_point": circle.get_right()},
                *all_updates,
                run_time=1
            )
            self.wait()
            self.play(
                circle.scale, 1.0 /
                factor, {"about_point": circle.get_right()},
                *all_updates,
                run_time=1
            )
        self.wait()
        self.play(
            fraction_tracker.set_value, start_fraction,
            *all_updates,
            run_time=run_time / 2
        )

    def get_keeper_point(self):
        return self.get_circle_point_at_proportion(0)

    def get_sailor_point(self):
        return self.get_circle_point_at_proportion(0.5 / self.num_lighthouses)

    def create_pi_creatures(self):
        keeper = self.keeper = PiCreature(color=self.keeper_color).flip()
        sailor = self.sailor = Sailor()
        observers = self.observers = VGroup(keeper, sailor)
        observers.set_height(3)
        keeper.shift(4 * RIGHT + 2 * DOWN)
        sailor.shift(4 * RIGHT + 2 * UP)
        return VGroup(keeper, sailor)

    def replace_lighthouses_with_labels(self):
        lighthouse_labels = self.get_light_labels()
        self.lighthouse_labels = lighthouse_labels

        self.remove(self.lights[0], self.lighthouses[0])
        self.play(
            FadeOut(self.lighthouses[1:]),
            FadeIn(lighthouse_labels[1:]),
        )

    def get_light_labels(self):
        labels = VGroup()
        for count, point in enumerate(self.get_lh_points()):
            if count > self.num_lighthouses / 2:
                count -= self.num_lighthouses
            label = OldTex("L_{%d}" % count)
            label.scale(0.8)
            labels.add(label)
        self.position_labels_outside_lights(labels)
        return labels

    def position_labels_outside_lights(self, labels):
        center = self.circle.get_center()
        for light, label in zip(self.lights, labels):
            point = light[0].get_center()
            vect = (point - center)
            norm = get_norm(vect)
            buff = label.get_height()
            vect *= (norm + buff) / norm
            label.move_to(center + vect)
        return labels

    def get_keeper_lines(self, line_class=Line):
        lines = self.get_distance_lines(self.get_keeper_point())
        lines.set_stroke(self.keeper_color, 3)
        return lines

    def get_sailor_lines(self, line_class=Line):
        lines = self.get_distance_lines(self.get_sailor_point())
        lines.set_stroke(self.sailor_color, 3)
        return lines

    def get_term_rects(self, terms):
        return VGroup(*[
            SurroundingRectangle(term, color=WHITE)
            for term in terms
        ])

    def get_circle_brace(self, f1, f2):
        line = Line(
            self.get_circle_point_at_proportion(f1),
            self.get_circle_point_at_proportion(f2),
        )
        angle = (line.get_angle() + TAU / 2) % TAU
        scale_factor = 1.5
        line.rotate(-angle, about_point=ORIGIN)
        line.scale(scale_factor, about_point=ORIGIN)
        brace = Brace(line, DOWN, buff=SMALL_BUFF)
        group = VGroup(line, brace)
        group.scale(1.0 / scale_factor, about_point=ORIGIN)
        group.rotate(angle, about_point=ORIGIN)

        # Keep track of a fraction between -0.5 and 0.5
        if f1 > 0.5:
            f1 -= 1
        if f2 > 0.5:
            f2 -= 1
        brace.fraction1 = f1
        brace.fraction2 = f2
        return brace

    def get_all_circle_braces(self):
        fractions = np.linspace(0, 1, 2 * self.num_lighthouses + 1)
        return VGroup(*[
            self.get_circle_brace(f1, f2)
            for f1, f2 in zip(fractions, fractions[1:])
        ])
