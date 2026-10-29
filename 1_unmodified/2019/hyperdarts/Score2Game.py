# ==============================================================================
# Scene:      Score2Game
# Source:     videos/_2019/hyperdarts.py (lines 1928-1931)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Score2Game.py Score2Game -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HyperdartScene(MovingCameraScene):
    CONFIG = {
        "square_width": 6,
        "square_style": {
            "stroke_width": 2,
            "fill_color": BLUE,
            "fill_opacity": 0.5,
        },
        "circle_style": {
            "fill_color": RED_E,
            "fill_opacity": 1,
            "stroke_width": 0,
        },
        "circle_center_dot_radius": 0.025,
        "default_line_style": {
            "stroke_width": 2,
            "stroke_color": WHITE,
        },
        "default_dot_config": {
            "fill_color": WHITE,
            "background_stroke_width": 1,
            "background_stroke_color": BLACK,
            "radius": 0.5 * DEFAULT_DOT_RADIUS,
        },
        "dart_sound": "dart_low",
        "default_bullseye_shadow_opacity": 0.35,
    }

    def setup(self):
        MovingCameraScene.setup(self)
        self.square = self.get_square()
        self.circle = self.get_circle()
        self.circle_center_dot = self.get_circle_center_dot()

        self.add(self.square)
        self.add(self.circle)
        self.add(self.circle_center_dot)

    def get_square(self):
        return Square(
            side_length=self.square_width,
            **self.square_style
        )

    def get_circle(self, square=None):
        square = square or self.square
        circle = Circle(**self.circle_style)
        circle.replace(square)
        return circle

    def get_circle_center_dot(self, circle=None):
        circle = circle or self.circle
        return Dot(
            circle.get_center(),
            radius=self.circle_center_dot_radius,
            fill_color=BLACK,
        )

    def get_number_plane(self):
        square = self.square
        unit_size = square.get_width() / 2
        plane = NumberPlane(
            axis_config={
                "unit_size": unit_size,
            }
        )
        plane.add_coordinates()
        plane.shift(square.get_center() - plane.c2p(0, 0))
        return plane

    def get_random_points(self, n):
        square = self.square
        points = np.random.uniform(-1, 1, 3 * n).reshape((n, 3))

        points[:, 0] *= square.get_width() / 2
        points[:, 1] *= square.get_height() / 2
        points[:, 2] = 0
        points += square.get_center()
        return points

    def get_random_point(self):
        return self.get_random_points(1)[0]

    def get_dot(self, point):
        return Dot(point, **self.default_dot_config)

    # Hit transform rules
    def is_inside(self, point, circle=None):
        circle = circle or self.circle
        return get_norm(point - circle.get_center()) <= circle.get_width() / 2

    def get_new_radius(self, point, circle=None):
        circle = circle or self.circle
        center = circle.get_center()
        radius = circle.get_width() / 2
        p_dist = get_norm(point - center)
        return np.sqrt(radius**2 - p_dist**2)

    def get_hit_distance_line(self, point, circle=None):
        circle = circle or self.circle

        line = Line(
            circle.get_center(), point,
            **self.default_line_style
        )
        return line

    def get_chord(self, point, circle=None):
        circle = circle or self.circle

        center = circle.get_center()
        p_angle = angle_of_vector(point - center)
        chord = Line(DOWN, UP)
        new_radius = self.get_new_radius(point, circle)
        chord.scale(new_radius)
        chord.rotate(p_angle)
        chord.move_to(point)
        chord.set_style(**self.default_line_style)
        return chord

    def get_radii_to_chord(self, chord, circle=None):
        circle = circle or self.circle

        center = circle.get_center()
        radii = VGroup(*[
            DashedLine(center, point)
            for point in chord.get_start_and_end()
        ])
        radii.set_style(**self.default_line_style)
        return radii

    def get_all_hit_lines(self, point, circle=None):
        h_line = self.get_hit_distance_line(point, circle)
        chord = self.get_chord(point, circle)
        # radii = self.get_radii_to_chord(chord, circle)

        elbow = Elbow(width=0.15)
        elbow.set_stroke(WHITE, 2)
        elbow.rotate(h_line.get_angle() - PI, about_point=ORIGIN)
        elbow.shift(point)

        return VGroup(h_line, chord, elbow)

    def get_dart(self, length=1.5):
        dart = SVGMobject(file_name="dart")
        dart.rotate(135 * DEGREES)
        dart.set_width(length)
        dart.rotate(45 * DEGREES, UP)
        dart.rotate(-10 * DEGREES)

        dart.set_fill(GREY)
        dart.set_sheen(2, UL)
        dart.set_stroke(BLACK, 0.5, background=True)
        dart.set_stroke(width=0)
        return dart

    # New circle
    def get_new_circle_from_point(self, point, circle=None):
        return self.get_new_circle(
            self.get_new_radius(point, circle),
            circle,
        )

    def get_new_circle_from_chord(self, chord, circle=None):
        return self.get_new_circle(
            chord.get_length() / 2,
            circle,
        )

    def get_new_circle(self, new_radius, circle=None):
        circle = circle or self.circle
        new_circle = self.get_circle()
        new_circle.set_width(2 * new_radius)
        new_circle.move_to(circle)
        return new_circle

    # Sound
    def add_dart_sound(self, time_offset=0, gain=-20, **kwargs):
        self.add_sound(
            self.dart_sound,
            time_offset=time_offset,
            gain=-20,
            **kwargs,
        )

    # Animations
    def show_full_hit_process(self, point, pace="slow", with_dart=True):
        assert(pace in ["slow", "fast"])

        to_fade = VGroup()

        if with_dart:
            dart, dot = self.show_hit_with_dart(point)
            to_fade.add(dart, dot)
        else:
            dot = self.show_hit(point)
            to_fade.add(dot)

        if pace == "slow":
            self.wait(0.5)

        # TODO, automatically act based on hit or miss?

        lines = self.show_geometry(point, pace)
        chord_and_shadow = self.show_circle_shrink(lines[1], pace=pace)

        to_fade.add_to_back(chord_and_shadow, lines)

        self.play(
            FadeOut(to_fade),
            run_time=(1 if pace == "slow" else 0.5)
        )

    def show_hits_with_darts(self, points, run_time=0.5, added_anims=None):
        if added_anims is None:
            added_anims = []

        darts = VGroup(*[
            self.get_dart().move_to(point, DR)
            for point in points
        ])
        dots = VGroup(*[
            self.get_dot(point)
            for point in points
        ])

        for dart in darts:
            dart.save_state()
            dart.set_x(-(FRAME_WIDTH + dart.get_width()) / 2)
            dart.rotate(20 * DEGREES)

        n_points = len(points)
        self.play(
            ShowIncreasingSubsets(
                dots,
                rate_func=squish_rate_func(linear, 0.5, 1),
            ),
            LaggedStart(*[
                Restore(
                    dart,
                    path_arc=-20 * DEGREES,
                    rate_func=linear,
                    run_time=run_time,
                )
                for dart in darts
            ], lag_ratio=(1 / n_points)),
            *added_anims,
            run_time=run_time
        )
        for n in range(n_points):
            self.add_dart_sound(
                time_offset=(-n / (2 * n_points))
            )

        return darts, dots

    def show_hit_with_dart(self, point, run_time=0.25, **kwargs):
        darts, dots = self.show_hits_with_darts([point], run_time, **kwargs)
        return darts[0], dots[0]

    def show_hit(self, point, pace="slow", added_anims=None):
        assert(pace in ["slow", "fast"])
        if added_anims is None:
            added_anims = []

        dot = self.get_dot(point)
        if pace == "slow":
            self.play(
                FadeInFromLarge(dot, rate_func=rush_into),
                *added_anims,
                run_time=0.5,
            )
        elif pace == "fast":
            self.add(dot)
        # self.add_dart_sound()
        return dot

    def show_geometry(self, point, pace="slow"):
        assert(pace in ["slow", "fast"])

        lines = self.get_all_hit_lines(point, self.circle)
        h_line, chord, elbow = lines

        # Note, note animating radii anymore...does that mess anything up?
        if pace == "slow":
            self.play(
                ShowCreation(h_line),
                GrowFromCenter(chord),
            )
            self.play(ShowCreation(elbow))
        elif pace == "fast":
            self.play(
                ShowCreation(h_line),
                GrowFromCenter(chord),
                ShowCreation(elbow),
                run_time=0.5
            )
        # return VGroup(h_line, chord)
        return lines

    def show_circle_shrink(self, chord, pace="slow", shadow_opacity=None):
        circle = self.circle
        chord_copy = chord.copy()
        new_circle = self.get_new_circle_from_chord(chord)
        to_fade = VGroup(chord_copy)

        if shadow_opacity is None:
            shadow_opacity = self.default_bullseye_shadow_opacity
        if shadow_opacity > 0:
            shadow = circle.copy()
            shadow.set_opacity(shadow_opacity)
            to_fade.add_to_back(shadow)
            if circle in self.mobjects:
                index = self.mobjects.index(circle)
                self.mobjects.insert(index, shadow)
            else:
                self.add(shadow, self.circle_center_dot)

        outline = VGroup(*[
            VMobject().pointwise_become_partial(new_circle, a, b)
            for (a, b) in [(0, 0.5), (0.5, 1)]
        ])
        outline.rotate(chord.get_angle())
        outline.set_fill(opacity=0)
        outline.set_stroke(YELLOW, 2)

        assert(pace in ["slow", "fast"])

        if pace == "slow":
            self.play(
                chord_copy.move_to, circle.get_center(),
                circle.set_opacity, 0.5,
            )
            self.play(
                Rotating(
                    chord_copy,
                    radians=PI,
                ),
                ShowCreation(
                    outline,
                    lag_ratio=0
                ),
                run_time=1,
                rate_func=smooth,
            )
            self.play(
                Transform(circle, new_circle),
                FadeOut(outline),
            )
        elif pace == "fast":
            outline = new_circle.copy()
            outline.set_fill(opacity=0)
            outline.set_stroke(YELLOW, 2)
            outline.move_to(chord)
            outline.generate_target()
            outline.target.move_to(circle)
            self.play(
                chord_copy.move_to, circle,
                Transform(circle, new_circle),
                # MoveToTarget(
                #     outline,
                #     remover=True
                # )
            )
            # circle.become(new_circle)
            # circle.become(new_circle)
            # self.remove(new_circle)
        return to_fade

    def show_miss(self, point, with_dart=True):
        square = self.square
        miss = OldTexText("Miss!")
        miss.next_to(point, UP)
        to_fade = VGroup(miss)

        if with_dart:
            dart, dot = self.show_hit_with_dart(point)
            to_fade.add(dart, dot)
        else:
            dot = self.show_hit(point)
            to_fade.add(dot)
        self.play(
            ApplyMethod(
                square.set_color, YELLOW,
                rate_func=lambda t: (1 - t),
            ),
            GrowFromCenter(miss),
            run_time=0.25
        )
        return to_fade

    def show_game_over(self):
        game_over = OldTexText("GAME OVER")
        game_over.set_width(FRAME_WIDTH - 1)
        rect = FullScreenFadeRectangle(opacity=0.25)

        self.play(
            FadeIn(rect),
            FadeInFromLarge(game_over),
        )
        return VGroup(rect, game_over)


class GameWithSpecifiedScore(HyperdartScene):
    CONFIG = {
        "score": 1,
        "random_seed": 1,
    }

    def construct(self):
        board = VGroup(self.square, self.circle, self.circle_center_dot)
        board.to_edge(DOWN, buff=0.5)

        score_label = VGroup(
            OldTexText("Score: "),
            Integer(1)
        )
        score_label.scale(2)
        score_label.arrange(RIGHT, aligned_edge=DOWN)
        score_label.to_edge(UP, buff=0.25)

        self.add(score_label)

        score = 1
        pace = "fast"
        while True:
            point = self.get_random_point()
            want_to_continue = (score < self.score)
            if want_to_continue:
                while not self.is_inside(point):
                    point = self.get_random_point()

                dart, dot = self.show_hit_with_dart(point)
                score_label[1].increment_value()
                lines = self.show_geometry(point, pace)
                chord_and_shadow = self.show_circle_shrink(lines[1], pace=pace)

                self.play(
                    FadeOut(VGroup(dart, dot, lines, chord_and_shadow)),
                    run_time=0.5,
                )
                score += 1
            else:
                while self.is_inside(point):
                    point = self.get_random_point()
                self.show_miss(point)
                self.play(ShowCreationThenFadeAround(score_label[1]))
                self.wait()
                return


class Score2Game(GameWithSpecifiedScore):
    CONFIG = {
        "score": 2,
    }
