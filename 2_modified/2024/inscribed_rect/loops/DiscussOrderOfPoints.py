# ==============================================================================
# Scene:      DiscussOrderOfPoints
# Source:     videos/_2024/inscribed_rect/loops.py (lines 1724-1835)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl DiscussOrderOfPoints.py DiscussOrderOfPoints -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - example_loop2.svg is missing (private): placeholder loop; the code does not change
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/generated/2024/inscribed_rect/example_loop2.svg (placeholder, make_inscribed_rect_svgs.py)
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


class DiscussOrderOfPoints(LoopScene):
    def construct(self):
        # Add loops
        loop = get_example_loop(2)
        loop.set_height(6)
        loop.to_edge(DOWN, buff=0.25)
        loop_func = get_quick_loop_func(loop)
        self.add(loop)

        # Dots
        uv_tracker = ValueTracker([0.8, 0.4])
        dots = self.get_movable_pair(uv_tracker, loop_func, radius=0.1)
        line = self.get_connecting_line(dots)
        mid_dot = self.get_midpoint_dot(dots)
        mid_dot.update()

        A_label = Tex("A")
        B_label = Tex("B")
        labels = VGroup(A_label, B_label)
        for dot, label in zip(dots, labels):
            label.next_to(dot, UL, buff=-0.1)

        self.add(dots)
        self.add(labels)

        dots.clear_updaters()

        # Add question
        question = TexText(R"Is $(A, B)$ distinct from $(B, A)$?", font_size=60)
        question.to_edge(UP)
        self.play(Write(question))
        self.wait()

        # Swap points
        for _ in range(2):
            self.play(
                Swap(*dots),
                Swap(*labels),
                run_time=2
            )
            self.wait()

        # Show the same midpoint
        midpoint_word = Text("Same midpoint", font_size=36)
        midpoint_word.next_to(mid_dot, LEFT, buff=0)
        midpoint_word.set_color(TEAL)

        dist_word = Text("Same distance", font_size=36)
        dist_word.set_color(TEAL)
        dist_word.next_to(ORIGIN, DOWN, SMALL_BUFF)
        dist_word.rotate(line.get_angle(), about_point=ORIGIN)
        dist_word.shift(mid_dot.get_center())

        self.play(
            GrowFromCenter(line, suspend_mobject_updating=True),
            FadeIn(mid_dot),
            FadeIn(midpoint_word, lag_ratio=0.1),
        )
        self.play(Swap(*dots))
        self.play(
            TransformMatchingStrings(
                midpoint_word, dist_word,
                key_map={"midpoint": "distance"},
                run_time=1
            )
        )
        self.play(Swap(*dots))
        self.play(FadeOut(dist_word))
        self.wait()

        # Answer
        answer = Text("It shouldn't be!")
        answer.next_to(question, DOWN)
        answer.to_edge(RIGHT)
        answer.set_color(RED)

        self.play(FadeIn(answer, lag_ratio=0.1))
        self.wait()

        # Show trivial rectangle
        frame = self.frame
        angle = 60 * DEG
        question.fix_in_frame()
        answer.fix_in_frame()
        pair_group1 = Group(dots, line)
        pair_group1.clear_updaters()
        pair_group2 = pair_group1.copy()
        dots2 = pair_group2[0]
        dots2[0].set_color(PINK)
        dots2[1].set_color(YELLOW)
        pair_group2.rotate(angle, about_point=mid_dot.get_center())

        rect = self.get_dot_polygon(
            list(it.chain(*zip(dots, dots2)))
        )
        rect.update()

        self.play(
            FadeOut(loop),
            FadeIn(pair_group2),
            VFadeIn(rect),
            frame.animate.move_to(mid_dot.get_center() + 0.5 * UP).set_height(6)
        )
        self.play(
            Rotate(pair_group2, -angle, about_point=mid_dot.get_center()),
            run_time=5
        )
        self.wait()
        self.play(
            Rotate(pair_group2, -angle, about_point=mid_dot.get_center()),
            run_time=5
        )
