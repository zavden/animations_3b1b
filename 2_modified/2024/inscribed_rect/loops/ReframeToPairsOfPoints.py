# ==============================================================================
# Scene:      ReframeToPairsOfPoints
# Source:     videos/_2024/inscribed_rect/loops.py (lines 258-420)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl ReframeToPairsOfPoints.py ReframeToPairsOfPoints -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - xmas_tree.svg is missing (private): placeholder Christmas tree outline; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2024/inscribed_rect/xmas_tree.svg (placeholder, make_inscribed_rect_svgs.py)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/inscribed_rect/helpers.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect4


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


class ReframeToPairsOfPoints(LoopScene):
    def construct(self):
        # Add loop and dots
        loop = SVGMobject("xmas_tree").family_members_with_points()[0]
        loop.set_stroke(WHITE, 3)
        loop.set_fill(opacity=0)
        loop.insert_n_curves(100)
        loop.set_height(7)
        loop.to_edge(RIGHT)
        loop_func = loop.quick_point_from_proportion

        quad_tracker = ValueTracker(np.arange(0, 1, 0.25))
        dots = self.get_movable_quad(quad_tracker, loop_func, radius=0.075)
        labels = self.get_dot_labels(dots, "ABCD")
        labels.set_backstroke(BLACK, 3)
        rect_params = find_rectangle(loop_func, target_angle=55 * DEG)
        quad_tracker.set_value(rect_params + np.random.uniform(0.2, 0.2, 4))

        self.add(quad_tracker, loop, dots, labels)

        # Add words
        question1 = VGroup(
            Text("Find four points"),
            Tex("(A, B, C, D)"),
            Text("That form a rectangle"),
        )
        question2 = VGroup(
            Text("Find two pairs of points", t2s={"pairs": ITALIC}),
            Tex(
                R"\{\{A, C\}, \{B, D\}\}",
                t2c={"A": YELLOW, "B": RED, "C": YELLOW, "D": RED},
            ),
            Text("With the same midpoint\nand distance apart"),
        )
        for question in question1, question2:
            question.arrange(DOWN, buff=0.35)
            question.to_corner(UL)

        for char, label in zip("ABCD", labels):
            question1[1][char].match_style(label)

        self.add(question1)

        # Move to rectangle
        polygon = self.get_dot_polygon(dots)

        self.play(quad_tracker.animate.set_value(rect_params), run_time=8)
        polygon.update()
        self.play(
            ShowCreation(polygon, suspend_mobject_updating=True),
            loop.animate.set_stroke(width=2, opacity=0.5),
            run_time=2
        )
        self.wait()

        # Switch question
        line1 = self.get_connecting_line(dots[0::2]).set_stroke(YELLOW)
        line2 = self.get_connecting_line(dots[1::2]).set_stroke(RED)
        lines = VGroup(line1, line2)
        lines.update().suspend_updating()

        self.play(
            FadeOut(polygon),
            FadeOut(question1[2], DOWN),
            TransformMatchingStrings(question1[0], question2[0], key_map={"four": "two pairs of"}, mismatch_animation=FadeTransformPieces),
            TransformMatchingTex(question1[1], question2[1]),
            dots[2].animate.set_color(YELLOW),
            dots[1].animate.set_color(RED),
            labels[2].animate.set_fill(YELLOW),
            labels[1].animate.set_fill(RED),
        )
        self.wait()
        self.play(LaggedStartMap(ShowCreation, lines, lag_ratio=0.5))
        self.wait()

        # Show the midpoint
        mid_dot1 = self.get_midpoint_dot(dots[0::2])
        mid_dot2 = self.get_midpoint_dot(dots[1::2])
        mid_dot1.update()
        mid_dot2.update()
        arrow = Vector(RIGHT)
        arrow.match_color(mid_dot1[0])
        arrow.next_to(mid_dot1, LEFT, SMALL_BUFF)

        self.play(
            FadeIn(mid_dot1),
            GrowArrow(arrow),
            FadeIn(question2[2]["With the same midpoint"], lag_ratio=0.1)
        )
        self.play(
            FlashAround(question2[2]["midpoint"], color=TEAL),
            question2[2]["midpoint"].animate.set_color(TEAL),
        )
        self.wait()

        # Show the distance apart
        frame = self.frame
        new_lines = lines.copy()
        new_lines.clear_updaters()
        for line in new_lines:
            line.rotate(PI / 2 - line.get_angle())
        new_lines.arrange(RIGHT, buff=0.5)
        new_lines.next_to(loop, LEFT, buff=0.5)

        self.play(
            TransformFromCopy(lines, new_lines),
            Write(question2[2]["and distance apart"]),
            run_time=2
        )
        self.play(
            question2[2]["distance apart"].animate.set_color(YELLOW),
            FlashUnder(question2[2]["distance apart"]),
            run_time=1
        )
        self.wait()

        # Clear the loop and such
        dots.clear_updaters()
        dots[0].f_always.move_to(line1.get_start)
        dots[2].f_always.move_to(line1.get_end)
        dots[1].f_always.move_to(line2.get_start)
        dots[3].f_always.move_to(line2.get_end)

        self.play(
            LaggedStartMap(FadeOut, Group(mid_dot1, arrow, loop, new_lines)),
            question2[2].animate.set_opacity(0.25),
            line1.animate.scale(0.35).rotate(45 * DEG).shift(UP),
            line2.animate.scale(0.90).rotate(-30 * DEG).shift(DOWN),
            run_time=2
        )
        self.wait()

        # Match the midpoints
        for dot in mid_dot1, mid_dot2:
            dot.set_color(WHITE)
            dot.scale(0.5)

        target_midpoint = midpoint(line1.get_center(), line2.get_center())

        self.play(
            *map(FadeIn, [mid_dot1, mid_dot2]),
            question2[2]["With the same midpoint"].animate.set_fill(opacity=1),
        )
        self.play(
            line1.animate.move_to(target_midpoint),
            line2.animate.move_to(target_midpoint),
        )
        self.wait()

        # Match the distance
        self.play(
            line1.animate.set_length(line2.get_length()),
            question2[2]["and distance apart"].animate.set_opacity(1),
            run_time=2
        )
        self.wait()

        # Show various rectangles
        polygon.update()
        self.play(ShowCreation(polygon, suspend_mobject_updating=True))
        for line in [line2, line1, line2]:
            self.play(Rotate(line, 100 * DEG), run_time=4)
        self.wait()
