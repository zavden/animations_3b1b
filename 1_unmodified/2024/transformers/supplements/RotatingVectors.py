# ==============================================================================
# Scene:      RotatingVectors
# Source:     videos/_2024/transformers/supplements.py (lines 1905-1914)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl RotatingVectors.py RotatingVectors -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


class Dial(VGroup):
    def __init__(
        self,
        radius=0.5,
        relative_tick_size=0.2,
        value_range=(0, 1, 0.1),
        initial_value=0,
        arc_angle=270 * DEGREES,
        stroke_width=2,
        stroke_color=WHITE,
        needle_color=BLUE,
        needle_stroke_width=5.0,
        value_to_color_config=dict(),
        set_anim_streak_color=TEAL,
        set_anim_streak_width=4,
        set_value_anim_streak_density=6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value_range = value_range
        self.value_to_color_config = value_to_color_config
        self.set_anim_streak_color = set_anim_streak_color
        self.set_anim_streak_width = set_anim_streak_width
        self.set_value_anim_streak_density = set_value_anim_streak_density

        # Main dial
        self.arc = Arc(arc_angle / 2, -arc_angle, radius=radius)
        self.arc.rotate(90 * DEGREES, about_point=ORIGIN)

        low, high, step = value_range
        n_values = int(1 + (high - low) / step)
        tick_points = map(self.arc.pfp, np.linspace(0, 1, n_values))
        self.ticks = VGroup(*(
            Line((1.0 - relative_tick_size) * point, point)
            for point in tick_points
        ))
        self.bottom_point = VectorizedPoint(radius * DOWN)
        for mob in self.arc, self.ticks:
            mob.set_stroke(stroke_color, stroke_width)

        self.add(self.arc, self.ticks, self.bottom_point)

        # Needle
        self.needle = Line()
        self.needle.set_stroke(
            color=needle_color,
            width=[needle_stroke_width, 0]
        )
        self.add(self.needle)

        # Initialize
        self.set_value(initial_value)

    def value_to_point(self, value):
        low, high, step = self.value_range
        alpha = inverse_interpolate(low, high, value)
        return self.arc.pfp(alpha)

    def set_value(self, value):
        self.needle.put_start_and_end_on(
            self.get_center(),
            self.value_to_point(value)
        )
        self.needle.set_color(value_to_color(
            value,
            min_value=self.value_range[0],
            max_value=self.value_range[1],
            **self.value_to_color_config
        ))

    def animate_set_value(self, value, **kwargs):
        kwargs.pop("path_arc", None)
        center = self.get_center()
        points = [self.needle.get_end(), self.value_to_point(value)]
        vects = [point - center for point in points]
        angle1, angle2 = [
            (angle_of_vector(vect) + TAU / 4) % TAU - TAU / 4
            for vect in vects
        ]
        path_arc = angle2 - angle1

        density = self.set_value_anim_streak_density
        radii = np.linspace(0, 0.5 * self.get_width(), density + 1)[1:]
        diff_arcs = VGroup(*(
            Arc(
                angle1, angle2 - angle1,
                radius=radius,
                arc_center=center,
            )
            for radius in radii
        ))
        diff_arcs.set_stroke(self.set_anim_streak_color, self.set_anim_streak_width)

        return AnimationGroup(
            self.animate.set_value(value).set_anim_args(path_arc=path_arc, **kwargs),
            *(
                VShowPassingFlash(diff_arc, time_width=1.5, **kwargs)
                for diff_arc in diff_arcs
            )
        )

    def get_random_value(self):
        low, high, step = self.value_range
        return interpolate(low, high, random.random())



# ----- From _2024/transformers/supplements.py -----

class ReflectOnTwoThings(TeacherStudentsScene):
    def construct(self):
        # Initial reactions
        morty = self.teacher
        screen = self.screen
        stds = self.students

        morty.change_mode("raise_right_hand").look_at(self.screen)
        for std in stds:
            std.change_mode("happy")
        self.play(
            self.change_students("pondering", "thinking", "happy", look_at=screen)
        )
        self.wait(2)

        # Reflection points
        points = VGroup(
            Text("Two points of reflection"),
            Text("1."),
            Text("2."),
        )

        points[0].add(Underline(points[0], buff=-0.05))
        points[0].scale(1.25)
        points[0].set_color(YELLOW)

        dials = VGroup(Dial(initial_value=random.random()) for n in range(10))
        dials.set_height(0.5)
        dials.arrange(RIGHT)
        dials.set_flat_stroke(True)
        dials[-2].become(Tex(R"\dots").replace(dials[-2], dim_to_match=0))
        dials.next_to(points[1], RIGHT)
        points[1].add(dials)

        vectors = self.get_vectors()
        points[2].add(vectors)

        points.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        points.to_edge(UP)
        points[1:].shift(MED_SMALL_BUFF * RIGHT + 0.5 * DOWN)

        self.play(
            morty.change("tease", points[0]),
            self.change_students("erm", "plain", "hesitant", look_at=points[0]),
            Write(points[0], stroke_color=YELLOW_B),
        )
        self.wait(2)
        self.play(
            Write(points[1][:2]),
            LaggedStartMap(FadeIn, dials, lag_ratio=0.25),
            self.change_students("tease", "plain", "erm", look_at=points[1]),
            morty.change("raise_right_hand", points[1]),
        )
        self.wait(2)

        # Show vector clump
        self.play(
            VFadeIn(points[2]),
            Rotate(vectors, PI, axis=UP, run_time=8),
            self.change_students("confused", "hesitant", "erm", look_at=points[2]),
            morty.change("surprised", points[2]),
        )
        self.wait(3)

    def get_vectors(self):
        dodec = Dodecahedron()
        vectors = VGroup()
        for face in dodec:
            # for vert in face.get_anchors():
            for vert in [face.get_center()]:
                if not any([np.isclose(vert, v.get_end()).all() for v in vectors]):
                    vect = Vector(vert)
                    vect.set_color(random_bright_color(hue_range=(0.5, 0.7)))
                    vect.always.set_perpendicular_to_camera(self.frame)
                    vectors.add(vect)
        vectors.rotate(25 * DEGREES, axis=UR)
        vectors.set_height(1.5)
        return vectors


class RotatingVectors(ReflectOnTwoThings):
    def construct(self):
        self.clear()
        # Test
        vectors = self.get_vectors()
        vectors.set_height(4)

        self.play(
            Rotate(vectors, TAU, axis=UP, run_time=25, rate_func=linear),
        )
