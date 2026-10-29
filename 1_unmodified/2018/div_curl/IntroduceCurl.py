# ==============================================================================
# Scene:      IntroduceCurl
# Source:     videos/_2018/div_curl.py (lines 2058-2171)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceCurl.py IntroduceCurl -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def four_swirls_function(point):
    x, y = point[:2]
    result = (y**3 - 4 * y) * RIGHT + (x**3 - 16 * x) * UP
    result *= 0.05
    norm = get_norm(result)
    if norm == 0:
        return result
    # result *= 2 * sigmoid(norm) / norm
    return result


def get_force_field_func(*point_strength_pairs, **kwargs):
    radius = kwargs.get("radius", 0.5)

    def func(point):
        result = np.array(ORIGIN)
        for center, strength in point_strength_pairs:
            to_center = center - point
            norm = get_norm(to_center)
            if norm == 0:
                continue
            elif norm < radius:
                to_center /= radius**3
            elif norm >= radius:
                to_center /= norm**3
            to_center *= -strength
            result += to_center
        return result
    return func


class IntroduceVectorField(Scene):
    CONFIG = {
        "vector_field_config": {
            # "delta_x": 2,
            # "delta_y": 2,
            "delta_x": 0.5,
            "delta_y": 0.5,
        },
        "stream_line_config": {
            "start_points_generator_config": {
                # "delta_x": 1,
                # "delta_y": 1,
                "delta_x": 0.25,
                "delta_y": 0.25,
            },
            "virtual_time": 3,
        },
        "stream_line_animation_config": {
            # "line_anim_class": ShowPassingFlash,
            "line_anim_class": ShowPassingFlashWithThinningStrokeWidth,
        }
    }

    def construct(self):
        self.add_plane()
        self.add_title()
        self.points_to_vectors()
        self.show_fluid_flow()
        self.show_gravitational_force()
        self.show_magnetic_force()
        self.show_fluid_flow()

    def add_plane(self):
        plane = self.plane = NumberPlane()
        plane.add_coordinates()
        plane.remove(plane.coordinate_labels[-1])
        self.add(plane)

    def add_title(self):
        title = OldTexText("Vector field")
        title.scale(1.5)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle(opacity=1, buff=SMALL_BUFF)
        self.add_foreground_mobjects(title)

    def points_to_vectors(self):
        vector_field = self.vector_field = VectorField(
            four_swirls_function,
            **self.vector_field_config
        )
        dots = VGroup()
        for vector in vector_field:
            dot = Dot(radius=0.05)
            dot.move_to(vector.get_start())
            dot.target = vector
            dots.add(dot)

        self.play(LaggedStartMap(GrowFromCenter, dots))
        self.wait()
        self.play(LaggedStartMap(MoveToTarget, dots, remover=True))
        self.add(vector_field)
        self.wait()

    def show_fluid_flow(self):
        vector_field = self.vector_field
        stream_lines = StreamLines(
            vector_field.func,
            **self.stream_line_config
        )
        stream_line_animation = AnimatedStreamLines(
            stream_lines,
            **self.stream_line_animation_config
        )

        self.add(stream_line_animation)
        self.play(
            vector_field.set_fill, {"opacity": 0.5}
        )
        self.wait(7)
        self.play(
            vector_field.set_fill, {"opacity": 1},
            VFadeOut(stream_line_animation.mobject),
        )
        self.remove(stream_line_animation)

    def show_gravitational_force(self):
        earth = self.earth = ImageMobject("earth")
        moon = self.moon = ImageMobject("moon", height=1)
        earth_center = 3 * RIGHT + 2 * UP
        moon_center = 3 * LEFT + DOWN
        earth.move_to(earth_center)
        moon.move_to(moon_center)

        gravity_func = get_force_field_func((earth_center, -6), (moon_center, -1))
        gravity_field = VectorField(
            gravity_func,
            **self.vector_field_config
        )

        self.add_foreground_mobjects(earth, moon)
        self.play(
            GrowFromCenter(earth),
            GrowFromCenter(moon),
            Transform(self.vector_field, gravity_field),
            run_time=2
        )
        self.vector_field.func = gravity_field.func
        self.wait()

    def show_magnetic_force(self):
        magnetic_func = get_force_field_func(
            (3 * LEFT, -1), (3 * RIGHT, +1)
        )
        magnetic_field = VectorField(
            magnetic_func,
            **self.vector_field_config
        )
        magnet = VGroup(*[
            Rectangle(
                width=3.5,
                height=1,
                stroke_width=0,
                fill_opacity=1,
                fill_color=color
            )
            for color in (BLUE, RED)
        ])
        magnet.arrange(RIGHT, buff=0)
        for char, vect in ("S", LEFT), ("N", RIGHT):
            letter = OldTexText(char)
            edge = magnet.get_edge_center(vect)
            letter.next_to(edge, -vect, buff=MED_LARGE_BUFF)
            magnet.add(letter)

        self.add_foreground_mobjects(magnet)
        self.play(
            self.earth.scale, 0,
            self.moon.scale, 0,
            DrawBorderThenFill(magnet),
            Transform(self.vector_field, magnetic_field),
            run_time=2
        )
        self.vector_field.func = magnetic_field.func
        self.remove_foreground_mobjects(self.earth, self.moon)


class IntroduceCurl(IntroduceVectorField):
    CONFIG = {
        "stream_line_animation_config": {
            "line_anim_class": ShowPassingFlash,
        },
        "stream_line_config": {
            "start_points_generator_config": {
                "delta_x": 0.125,
                "delta_y": 0.125,
            },
            "virtual_time": 1,
        }
    }

    def construct(self):
        self.add_title()
        self.show_vector_field()
        self.begin_flow()
        self.show_rotation()

    def add_title(self):
        title = self.title = Title(
            "Curl",
            match_underline_width_to_text=True,
            scale_factor=1.5,
        )
        title.add_background_rectangle()
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        self.add_foreground_mobjects(title)

    def show_vector_field(self):
        vector_field = self.vector_field = VectorField(
            four_swirls_function,
            **self.vector_field_config
        )
        vector_field.submobjects.sort(
            key=lambda v: v.get_length()
        )

        self.play(LaggedStartMap(GrowArrow, vector_field))
        self.wait()

    def begin_flow(self):
        stream_lines = StreamLines(
            self.vector_field.func,
            **self.stream_line_config
        )
        stream_line_animation = AnimatedStreamLines(
            stream_lines,
            **self.stream_line_animation_config
        )

        self.add(stream_line_animation)
        self.wait(3)

    def show_rotation(self):
        clockwise_arrows, counterclockwise_arrows = [
            VGroup(*[
                self.get_rotation_arrows(clockwise=cw).move_to(point)
                for point in points
            ])
            for cw, points in [
                (True, [2 * UP, 2 * DOWN]),
                (False, [4 * LEFT, 4 * RIGHT]),
            ]
        ]

        for group, u in (counterclockwise_arrows, +1), (clockwise_arrows, -1):
            for arrows in group:
                label = OldTex(
                    "\\text{curl} \\, \\textbf{F}",
                    ">" if u > 0 else "<",
                    "0"
                )
                label.add_background_rectangle()
                label.next_to(arrows, DOWN)
                self.add_foreground_mobjects(label)
                always_rotate(arrows, rate=u * 30 * DEGREES)
                self.play(
                    FadeIn(arrows),
                    FadeIn(label)
                )
        self.wait(2)
        for group in counterclockwise_arrows, clockwise_arrows:
            self.play(FocusOn(group[0]))
            self.play(
                UpdateFromAlphaFunc(
                    group,
                    lambda mob, alpha: mob.set_color(
                        interpolate_color(WHITE, PINK, alpha)
                    ).set_stroke(
                        width=interpolate(5, 10, alpha)
                    ),
                    rate_func=there_and_back,
                    run_time=2
                )
            )
            self.wait()
        self.wait(6)

    # Helpers
    def get_rotation_arrows(self, clockwise=True, width=1):
        result = VGroup(*[
            Arrow(
                *points,
                buff=2 * SMALL_BUFF,
                path_arc=90 * DEGREES
            ).set_stroke(width=5)
            for points in adjacent_pairs(compass_directions(4, RIGHT))
        ])
        if clockwise:
            result.flip()
        result.set_width(width)
        return result
