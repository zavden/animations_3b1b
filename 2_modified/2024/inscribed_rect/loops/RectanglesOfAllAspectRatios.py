# ==============================================================================
# Scene:      RectanglesOfAllAspectRatios
# Source:     videos/_2024/inscribed_rect/loops.py (lines 2686-2800)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl RectanglesOfAllAspectRatios.py RectanglesOfAllAspectRatios -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - example_loop4.svg is missing (private): placeholder loop; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2024/inscribed_rect/example_loop4.svg (placeholder, make_inscribed_rect_svgs.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/inscribed_rect/helpers.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect4


def get_example_loop(index=1, stroke_color=WHITE, stroke_width=3, width=5):
    result = SVGMobject(f"example_loop{index}").family_members_with_points()[0]
    result.set_width(width)
    result.set_stroke(stroke_color, stroke_width)
    return result


def get_special_dot(
    color=YELLOW,
    radius=0.05,
    glow_radius_multiple=3,
    glow_factor=1.5
):
    return Group(
        TrueDot(radius=radius).make_3d(),
        GlowDot(radius=radius * glow_radius_multiple, glow_factor=glow_factor)
    ).set_color(color)


def smooth_index(lst: list, real_index: float):
    N = len(lst)
    scaled_index = real_index * (N - 1)
    int_index = int(scaled_index)
    residue = scaled_index % 1
    if int_index >= N - 1:
        return lst[-1]
    return interpolate(lst[int_index], lst[int_index + 1], residue)


def get_quick_loop_func(loop: VMobject, n_samples=501):
    samples = np.array(list(map(loop.pfp, np.linspace(0, 1, n_samples))))

    def func(x):
        return smooth_index(samples, x)

    return func


def find_rectangle(
    loop_func: Callable[[float], Vect3],
    initial_condition: Vect4 = np.arange(0, 1, 0.25),
    target_angle: float = 60 * DEGREES,
    initial_param_range: float = 1.0,
    n_samples_per_range: int = 10,
    n_refinements: int = 4,
    return_cost = False
) -> Vect4:
    """
    Returns an numpy array of 4 elements, between 0 and 1, such that 
    entering them into loop_func approximately gives a rectangle.
    """
    params = initial_condition.copy()
    param_range = initial_param_range
    min_cost = np.inf

    for _ in range(n_refinements):
        param_groups = [
            np.linspace(x - param_range / 2, x + param_range / 2, n_samples_per_range) % 1
            for x in params
        ]
        sample_groups = [
            np.array([loop_func(x) for x in param_group])
            for param_group in param_groups
        ]

        min_cost = np.inf
        best_idx_group = None
        for idx_group in it.product(*4 * [range(n_samples_per_range)]):
            a, b, c, d = [sg[i] for sg, i in zip(sample_groups, idx_group)]
            ac_dist = get_dist(a, c)
            mid_dist_ratio = get_dist(midpoint(a, c), midpoint(b, d)) / ac_dist
            dist_dist_ratio = abs(ac_dist - get_dist(b, d)) / ac_dist
            angle = abs(angle_between_vectors(c - a, d - b))
            if angle > PI / 2:
                angle = PI - angle
            cost = mid_dist_ratio + dist_dist_ratio + abs(angle - target_angle) / TAU
            if cost < min_cost:
                best_idx_group = idx_group
                min_cost = cost
        params = [pg[i] for pg, i in zip(param_groups, best_idx_group)]

        param_range /= n_samples_per_range

    if return_cost:
        return params, min_cost
    else:
        return params



# ----- From _2024/inscribed_rect/loops.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect4


class LoopScene(InteractiveScene):
    def get_dot_group(
        self,
        vect_tracker: ValueTracker,
        loop_func: Callable[[float], Vect3],
        colors=None,
        radius: float = 0.05,
        glow_factor: float = 1.5,
    ):
        n = len(vect_tracker.get_value())
        if colors is None:
            colors = [random_bright_color() for _ in range(n)]

        dots = Group(
            get_special_dot(color, radius=radius, glow_factor=glow_factor)
            for _, color in zip(range(n), it.cycle(colors))
        )

        def update_dots(dots):
            for dot, value in zip(dots, vect_tracker.get_value()):
                dot.move_to(loop_func(value))

        dots.add_updater(update_dots)
        return dots

    def get_movable_pair(
        self,
        uv_tracker: ValueTracker,
        loop_func: Callable[[float], Vect3],
        colors=[YELLOW, PINK],
        radius: float = 0.05,
        glow_factor: float = 1.5,
    ):
        return self.get_dot_group(uv_tracker, loop_func, colors, radius, glow_factor)

    def get_movable_quad(
        self,
        abcd_tracker: ValueTracker,
        loop_func: Callable[[float], Vect3],
        colors=[YELLOW, MAROON_B, PINK, RED],
        radius: float = 0.05,
        glow_factor: float = 1.5,
    ):
        return self.get_dot_group(abcd_tracker, loop_func, colors, radius, glow_factor)

    def get_connecting_line(self, dot_pair, stroke_color=TEAL_B, stroke_width=2):
        d1, d2 = dot_pair
        if stroke_color is None:
            stroke_color = average_color(d1.get_color(), d2.get_color())

        line = Line().set_stroke(stroke_color, stroke_width)
        line.f_always.put_start_and_end_on(d1.get_center, d2.get_center)
        return line

    def get_midpoint_dot(self, dot_pair, color=TEAL_B):
        dot = dot_pair[0].copy()
        dot.f_always.move_to(dot_pair.get_center)
        dot.set_color(color)
        return dot

    def get_dot_polygon(self, dots, stroke_color=BLUE, stroke_width=3):
        polygon = Polygon(LEFT, RIGHT)
        polygon.set_stroke(stroke_color, stroke_width)
        polygon.add_updater(lambda m: m.set_points_as_corners(
            [*(d.get_center() for d in dots), dots[0].get_center()]
        ))
        return polygon

    def get_dot_labels(self, dots, label_texs, direction=UL, buff=0):
        result = VGroup()
        for dot, tex in zip(dots, label_texs):
            label = Tex(tex)
            label.match_color(dot[0])
            label.set_backstroke(BLACK, 3)
            label.always.next_to(dot[0], direction, buff=buff)
            result.add(label)
        return result


class RectanglesOfAllAspectRatios(LoopScene):
    def construct(self):
        # Loop
        loop = self.get_loop()
        loop.set_height(6.5)
        loop.to_corner(DR)
        loop.set_stroke(WHITE, 1).set_fill(opacity=0)
        loop_func = get_quick_loop_func(loop)
        self.add(loop)

        # Dots
        angle_tracker = ValueTracker(90 * DEG)
        get_angle = angle_tracker.get_value
        square_params = find_rectangle(
            loop_func,
            initial_condition=np.arange(0.5, 1, 0.1),
            target_angle=angle_tracker.get_value()
        )
        abcd_tracker = ValueTracker(square_params)
        dots = self.get_movable_quad(abcd_tracker, loop_func, radius=0.075)
        rect = self.get_dot_polygon(dots)
        rect.set_stroke(YELLOW)

        rect_group = Group(abcd_tracker, dots, rect)

        self.add(rect_group)

        # Show aspect ratio
        def get_aspect_ratio():
            phi = get_angle() / 2
            return math.cot(phi)

        sample_rect = Square(side_length=2)
        sample_rect_center = 4 * LEFT + DOWN
        sample_rect_size_factor = 2.5
        sample_rect.set_stroke(YELLOW)

        def update_sample_rect(rect):
            phi = get_angle() / 2
            sf = sample_rect_size_factor
            rect.set_shape(sf * math.cos(phi), sf * math.sin(phi))
            rect.move_to(sample_rect_center)

        sample_rect.add_updater(update_sample_rect)

        aspect_ratio_label = TexText("Aspect ratio = 1:1")
        aspect_ratio_label.next_to(sample_rect, UP).shift(MED_SMALL_BUFF * LEFT)
        ar_label = aspect_ratio_label["1:1"][0]

        self.add(aspect_ratio_label[:-3])
        self.add(ar_label)
        self.add(sample_rect)
        self.wait()

        # Change angle
        def true_find_rect(loop_func, angle, max_tries=10, max_cost=1e-2):
            for _ in range(max_tries):
                result, cost = find_rectangle(
                    loop_func,
                    initial_condition=np.random.random(4),
                    target_angle=angle,
                    n_refinements=4,
                    return_cost=True
                )
                if cost < max_cost:
                    return result
            return result

        aspect_ratio_pairs = self.get_aspect_ratio_pairs()
        for tex, ratio in aspect_ratio_pairs:
            label = Tex(tex)
            label.move_to(ar_label, LEFT)
            if ratio < 1:
                ratio = 1.0 / ratio
            angle_tracker.set_value(2 * math.atan(1.0 / ratio))
            abcd_tracker.set_value(true_find_rect(loop_func, get_angle()))
            ar_label.set_submobjects(list(label))
            self.wait(1 / 3)

    def get_loop(self):
        return get_example_loop(4)

    def get_aspect_ratio_pairs(self):
        return [
            ("16 : 9", 16 / 9),
            ("4 : 3", 4 / 3),
            ("10 : 1", 10 / 1),
            (R"\sqrt{2} : 1", math.sqrt(2)),
            (R"5 : 2", 5 / 2),
            (R"\pi : 1", math.pi),
            (R"\varphi : 1", (1 + math.sqrt(5)) / 2),  # Golden ratio
            (R"e : 1", math.e),
            ("21 : 9", 21 / 9),  # Ultrawide
            (R"\sqrt{3} : 1", math.sqrt(3)),
            ("3 : 2", 3 / 2),    # Classic photography
            ("1 : 1", 1 / 1),    # Square
            (R"2\pi : 1", 2 * math.pi),
            ("7 : 5", 7 / 5),
            (R"\ln(10) : 1", math.log(10)),
            ("8 : 5", 8 / 5),
            ("12 : 5", 12 / 5),
            (R"\sqrt{5} : 1", math.sqrt(5)),
            ("9 : 16", 9 / 16),  # Portrait 16:9
            ("2 : 3", 2 / 3),    # Portrait photography
            (R"\pi : 2", math.pi / 2),
            ("7 : 3", 7 / 3),
            (R"2\sqrt{2} : 1", 2 * math.sqrt(2)),
            ("15 : 4", 15 / 4),
            (R"\sqrt{7} : 1", math.sqrt(7)),
            ("11 : 4", 11 / 4),
            (R"e : 2", math.e / 2),
            ("13 : 5", 13 / 5),
            ("8 : 3", 8 / 3),
            (R"\pi^2 : 9", math.pi ** 2 / 9)
        ]
