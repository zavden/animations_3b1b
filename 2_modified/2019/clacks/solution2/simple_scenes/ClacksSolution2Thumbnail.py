# ==============================================================================
# Scene:      ClacksSolution2Thumbnail
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 768-877)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/lost_lecture.py, _2019/clacks/question.py, _2019/clacks/solution2/mirror_scenes.py
#
# Run from this folder:
#     manimgl ClacksSolution2Thumbnail.py ClacksSolution2Thumbnail -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Complete the migration of ClackFlashes to updaters with dt and Animation.interpolate.
#   - Explicitly pass Block's fill and stroke to Square; GL overwrote them with its defaults.
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
#   - The nested scenes (Thumbnail, ReflectWorldThroughMirrorNew) are run with cairo_nested_scene, because in GL __init__ does not build and does not accept the CONFIG values as kwargs.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject


# ----- From _2018/lost_lecture.py -----

class ShowEmergingEllipse(Scene):
    CONFIG = {
        "circle_radius": 3,
        "circle_color": BLUE,
        "num_lines": 150,
        "lines_stroke_width": 1,
        "eccentricity_vector": 2 * RIGHT,
        "ghost_lines_stroke_color": GREY_B,
        "ghost_lines_stroke_width": 0.5,
        "ellipse_color": PINK,
    }

    def construct(self):
        circle = self.get_circle()
        e_point = self.get_eccentricity_point()
        e_dot = Dot(e_point, color=YELLOW)
        lines = self.get_lines()
        ellipse = self.get_ellipse()

        fade_rect = FullScreenFadeRectangle()

        line = lines[len(lines) // 5]
        line_dot = Dot(line.get_center(), color=YELLOW)
        line_dot.scale(0.5)

        ghost_line = self.get_ghost_lines(line)
        ghost_lines = self.get_ghost_lines(lines)

        rot_words = OldTexText("Rotate $90^\\circ$ \\\\ about center")
        rot_words.next_to(line_dot, RIGHT)

        elbow = self.get_elbow(line)

        eccentric_words = OldTexText("``Eccentric'' point")
        eccentric_words.next_to(circle.get_center(), DOWN)

        ellipse_words = OldTexText("Perfect ellipse")
        ellipse_words.next_to(ellipse, UP, SMALL_BUFF)

        for text in rot_words, ellipse_words:
            text.add_to_back(text.copy().set_stroke(BLACK, 5))

        shuffled_lines = VGroup(*lines)
        random.shuffle(shuffled_lines.submobjects)

        self.play(ShowCreation(circle))
        self.play(
            FadeIn(e_dot, LEFT),
            Write(eccentric_words, run_time=1)
        )
        self.wait()
        self.play(
            LaggedStartMap(ShowCreation, shuffled_lines),
            Animation(VGroup(e_dot, circle)),
            FadeOut(eccentric_words)
        )
        self.add(ghost_lines)
        self.add(e_dot, circle)
        self.wait()
        self.play(
            FadeIn(fade_rect),
            Animation(line),
            GrowFromCenter(line_dot),
            FadeInFromDown(rot_words),
        )
        self.wait()
        self.add(ghost_line)
        self.play(
            MoveToTarget(line, path_arc=90 * DEGREES),
            Animation(rot_words),
            ShowCreation(elbow)
        )
        self.wait()
        self.play(
            FadeOut(fade_rect),
            FadeOut(line_dot),
            FadeOut(rot_words),
            FadeOut(elbow),
            Animation(line),
            Animation(ghost_line)
        )
        self.play(
            LaggedStartMap(MoveToTarget, lines, run_time=4),
            Animation(VGroup(e_dot, circle))
        )
        self.wait()
        self.play(
            ShowCreation(ellipse),
            FadeInFromDown(ellipse_words)
        )
        self.wait()

    def get_circle(self):
        circle = self.circle = Circle(
            radius=self.circle_radius,
            color=self.circle_color
        )
        return circle

    def get_eccentricity_point(self):
        return self.circle.get_center() + self.eccentricity_vector

    def get_lines(self):
        center = self.circle.get_center()
        radius = self.circle.get_width() / 2
        e_point = self.get_eccentricity_point()
        lines = VGroup(*[
            Line(
                e_point,
                center + rotate_vector(radius * RIGHT, angle)
            )
            for angle in np.linspace(0, TAU, self.num_lines)
        ])
        lines.set_stroke(width=self.lines_stroke_width)
        for line in lines:
            line.generate_target()
            line.target.rotate(90 * DEGREES)
        return lines

    def get_ghost_lines(self, lines):
        return lines.copy().set_stroke(
            color=self.ghost_lines_stroke_color,
            width=self.ghost_lines_stroke_width
        )

    def get_elbow(self, line):
        elbow = VGroup(Line(UP, UL), Line(UL, LEFT))
        elbow.set_stroke(width=1)
        elbow.scale(0.2, about_point=ORIGIN)
        elbow.rotate(
            line.get_angle() - 90 * DEGREES,
            about_point=ORIGIN
        )
        elbow.shift(line.get_center())
        return elbow

    def get_ellipse(self):
        center = self.circle.get_center()
        e_point = self.get_eccentricity_point()
        radius = self.circle.get_width() / 2

        # Ellipse parameters
        a = radius / 2
        c = get_norm(e_point - center) / 2
        b = np.sqrt(a**2 - c**2)

        result = Circle(radius=b, color=self.ellipse_color)
        result.stretch(a / b, 0)
        result.move_to(Line(center, e_point))
        return result


class Thumbnail(ShowEmergingEllipse):
    CONFIG = {
        "num_lines": 50,
    }

    def construct(self):
        background = ImageMobject("Feynman_teaching")
        background.set_width(FRAME_WIDTH)
        background.scale(1.05)
        background.to_corner(UR, buff=0)
        background.shift(2 * UP)

        self.add(background)

        circle = self.get_circle()
        circle.set_stroke(width=6)
        circle.set_height(6.5)
        circle.to_corner(UL)
        circle.set_fill(BLACK, 0.9)
        lines = self.get_lines()
        lines.set_stroke(YELLOW, 5)
        lines.set_color_by_gradient(YELLOW, RED)
        ghost_lines = self.get_ghost_lines(lines)
        for line in lines:
            line.rotate(90 * DEGREES)
        ellipse = self.get_ellipse()
        ellipse.set_stroke(BLUE, 6)
        sun = ImageMobject("sun", height=0.5)
        sun.move_to(self.get_eccentricity_point())

        circle_group = VGroup(circle, ghost_lines, lines, ellipse, sun)
        self.add(circle_group)

        l1 = Line(
            circle.point_from_proportion(0.175),
            6.25 * RIGHT + 0.75 * DOWN
        )
        l2 = Line(
            circle.point_from_proportion(0.75),
            6.25 * RIGHT + 2.5 * DOWN
        )
        l2a = VMobject().pointwise_become_partial(l2, 0, 0.56)
        l2b = VMobject().pointwise_become_partial(l2, 0.715, 1)
        expand_lines = VGroup(l1, l2a, l2b)

        expand_lines.set_stroke("RED", 5)
        self.add(expand_lines)
        self.add(circle_group)

        small_group = circle_group.copy()
        small_group.scale(0.2)
        small_group.stretch(1.35, 1)
        small_group.move_to(6.2 * RIGHT + 1.6 * DOWN)
        for mob in small_group:
            if isinstance(mob, VMobject) and mob.get_stroke_width() > 1:
                mob.set_stroke(width=1)
        small_group[0].set_fill(opacity=0.25)
        self.add(small_group)

        title = OldTexText(
            "Feynman's \\\\", "Lost \\\\", "Lecture",
            alignment=""
        )
        title.scale(2.4)
        for part in title:
            part.add_to_back(
                part.copy().set_stroke(BLACK, 12).set_fill(BLACK, 1)
            )
        title.to_corner(UR)
        title[2].to_edge(RIGHT)
        title[1].shift(0.9 * RIGHT)
        title.shift(0.5 * LEFT)
        self.add(title)



# ----- From _2019/clacks/solution2/mirror_scenes.py -----

class MirrorScene(Scene):
    CONFIG = {
        "center": DOWN + 3 * LEFT,
        "line_length": FRAME_WIDTH,
        "start_theta": np.arctan(0.25),
        "start_y_offset": 0.5,
        "start_x_offset": 8,
        "arc_config": {
            "radius": 1,
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "trajectory_point_spacing": 0.1,
        "trajectory_style": {
            "stroke_color": YELLOW,
            "stroke_width": 2,
        },
        "ghost_lines_style": {
            "stroke_color": WHITE,
            "stroke_width": 1,
            "stroke_opacity": 0.5,
        },
        # "reflect_sound": "ping",
        "reflect_sound": "pen_click",
    }

    def setup(self):
        self.theta_tracker = ValueTracker(self.start_theta)
        self.start_y_offset_tracker = ValueTracker(self.start_y_offset)
        self.start_x_offset_tracker = ValueTracker(self.start_x_offset)
        self.center_tracker = VectorizedPoint(self.center)
        self.beam_point = VectorizedPoint(np.array([
            self.get_start_x_offset(),
            self.get_start_y_offset(),
            0
        ]))
        self.ghost_beam_point = self.beam_point.copy()
        self.is_sound_allowed = False

        self.mirrors = self.get_mirrors()
        self.arc = self.get_arc()
        self.theta_symbol = self.get_theta_symbol()
        self.trajectory = self.get_trajectory()
        self.ghost_trajectory = self.get_ghost_trajectory()
        self.theta_display = self.get_theta_display()
        self.count_display_word = self.get_count_display_word()
        self.count_display_number = self.get_count_display_number()
        self.last_count = self.get_count()

        # Add some of them
        self.add(
            self.mirrors,
            self.arc,
            self.theta_symbol,
            self.theta_display,
            self.count_display_word,
            self.count_display_number,
        )

    def get_center(self):
        return self.center_tracker.get_location()

    def get_theta(self):
        return self.theta_tracker.get_value()

    def get_start_y_offset(self):
        return self.start_y_offset_tracker.get_value()

    def get_start_x_offset(self):
        return self.start_x_offset_tracker.get_value()

    def get_mirror(self):
        mirror = VGroup(
            Line(ORIGIN, 2 * RIGHT),
            Line(ORIGIN, 2 * RIGHT),
            Line(ORIGIN, (self.line_length - 4) * RIGHT),
        )
        mirror.arrange(RIGHT, buff=0)
        mirror.set_stroke(width=5)
        mirror[0::2].set_stroke((WHITE, GREY))
        mirror[1::2].set_stroke((GREY, WHITE))
        return mirror

    def get_mirrors(self):
        mirrors = VGroup(self.get_mirror(), self.get_mirror())

        def update_mirrors(mirrors):
            m1, m2 = mirrors
            center = self.get_center()
            theta = self.get_theta()
            m1.move_to(center, DL)
            m2.become(m1)
            m2.rotate(theta, about_point=center)

        mirrors.add_updater(update_mirrors)
        return mirrors

    def get_arc(self, radius=0.5):
        return always_redraw(lambda: Arc(
            start_angle=0,
            angle=self.get_theta(),
            arc_center=self.get_center(),
            **self.arc_config,
        ))

    def get_theta_symbol(self, arc=None, buff=0.15):
        if arc is None:
            arc = self.arc
        symbol = OldTex("\\theta")

        def update_symbol(symbol):
            midpoint = arc.point_from_proportion(0.5)
            center = arc.arc_center
            vect = (midpoint - center)
            max_height = 0.8 * arc.get_height()
            if symbol.get_height() > max_height:
                symbol.set_height(max_height)
            symbol.move_to(
                center + vect + buff * normalize(vect)
            )
        symbol.add_updater(update_symbol)
        return symbol

    def get_ghost_collision_points(self):
        x = self.get_start_x_offset()
        y = self.get_start_y_offset()
        theta = self.get_theta()

        points = [np.array([x, y, 0])]
        points += [
            np.array([x, y, 0])
            for k in range(1, int(PI / theta) + 1)
            for x in [y / np.tan(k * theta)]
            if abs(x) < FRAME_WIDTH
        ]
        points.append(points[-1] + x * LEFT)
        points = np.array(points)
        points += self.get_center()
        return points

    def get_collision_points(self, ghost_points=None):
        if ghost_points is None:
            ghost_points = self.get_ghost_collision_points()
        theta = self.get_theta()
        center = self.get_center()
        points = []
        for ghost_point in ghost_points:
            vect = ghost_point - center
            angle = angle_of_vector(vect)
            k = int(angle / theta)
            if k % 2 == 0:
                vect = rotate_vector(vect, -k * theta)
            else:
                vect = rotate_vector(vect, -(k + 1) * theta)
                vect[1] = abs(vect[1])
            points.append(center + vect)
        return points

    def get_trajectory(self, collision_points=None):
        if collision_points is None:
            collision_points = self.get_collision_points()
        points = []
        spacing = self.trajectory_point_spacing
        for p0, p1 in zip(collision_points, collision_points[1:]):
            n_intervals = max(1, int(get_norm(p1 - p0) / spacing))
            for alpha in np.linspace(0, 1, n_intervals + 1):
                points.append(interpolate(p0, p1, alpha))
        trajectory = VMobject()
        trajectory.set_points_as_corners(points)
        trajectory.set_style(**self.trajectory_style)
        return trajectory

    def get_ghost_trajectory(self):
        return self.get_trajectory(self.get_ghost_collision_points())

    def get_collision_point_counts(self, collision_points=None):
        if collision_points is None:
            collision_points = self.get_collision_points()[1:-1]
        result = VGroup()
        for n, point in enumerate(collision_points):
            count = Integer(n + 1)
            count.set_height(0.25)
            vect = UP if n % 2 == 0 else DOWN
            count.next_to(point, vect, SMALL_BUFF)
            result.add(count)
        return result

    def get_collision_count_anim(self, collision_point_counts=None):
        if collision_point_counts is None:
            collision_point_counts = self.get_collision_point_counts()
        group = VGroup()

        def update(group):
            count = self.get_count()
            if count == 0:
                group.submobjects = []
            elif count < len(collision_point_counts) + 1:
                group.submobjects = [
                    collision_point_counts[count - 1]
                ]

        return UpdateFromFunc(group, update, remover=True)

    def get_ghost_lines(self):
        line = self.mirrors[0]
        center = self.get_center()
        theta = self.get_theta()
        lines = VGroup()
        for k in range(1, int(PI / theta) + 2):
            new_line = line.copy()
            new_line.rotate(k * theta, about_point=center)
            lines.add(new_line)
        lines.set_style(**self.ghost_lines_style)
        return lines

    # Displays
    def get_theta_display(self):
        lhs = OldTex("\\theta = ")
        radians = DecimalNumber()
        radians.add_updater(
            lambda m: m.set_value(self.get_theta())
        )
        radians_word = OldTexText("radians")
        radians_word.next_to(
            radians, RIGHT, aligned_edge=DOWN
        )
        equals = OldTex("=")
        degrees = Integer(0, unit="^\\circ")
        degrees.add_updater(
            lambda m: m.set_value(
                int(np.round(self.get_theta() / DEGREES))
            )
        )
        group = VGroup(lhs, radians, radians_word, equals, degrees)
        group.arrange(RIGHT, aligned_edge=DOWN)
        equals.align_to(lhs[-1], DOWN)
        group.to_corner(UL)
        return group

    def get_count_display_word(self):
        result = OldTexText("\\# Bounces: ")
        result.to_corner(UL)
        result.shift(DOWN)
        result.set_color(YELLOW)
        return result

    def get_count_display_number(self, count_display_word=None, ghost_beam_point=None):
        if count_display_word is None:
            count_display_word = self.count_display_word
        result = Integer()
        result.next_to(
            count_display_word[-1], RIGHT,
            aligned_edge=DOWN,
        )
        result.set_color(YELLOW)
        result.add_updater(
            lambda m: m.set_value(self.get_count())
        )
        return result

    def get_count(self, ghost_beam_point=None):
        if ghost_beam_point is None:
            ghost_beam_point = self.ghost_beam_point.get_location()
        angle = angle_of_vector(
            ghost_beam_point - self.get_center()
        )
        return int(angle / self.get_theta())

    # Sounds
    def allow_sound(self):
        self.is_sound_allowed = True

    def disallow_sound(self):
        self.is_sound_allowed = False

    def update_mobjects(self, dt):
        super().update_mobjects(dt)
        if self.get_count() != self.last_count:
            self.last_count = self.get_count()
            if self.is_sound_allowed:
                self.add_sound(
                    self.reflect_sound,
                    gain=-20,
                )

    # Bouncing animations
    def show_bouncing(self, run_time=5):
        trajectory = self.trajectory
        ghost_trajectory = self.get_ghost_trajectory()

        beam_anims = self.get_shooting_beam_anims(
            trajectory, ghost_trajectory
        )
        count_anim = self.get_collision_count_anim()

        self.allow_sound()
        self.play(count_anim, *beam_anims, run_time=run_time)
        self.disallow_sound()

    def get_special_flash(self, mobject, stroke_width, time_width, rate_func=linear, **kwargs):
        kwargs["rate_func"] = rate_func
        mob_copy = mobject.copy()
        mob_copy.set_stroke(width=stroke_width)
        mob_copy.time_width = time_width
        return UpdateFromAlphaFunc(
            mob_copy,
            lambda m, a: m.pointwise_become_partial(
                mobject,
                max(a - (1 - a) * m.time_width, 0),
                a,
            ),
            **kwargs
        )

    def get_shooting_beam_anims(self,
                                trajectory,
                                ghost_trajectory=None,
                                update_beam_point=True,
                                num_flashes=20,
                                min_time_width=0.01,
                                max_time_width=0.5,
                                min_stroke_width=0.01,
                                max_stroke_width=6,
                                fade_trajectory=True,
                                faded_trajectory_width=0.25,
                                faded_trajectory_time_exp=0.2,
                                ):
        # Most flashes
        result = [
            self.get_special_flash(trajectory, stroke_width, time_width)
            for stroke_width, time_width in zip(
                np.linspace(max_stroke_width, min_stroke_width, num_flashes),
                np.linspace(min_time_width, max_time_width, num_flashes),
            )
        ]

        # Make sure beam point is updated
        if update_beam_point:
            smallest_flash = result[0]
            result.append(
                UpdateFromFunc(
                    self.beam_point,
                    lambda m: m.move_to(smallest_flash.mobject.get_points()[-1])
                )
            )

        # Make sure ghost beam point is updated
        if ghost_trajectory:
            ghost_flash = self.get_special_flash(
                ghost_trajectory, 0, min_time_width,
            )
            ghost_beam_point_update = UpdateFromFunc(
                self.ghost_beam_point,
                lambda m: m.move_to(ghost_flash.mobject.get_points()[-1])
            )
            result += [
                ghost_flash,
                ghost_beam_point_update,
            ]

        # Fade trajectory
        if fade_trajectory:
            ftte = faded_trajectory_time_exp
            result.append(
                ApplyMethod(
                    trajectory.set_stroke,
                    {"width": faded_trajectory_width},
                    rate_func=lambda t: there_and_back(t)**ftte
                ),
            )
        return result


class ReflectWorldThroughMirrorNew(MirrorScene):
    CONFIG = {
        "start_y_offset": 1.25,
        "center": DOWN,
        "randy_height": 1,
        "partial_trajectory_values": [
            0, 0.22, 0.28, 0.315, 1,
        ],
    }

    def construct(self):
        self.add_randy()
        self.shift_displays()
        self.add_ghost_beam_point()
        self.up_through_first_bounce()
        self.create_reflected_worlds()
        self.create_reflected_trajectories()
        self.first_reflection()
        self.next_reflection(2)
        self.next_reflection(3)
        self.unfold_all_reflected_worlds()
        self.show_completed_beam()
        self.blink_all_randys()
        self.add_randy_updates()
        self.show_all_trajectories()
        self.focus_on_two_important_trajectories()

    def add_randy(self):
        randy = self.randy = Randolph()
        randy.flip()
        randy.set_height(self.randy_height)
        randy.change("pondering")
        randy.align_to(self.mirrors, DOWN)
        randy.shift(0.01 * UP)
        randy.to_edge(RIGHT, buff=1)
        randy.tracked_mobject = self.trajectory
        randy.add_updater(
            lambda m: m.look_at(
                m.tracked_mobject.get_points()[-1]
            )
        )
        self.add(randy)

    def shift_displays(self):
        VGroup(
            self.theta_display,
            self.count_display_word,
            self.count_display_number,
        ).to_edge(DOWN)

    def add_ghost_beam_point(self):
        self.ghost_beam_point.add_updater(
            lambda m: m.move_to(
                self.ghost_trajectory.get_points()[-1]
            )
        )
        self.add(self.ghost_beam_point)

    def up_through_first_bounce(self):
        self.play(*self.get_both_partial_trajectory_anims(
            *self.partial_trajectory_values[:2]
        ))
        self.wait()

    def create_reflected_worlds(self):
        mirrors = self.mirrors
        triangle = Polygon(*[
            mirrors.get_corner(corner)
            for corner in (DR, DL, UR)
        ])
        triangle.set_stroke(width=0)
        triangle.set_fill(BLUE_E, opacity=0)
        world = self.world = VGroup(
            triangle,
            mirrors,
            self.arc,
            self.theta_symbol,
            self.randy,
        )
        reflected_worlds = self.get_reflected_worlds(world)
        self.reflected_worlds = reflected_worlds
        # Alternating triangle opacities
        for rw in reflected_worlds[::2]:
            rw[0].set_fill(opacity=0.25)

    def create_reflected_trajectories(self):
        self.reflected_trajectories = always_redraw(
            lambda: self.get_reflected_worlds(self.trajectory)
        )

    def first_reflection(self):
        reflected_trajectory = self.reflected_trajectories[0]
        reflected_world = self.reflected_worlds[0]
        world = self.world
        trajectory = self.trajectory
        ghost_trajectory = self.ghost_trajectory

        self.play(
            TransformFromCopy(world, reflected_world),
            TransformFromCopy(trajectory, reflected_trajectory),
            run_time=2
        )
        beam_anims = self.get_shooting_beam_anims(
            ghost_trajectory,
            fade_trajectory=False,
        )
        self.play(
            *[
                ApplyMethod(m.set_stroke, GREY, 1)
                for m in (trajectory, reflected_trajectory)
            ] + beam_anims,
            run_time=2
        )
        for x in range(2):
            self.play(*beam_anims, run_time=2)

        ghost_trajectory.set_stroke(YELLOW, 4)
        self.bring_to_front(ghost_trajectory)
        self.play(FadeIn(ghost_trajectory))
        self.wait()

    def next_reflection(self, index=2):
        i = index
        self.play(
            *self.get_both_partial_trajectory_anims(
                *self.partial_trajectory_values[i - 1:i + 1]
            ),
            UpdateFromFunc(
                VMobject(),  # Null
                lambda m: self.reflected_trajectories.update(),
                remover=True,
            ),
        )

        anims = [
            TransformFromCopy(*reflections[i - 2:i])
            for reflections in [
                self.reflected_worlds,
                self.reflected_trajectories
            ]
        ]
        self.play(*anims, run_time=2)
        self.add(self.ghost_trajectory)
        self.wait()

    def unfold_all_reflected_worlds(self):
        worlds = self.reflected_worlds
        trajectories = self.reflected_trajectories

        pairs = [
            (VGroup(w1, t1), VGroup(w2, t2))
            for w1, w2, t1, t2 in zip(
                worlds[2:], worlds[3:],
                trajectories[2:], trajectories[3:],
            )
        ]

        new_worlds = VGroup()  # Brought to you by Dvorak
        for m1, m2 in pairs:
            m2.pre_world = m1.copy()
            new_worlds.add(m2)
        for mob in new_worlds:
            mob.save_state()
            mob.become(mob.pre_world)
            mob.fade(1)

        self.play(LaggedStartMap(
            Restore, new_worlds,
            lag_ratio=0.4,
            run_time=3
        ))

    def show_completed_beam(self):
        self.add(self.reflected_trajectories)
        self.add(self.ghost_trajectory)
        self.play(*self.get_both_partial_trajectory_anims(
            *self.partial_trajectory_values[-2:],
            run_time=7
        ))

    def blink_all_randys(self):
        randys = self.randys = VGroup(self.randy)
        randys.add(*[rw[-1] for rw in self.reflected_worlds])
        self.play(LaggedStartMap(Blink, randys))

    def add_randy_updates(self):
        # Makes it run slower, but it's fun!
        reflected_randys = VGroup(*[
            rw[-1] for rw in self.reflected_worlds
        ])
        reflected_randys.add_updater(
            lambda m: m.become(
                self.get_reflected_worlds(self.randy)
            )
        )
        self.add(reflected_randys)

    def show_all_trajectories(self):
        ghost_trajectory = self.ghost_trajectory
        reflected_trajectories = self.reflected_trajectories
        trajectory = self.trajectory
        reflected_trajectories.suspend_updating()
        trajectories = VGroup(trajectory, *reflected_trajectories)

        all_mirrors = VGroup(*[
            world[1]
            for world in it.chain([self.world], self.reflected_worlds)
        ])

        self.play(
            FadeOut(ghost_trajectory),
            trajectories.set_stroke, YELLOW, 0.5,
            all_mirrors.set_stroke, {"width": 1},
        )

        # All trajectory light beams
        flash_groups = [
            self.get_shooting_beam_anims(
                mob, fade_trajectory=False,
            )
            for mob in trajectories
        ]
        all_flashes = list(it.chain(*flash_groups))

        # Have all the pi creature eyes follows
        self.randy.tracked_mobject = all_flashes[0].mobject

        # Highlight the illustory straight beam
        red_ghost = self.ghost_trajectory.copy()
        red_ghost.set_color(RED)
        red_ghost_beam = self.get_shooting_beam_anims(
            red_ghost, fade_trajectory=False,
        )

        num_repeats = 3
        for x in range(num_repeats):
            anims = list(all_flashes)
            if x == num_repeats - 1:
                anims += list(red_ghost_beam)
                self.randy.tracked_mobject = red_ghost_beam[0].mobject
                for flash in all_flashes:
                    if hasattr(flash.mobject, "time_width"):
                        flash.mobject.set_stroke(
                            width=0.25 * flash.mobject.get_stroke_width()
                        )
                        flash.mobject.time_width *= 0.25
            self.play(*anims, run_time=3)

    def focus_on_two_important_trajectories(self):
        self.ghost_trajectory.set_stroke(YELLOW, 1)
        self.play(
            FadeOut(self.reflected_trajectories),
            FadeIn(self.ghost_trajectory),
            self.trajectory.set_stroke, YELLOW, 1,
        )
        self.add_flashing_windows()
        t_beam_anims = self.get_shooting_beam_anims(self.trajectory)
        gt_beam_anims = self.get_shooting_beam_anims(self.ghost_trajectory)
        self.ghost_beam_point.clear_updaters()
        self.ghost_beam_point.add_updater(
            lambda m: m.move_to(
                gt_beam_anims[0].mobject.get_points()[-1]
            )
        )
        self.randy.tracked_mobject = t_beam_anims[0].mobject
        self.allow_sound()
        self.play(
            *t_beam_anims, *gt_beam_anims,
            run_time=6
        )
        self.add_room_color_updates()
        self.play(
            *t_beam_anims, *gt_beam_anims,
            run_time=6
        )
        self.blink_all_randys()
        self.play(
            *t_beam_anims, *gt_beam_anims,
            run_time=6
        )

    # Helpers
    def get_reflected_worlds(self, world, n_reflections=None):
        theta = self.get_theta()
        center = self.get_center()
        if n_reflections is None:
            n_reflections = int(PI / theta)

        result = VGroup()
        last_world = world
        for n in range(n_reflections):
            vect = rotate_vector(RIGHT, (n + 1) * theta)
            reflected_world = last_world.copy()
            reflected_world.clear_updaters()
            reflected_world.rotate(
                PI, axis=vect, about_point=center,
            )
            last_world = reflected_world
            result.add(last_world)
        return result

    def get_partial_trajectory_anims(self, trajectory, a, b, **kwargs):
        if not hasattr(trajectory, "full_self"):
            trajectory.full_self = trajectory.copy()
        return UpdateFromAlphaFunc(
            trajectory,
            lambda m, alpha: m.pointwise_become_partial(
                m.full_self, 0,
                interpolate(a, b, alpha)
            ),
            **kwargs
        )

    def get_both_partial_trajectory_anims(self, a, b, run_time=2, **kwargs):
        kwargs["run_time"] = run_time
        return [
            self.get_partial_trajectory_anims(
                mob, a, b, **kwargs
            )
            for mob in (self.trajectory, self.ghost_trajectory)
        ]

    def add_flashing_windows(self):
        theta = self.get_theta()
        center = self.get_center()
        windows = self.windows = VGroup(*[
            Line(
                center,
                center + rotate_vector(10 * RIGHT, k * theta),
                color=BLUE,
                stroke_width=0,
            )
            for k in range(0, self.get_count() + 1)
        ])
        windows[0].set_stroke(opacity=0)

        # Warning, windows update manager may launch
        def update_windows(windows):
            windows.set_stroke(width=0)
            windows[self.get_count()].set_stroke(width=5)
        windows.add_updater(update_windows)
        self.add(windows)

    def add_room_color_updates(self):
        def update_reflected_worlds(worlds):
            for n, world in enumerate(worlds):
                worlds[n][0].set_fill(
                    opacity=(0.25 if (n % 2 == 0) else 0)
                )
            index = self.get_count() - 1
            if index < 0:
                return
            worlds[index][0].set_fill(opacity=0.5)
        self.reflected_worlds.add_updater(update_reflected_worlds)
        self.add(self.reflected_worlds)



# ----- From _2019/clacks/question.py -----

class Block(Square):
    CONFIG = {
        "mass": 1,
        "velocity": 0,
        "width": None,
        "label_text": None,
        "label_scale_value": 0.8,
        "fill_opacity": 1,
        "stroke_width": 3,
        "stroke_color": WHITE,
        "fill_color": None,
        "sheen_direction": UL,
        "sheen_factor": 0.5,
        "sheen_direction": UL,
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        if self.width is None:
            self.width = self.mass_to_width(self.mass)
        if self.fill_color is None:
            self.fill_color = self.mass_to_color(self.mass)
        if self.label_text is None:
            self.label_text = self.mass_to_label_text(self.mass)
        if "width" in kwargs:
            kwargs.pop("width")
        # CHANGE: keep the CONFIG style computed before the defaults of Square replace it.
        for key in ('fill_opacity', 'fill_color', 'stroke_width', 'stroke_color'):
            kwargs.setdefault(key, getattr(self, key))
        Square.__init__(self, side_length=self.width, **kwargs)
        self.label = self.get_label()
        self.add(self.label)

    def get_label(self):
        label = OldTexText(self.label_text)
        label.scale(self.label_scale_value)
        label.next_to(self, UP, SMALL_BUFF)
        return label

    def get_points_defining_boundary(self):
        return self.get_points()

    def mass_to_color(self, mass):
        colors = [
            GREY_B,
            BLUE_D,
            BLUE_D,
            BLUE_E,
            BLUE_E,
            GREY_D,
            GREY_D,
            BLACK,
        ]
        index = min(int(np.log10(mass)), len(colors) - 1)
        return colors[index]

    def mass_to_width(self, mass):
        return 1 + 0.25 * np.log10(mass)

    def mass_to_label_text(self, mass):
        return "{:,}\\,kg".format(int(mass))


class SlidingBlocks(VGroup):
    CONFIG = {
        "block1_config": {
            "distance": 7,
            "mass": 1e6,
            "velocity": -2,
        },
        "block2_config": {
            "distance": 3,
            "mass": 1,
            "velocity": 0,
        },
        "collect_clack_data": True,
    }

    def __init__(self, scene, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.scene = scene
        self.floor = scene.floor
        self.wall = scene.wall

        self.block1 = self.get_block(**self.block1_config)
        self.block2 = self.get_block(**self.block2_config)
        self.mass_ratio = self.block2.mass / self.block1.mass
        self.phase_space_point_tracker = self.get_phase_space_point_tracker()
        self.add(
            self.block1, self.block2,
            self.phase_space_point_tracker,
        )
        self.add_updater(self.__class__.update_positions)

        if self.collect_clack_data:
            self.clack_data = self.get_clack_data()

    def get_block(self, distance, **kwargs):
        block = Block(**kwargs)
        block.move_to(
            self.floor.get_top()[1] * UP +
            (self.wall.get_right()[0] + distance) * RIGHT,
            DL,
        )
        return block

    def get_phase_space_point_tracker(self):
        block1, block2 = self.block1, self.block2
        w2 = block2.get_width()
        s1 = block1.get_left()[0] - self.wall.get_right()[0] - w2
        s2 = block2.get_right()[0] - self.wall.get_right()[0] - w2
        result = VectorizedPoint([
            s1 * np.sqrt(block1.mass),
            s2 * np.sqrt(block2.mass),
            0
        ])

        result.velocity = np.array([
            np.sqrt(block1.mass) * block1.velocity,
            np.sqrt(block2.mass) * block2.velocity,
            0
        ])
        return result

    def update_positions(self, dt):
        self.phase_space_point_tracker.shift(
            self.phase_space_point_tracker.velocity * dt
        )
        self.update_blocks_from_phase_space_point_tracker()

    def update_blocks_from_phase_space_point_tracker(self):
        block1, block2 = self.block1, self.block2
        ps_point = self.phase_space_point_tracker.get_location()

        theta = np.arctan(np.sqrt(self.mass_ratio))
        ps_point_angle = angle_of_vector(ps_point)
        n_clacks = int(ps_point_angle / theta)
        reflected_point = rotate_vector(
            ps_point,
            -2 * np.ceil(n_clacks / 2) * theta
        )
        reflected_point = np.abs(reflected_point)

        shadow_wall_x = self.wall.get_right()[0] + block2.get_width()
        floor_y = self.floor.get_top()[1]
        s1 = reflected_point[0] / np.sqrt(block1.mass)
        s2 = reflected_point[1] / np.sqrt(block2.mass)
        block1.move_to(
            (shadow_wall_x + s1) * RIGHT +
            floor_y * UP,
            DL,
        )
        block2.move_to(
            (shadow_wall_x + s2) * RIGHT +
            floor_y * UP,
            DR,
        )

        self.scene.update_num_clacks(n_clacks)

    def get_clack_data(self):
        ps_point = self.phase_space_point_tracker.get_location()
        ps_velocity = self.phase_space_point_tracker.velocity
        if ps_velocity[1] != 0:
            raise Exception(
                "Haven't implemented anything to gather clack "
                "data from a start state with block2 moving"
            )
        y = ps_point[1]
        theta = np.arctan(np.sqrt(self.mass_ratio))

        clack_data = []
        for k in range(1, int(PI / theta) + 1):
            clack_ps_point = np.array([
                y / np.tan(k * theta),
                y,
                0
            ])
            time = get_norm(ps_point - clack_ps_point) / get_norm(ps_velocity)
            reflected_point = rotate_vector(
                clack_ps_point,
                -2 * np.ceil((k - 1) / 2) * theta
            )
            block2 = self.block2
            s2 = reflected_point[1] / np.sqrt(block2.mass)
            location = np.array([
                self.wall.get_right()[0] + s2,
                block2.get_center()[1],
                0
            ])
            if k % 2 == 1:
                location += block2.get_width() * RIGHT
            clack_data.append((location, time))
        return clack_data


# TODO, this is untested after turning it from a
# ContinualAnimation into a VGroup
class ClackFlashes(VGroup):
    CONFIG = {
        "flash_config": {
            "run_time": 0.5,
            "line_length": 0.1,
            "flash_radius": 0.2,
        },
        "start_up_time": 0,
        "min_time_between_flashes": 1 / 30,
    }

    def __init__(self, clack_data, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.flashes = []
        last_time = 0
        for location, time in clack_data:
            if (time - last_time) < self.min_time_between_flashes:
                continue
            last_time = time
            flash = Flash(location, **self.flash_config)
            flash.begin()
            for sm in flash.mobject.family_members_with_points():
                if isinstance(sm, VMobject):
                    sm.set_stroke(YELLOW, 3)
                    sm.set_stroke(WHITE, 6, 0.5, background=True)
            flash.start_time = time
            flash.end_time = time + flash.run_time
            self.flashes.append(flash)

        self.time = 0
        # CHANGE: receive dt and use an updater, keeping Mobject.update and its children.
        self.add_updater(lambda m, dt: m.update_flashes(dt))

    # CHANGE: update is now the Mobject API; separate the logic of the flashes.
    def update_flashes(self, dt):
        time = self.time
        self.time += dt
        for flash in self.flashes:
            if flash.start_time < time < flash.end_time:
                if flash.mobject not in self.submobjects:
                    self.add(flash.mobject)
                # CHANGE: Animation.update was renamed to interpolate.
                flash.interpolate(
                    (time - flash.start_time) / flash.run_time
                )
            else:
                if flash.mobject in self.submobjects:
                    self.remove(flash.mobject)


class Wall(Line):
    CONFIG = {
        "tick_spacing": 0.5,
        "tick_length": 0.25,
        "tick_style": {
            "stroke_width": 1,
            "stroke_color": WHITE,
        },
    }

    def __init__(self, height, **kwargs):
        Line.__init__(self, ORIGIN, height * UP, **kwargs)
        self.height = height
        self.ticks = self.get_ticks()
        self.add(self.ticks)

    def get_ticks(self):
        n_lines = int(self.height / self.tick_spacing)
        lines = VGroup(*[
            Line(ORIGIN, self.tick_length * UR).shift(n * self.tick_spacing * UP)
            for n in range(n_lines)
        ])
        lines.set_style(**self.tick_style)
        lines.move_to(self, DR)
        return lines


class BlocksAndWallScene(Scene):
    CONFIG = {
        "include_sound": True,
        "collision_sound": "clack.wav",
        "count_clacks": True,
        "counter_group_shift_vect": LEFT,
        "sliding_blocks_config": {},
        "floor_y": -2,
        "wall_x": -6,
        "n_wall_ticks": 15,
        "counter_label": "\\# Collisions: ",
        "show_flash_animations": True,
        "min_time_between_sounds": 0.004,
    }

    def setup(self):
        self.track_time()
        self.add_floor_and_wall()
        self.add_blocks()
        if self.show_flash_animations:
            self.add_flash_animations()

        if self.count_clacks:
            self.add_counter()

    def add_floor_and_wall(self):
        self.floor = self.get_floor()
        self.wall = self.get_wall()
        self.add(self.floor, self.wall)

    def add_blocks(self):
        self.blocks = SlidingBlocks(self, **self.sliding_blocks_config)
        if hasattr(self.blocks, "clack_data"):
            self.clack_data = self.blocks.clack_data
        self.add(self.blocks)

    def add_flash_animations(self):
        self.clack_flashes = ClackFlashes(self.clack_data)
        self.add(self.clack_flashes)

    def track_time(self):
        time_tracker = ValueTracker()
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(time_tracker)
        self.get_time = time_tracker.get_value

    def add_counter(self):
        self.n_clacks = 0
        counter_label = OldTexText(self.counter_label)
        counter_mob = Integer(self.n_clacks)
        counter_mob.next_to(
            counter_label[-1], RIGHT,
        )
        counter_mob.align_to(counter_label[-1][-1], DOWN)
        counter_group = VGroup(
            counter_label,
            counter_mob,
        )
        counter_group.to_corner(UR)
        counter_group.shift(self.counter_group_shift_vect)
        self.add(counter_group)

        self.counter_mob = counter_mob

    def get_wall(self):
        height = (FRAME_HEIGHT / 2) - self.floor_y
        wall = Wall(height=height)
        wall.shift(self.wall_x * RIGHT)
        wall.to_edge(UP, buff=0)
        return wall

    def get_floor(self):
        floor = Line(self.wall_x * RIGHT, FRAME_WIDTH * RIGHT / 2)
        floor.shift(self.floor_y * UP)
        return floor

    def update_num_clacks(self, n_clacks):
        if hasattr(self, "n_clacks"):
            if n_clacks == self.n_clacks:
                return
            self.counter_mob.set_value(n_clacks)

    def add_clack_sounds(self, clack_data):
        clack_file = self.collision_sound
        total_time = self.get_time()
        times = [
            time
            for location, time in clack_data
            if time < total_time
        ]
        last_time = 0
        for time in times:
            d_time = time - last_time
            if d_time < self.min_time_between_sounds:
                continue
            last_time = time
            self.add_sound(
                clack_file,
                time_offset=(time - total_time),
                gain=-20,
            )
        return self

    def tear_down(self):
        super().tear_down()
        if self.include_sound:
            self.add_clack_sounds(self.clack_data)


class BlocksAndWallExample(BlocksAndWallScene):
    CONFIG = {
        "sliding_blocks_config": {
            "block1_config": {
                "mass": 1e0,
                "velocity": -2,
            }
        },
        "wait_time": 15,
    }

    def construct(self):
        self.wait(self.wait_time)


class Thumbnail(BlocksAndWallExample, MovingCameraScene):
    CONFIG = {
        "sliding_blocks_config": {
            "block1_config": {
                "mass": 1e4,
                "velocity": -1.5,
            },
            "collect_clack_data": False,
        },
        "wait_time": 0,
        "count_clacks": False,
        "show_flash_animations": False,
        "floor_y": -3.0,
        "include_sound": False,
    }

    def setup(self):
        MovingCameraScene.setup(self)
        BlocksAndWallExample.setup(self)

    def construct(self):
        self.camera_frame.shift(0.9 * UP)
        # self.mobjects.insert(
        #     0,
        #     FullScreenFadeRectangle(
        #         color=GREY_D,
        #         opacity=0.5,
        #         sheen_direction=UL,
        #         sheen=0.5,
        #     ),
        # )
        self.thicken_lines()
        self.grow_labels()
        self.add_vector()
        self.add_text()

    def thicken_lines(self):
        self.floor.set_stroke(WHITE, 10)
        self.wall.set_stroke(WHITE, 10)
        self.wall[1:].set_stroke(WHITE, 4)

    def grow_labels(self):
        blocks = self.blocks
        for block in blocks.block1, blocks.block2:
            block.remove(block.label)
            block.label.scale(2.5, about_point=block.get_top())
            self.add(block.label)

    def add_vector(self):
        blocks = self.blocks
        arrow = self.arrow = Vector(
            2.5 * LEFT,
            color=RED,
            rectangular_stem_width=1.5,
            tip_length=0.5
        )
        arrow.move_to(blocks.block1.get_center(), RIGHT)
        arrow.add_to_back(
            arrow.copy().set_stroke(GREY, 5)
        )
        self.add(arrow)

    def add_text(self):
        question = self.question = OldTexText(
            "How many\\\\collisions?"
        )
        question.scale(2.5)
        question.to_edge(UP)
        question.set_color(YELLOW)
        question.set_stroke(RED, 2, background=True)
        self.add(question)



# ----- From _2019/clacks/solution2/simple_scenes.py -----

class ClacksSolution2Thumbnail(Scene):
    def construct(self):
        self.add_scene1()
        self.add_scene2()

        arrow = Arrow(
            self.block_word.get_top(),
            self.light_dot.get_bottom(),
            tip_length=0.75,
            rectangular_stem_width=0.2,
            color=RED,
            buff=0.5,
        )
        arrow.add_to_back(arrow.copy().set_stroke(BLACK, 20))
        self.add(arrow)
        return

        arrow = OldTex("\\Updownarrow")
        arrow.set_height(2)
        arrow.set_color(YELLOW)
        arrow.set_stroke(Color("red"), 2, background=True)
        self.add(arrow)

    def add_scene1(self):
        # CHANGE: in GL __init__ does not build and does not accept the CONFIG values as kwargs; cairo_nested_scene does it like Cairo
        scene1 = cairo_nested_scene(
            Thumbnail,
            sliding_blocks_config={
                "block1_config": {
                    "label_text": "$100^{d}$ kg",
                    "distance": 8,
                },
            }
        )
        group = Group(*scene1.mobjects)
        group.scale(0.75, about_point=ORIGIN)
        group.shift(1.5 * DOWN + 3 * LEFT)
        scene1.remove(scene1.question)
        self.add(*scene1.mobjects)

        black_rect = FullScreenFadeRectangle(fill_opacity=1)
        black_rect.shift(3.5 * UP)
        self.add(black_rect)

        word = OldTexText("Blocks")
        word.set_color(YELLOW)
        word.scale(3)
        word.to_corner(DR, buff=LARGE_BUFF)
        word.shift(0.5 * LEFT)
        self.block_word = word
        self.add(word)

    def add_scene2(self):
        # CHANGE: like scene1, the nested scene is run with cairo_nested_scene
        scene2 = cairo_nested_scene(
            ReflectWorldThroughMirrorNew,
            skip_animations=True,
            file_writer_config={
                "write_to_movie": False,
            },
            end_at_animation_number=18,
            # center=1.5 * DOWN,
            center=ORIGIN,
        )
        worlds = VGroup(scene2.world, *scene2.reflected_worlds)
        mirrors = VGroup(*[rw[1] for rw in worlds])
        mirrors.set_stroke(width=5)
        triangles = VGroup(*[rw[0] for rw in worlds])
        trajectories = VGroup(
            scene2.trajectory,
            *scene2.reflected_trajectories
        )
        trajectories.set_stroke(YELLOW, 1)

        beams1, beams2 = [
            scene2.get_shooting_beam_anims(
                path,
                max_stroke_width=20,
                max_time_width=1,
                num_flashes=50,
            )
            for path in [
                scene2.trajectory,
                scene2.ghost_trajectory,
            ]
        ]
        beams = beams1 + beams2
        beams = beams2
        flashes = VGroup()
        for beam in beams:
            beam.update(0.5)
            flashes.add(beam.mobject)

        dot = self.light_dot = Dot(color=YELLOW, radius=0.1)
        dot.move_to(flashes[0].get_left())
        flashes.add(dot)

        self.add(triangles, mirrors)
        # self.add(randys)
        self.add(trajectories[0].set_stroke(width=2))
        self.add(flashes)

        word = OldTexText("Light beam")
        word.scale(3.5)
        word.set_color(YELLOW)
        # word.set_stroke(BLACK, 25, background=True)
        word.add_to_back(word.copy().set_stroke(
            BLACK, 25,
        ))
        word.next_to(dot, UR)
        word.shift(-word.get_center()[0] * RIGHT)
        word.shift(SMALL_BUFF * RIGHT)
        self.light_word = word
        self.add(word)
