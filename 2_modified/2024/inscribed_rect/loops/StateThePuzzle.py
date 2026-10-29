# ==============================================================================
# Scene:      StateThePuzzle
# Source:     videos/_2024/inscribed_rect/loops.py (lines 93-255)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl StateThePuzzle.py StateThePuzzle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - example_loop1.svg, example_loop2.svg and example_loop4.svg are missing (private): placeholder loops; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2024/inscribed_rect/example_loop1.svg (placeholder, make_inscribed_rect_svgs.py)
#   - _lib/assets/generated/2024/inscribed_rect/example_loop2.svg (placeholder, make_inscribed_rect_svgs.py)
#   - _lib/assets/generated/2024/inscribed_rect/example_loop4.svg (placeholder, make_inscribed_rect_svgs.py)
#
# Notes:
#   Slow render (~17 min, needs --timeout 2400): in the final part UpdateFromFunc runs true_find_square (find_rectangle x8) on every frame, about 4 s per frame.
#   The published video is the one from the 360p, 10 fps test: at 720p it takes too long (more than 500 s at 360p).
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


class StateThePuzzle(LoopScene):
    def construct(self):
        # Show the loop
        loop = get_example_loop(4)
        loop.set_height(7)
        loop.move_to(2 * RIGHT)
        curve_words = Text("Closed\nContinuous\nCurve", alignment="LEFT", font_size=72)
        curve_words.to_edge(LEFT)

        self.play(
            ShowCreation(loop),
            Write(curve_words, time_span=(3, 5)),
            run_time=9
        )

        # Show four points going to a square
        loop.insert_n_curves(50)
        loop_func = loop.quick_point_from_proportion
        quad_tracker = ValueTracker([0, 0, 0, 0])
        dots = self.get_movable_quad(quad_tracker, loop_func, colors=color_gradient([RED, PINK], 4), radius=0.075)
        square_params = find_rectangle(loop_func, target_angle=90 * DEG)

        polygon = self.get_dot_polygon(dots, stroke_color=YELLOW, stroke_width=5)
        inscribed_words = TexText(R"``Inscribed\\Square''", font_size=72)
        inscribed_words.to_edge(LEFT)

        self.add(dots)
        self.play(quad_tracker.animate.set_value(square_params), run_time=3)
        polygon.update()
        self.add(polygon, dots)
        self.play(ShowCreation(polygon, suspend_mobject_updating=True))
        self.play(
            Write(inscribed_words),
            FadeOut(curve_words, LEFT)
        )
        self.wait()

        # Alternate squares
        new_square_params = [
            [0.519, 0.308, 0.277, 0.177],
            [0.444, 0.105, 0.877, 0.650],
            [0.037, 0.739, 0.468, 0.372],
        ]
        dots.suspend_updating()
        for new_params in new_square_params:
            new_dots = dots.copy()
            new_dots.set_opacity(0)
            for dot, p in zip(new_dots, new_params):
                dot.move_to(loop_func(p))

            dots.set_opacity(0)
            self.play(Transform(dots, new_dots), run_time=2)
            dots.set_opacity(1)
            self.wait()

        # Ask question
        title = Text("Open Question", font_size=60)
        title.add(Underline(title))
        title.set_color(BLUE)
        question = Text("Do all closed\ncontinuous curves\nhave an inscribed\nsquare?", alignment="LEFT")
        question.next_to(title, DOWN)
        question.align_to(title[0], LEFT)
        question_group = VGroup(title, question)
        question_group.to_corner(UL, buff=MED_SMALL_BUFF)

        self.play(
            FadeIn(question_group, UP),
            FadeOut(inscribed_words, LEFT)
        )
        self.wait()

        # Ambiently animate to various different loops
        def true_find_square(loop_func, trg_angle=90 * DEG, cost_tol=1e-2, max_tries=8):
            ic = np.arange(0, 1, 0.25)
            min_params = ic
            min_cost = np.inf
            for x in range(max_tries):
                params, cost = find_rectangle(loop_func, target_angle=trg_angle, n_refinements=3, return_cost=True)
                if cost < min_cost:
                    min_params = params
                    min_cost = cost
                ic = np.random.random(4)
            return min_params

        new_loops = [
            get_example_loop(1),
            get_example_loop(2),
            Tex(R"\pi").family_members_with_points()[0],
            Tex(R"\epsilon").family_members_with_points()[0],
            get_example_loop(1),
        ]
        og_loop = loop.copy()
        for new_loop in new_loops:
            new_loop.insert_n_curves(50)
            new_loop.match_style(loop)
            new_loop.match_height(loop)
            new_loop.move_to(loop)

        dots.resume_updating()
        self.add(dots, polygon)
        for new_loop in new_loops:
            self.remove(dots, polygon)
            self.play(
                Transform(loop, new_loop),
                # UpdateFromFunc(
                #     quad_tracker,
                #     lambda m: m.set_value(true_find_square(loop_func))
                # ),
                run_time=1
            )
            self.add(dots, polygon)
            for _ in range(5):
                quad_tracker.set_value(find_rectangle(loop_func, np.random.random(4), target_angle=90 * DEG))
                self.wait(0.5)

        # Change question to rectangle
        square_word = question["square"]
        q_mark = question["?"]
        rect_word = Text("rectangle")
        rect_word.move_to(square_word, LEFT)
        rect_word.set_color(BLUE)
        red_line = Line(LEFT, RIGHT)
        red_line.replace(square_word, 0)
        red_line.set_stroke(RED, 8)

        self.play(
            FadeOut(title, UP),
            ShowCreation(red_line)
        )
        self.play(
            VGroup(square_word, red_line).animate.shift(0.75 * DOWN),
            Write(rect_word),
            q_mark.animate.next_to(rect_word, RIGHT, SMALL_BUFF, aligned_edge=UP),
        )
        self.wait()

        # Transition dots to rectangle
        rect_params = find_rectangle(loop_func, target_angle=45 * DEG)
        self.play(quad_tracker.animate.set_value(rect_params), run_time=4)
        self.wait()

        dots.suspend_updating()
        new_dots = dots.copy()
        for dot, p in zip(new_dots, rect_params):
            dot.move_to(loop_func(p))
        self.play(
            Transform(dots, new_dots),
            run_time=4
        )
        self.wait()
        dots.resume_updating()

        # More ambient transitioning
        for new_loop in [og_loop, *new_loops[1:3]]:
            self.play(
                Transform(loop, new_loop),
                UpdateFromFunc(
                    quad_tracker,
                    lambda m: m.set_value(true_find_square(loop_func, 60 * DEG))
                ),
                run_time=5
            )
            self.wait()
