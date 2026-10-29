# ==============================================================================
# Scene:      MirrorAndWiresOverlay
# Source:     videos/_2019/clacks/solution2/mirror_scenes.py (lines 775-1021)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MirrorAndWiresOverlay.py MirrorAndWiresOverlay -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class MirrorAndWiresOverlay(MirrorScene):
    CONFIG = {
        "wire_pixel_points": [
            (355, 574),
            (846, 438),
            (839, 629),
            (845, 288),
            (1273, 314),
        ],
        "max_x_pixel": 1440,
        "max_y_pixel": 1440,
    }

    def setup(self):
        self.last_count = 0

    def get_count(self):
        return 0

    def get_shooting_beam_anims(self, mobject, **new_kwargs):
        kwargs = {
            "update_beam_point": False,
            "fade_trajectory": False,
            "max_stroke_width": 10,
        }
        kwargs.update(new_kwargs)
        return super().get_shooting_beam_anims(mobject, **kwargs)

    def construct(self):
        self.add_wires()
        self.add_diagram()

        self.introduce_wires()
        self.show_illusion()
        self.show_angles()

        # self.show_reflecting_beam()

    def add_wires(self):
        ul_corner = TOP + LEFT_SIDE
        points = self.wire_points = [
            ul_corner + np.array([
                (x / self.max_x_pixel) * FRAME_HEIGHT,
                (-y / self.max_y_pixel) * FRAME_HEIGHT,
                0
            ])
            for x, y in self.wire_pixel_points
        ]
        wires = self.wires = VGroup(
            Line(points[0], points[1]),
            Line(points[1], points[2]),
            Line(points[1], points[3]),
            Line(points[1], points[4]),
        )
        wires.set_stroke(RED, 4)
        self.dl_wire, self.dr_wire, self.ul_wire, self.ur_wire = wires

        self.trajectory = VMobject()
        self.trajectory.set_points_as_corners(points[:3])
        self.ghost_trajectory = VMobject()
        self.ghost_trajectory.set_points_as_corners([*points[:2], points[4]])
        VGroup(self.trajectory, self.ghost_trajectory).match_style(
            self.wires
        )

    def add_diagram(self):
        diagram = self.diagram = VGroup()
        rect = diagram.rect = Rectangle(
            height=4, width=5,
            stroke_color=WHITE,
            stroke_width=1,
            fill_color=BLACK,
            fill_opacity=0.9,
        )
        rect.to_corner(UR)
        diagram.add(rect)

        center = rect.get_center()

        mirror = diagram.mirror = VGroup(
            Line(rect.get_left(), center + 1.5 * LEFT),
            Line(center + 1.5 * LEFT, rect.get_right()),
        )
        mirror.scale(0.8)
        mirror[0].set_color((WHITE, GREY))
        mirror[1].set_color((GREY, WHITE))
        diagram.add(mirror)

        def set_as_reflection(m1, m2):
            m1.become(m2)
            m1.rotate(PI, axis=UP, about_point=center)

        def set_as_mirror_image(m1, m2):
            m1.become(m2)
            m1.rotate(PI, axis=RIGHT, about_point=center)

        wires = VGroup(*[
            Line(center + np.array([-1, -1.5, 0]), center)
            for x in range(4)
        ])
        dl_wire, dr_wire, ul_wire, ur_wire = wires
        dr_wire.add_updater(
            lambda m: set_as_reflection(m, dl_wire)
        )
        ul_wire.add_updater(
            lambda m: set_as_mirror_image(m, dl_wire)
        )
        ur_wire.add_updater(
            lambda m: set_as_mirror_image(m, dr_wire)
        )

        diagram.wires = wires
        diagram.wires.set_stroke(RED, 2)
        diagram.add(diagram.wires)

    def introduce_wires(self):
        dl_wire = self.dl_wire
        dr_wire = self.dr_wire

        def get_rect(wire):
            rect = Rectangle(
                width=wire.get_length(),
                height=0.25,
                color=YELLOW,
            )
            rect.rotate(wire.get_angle())
            rect.move_to(wire)
            return rect

        for wire in dl_wire, dr_wire:
            self.play(ShowCreationThenFadeOut(get_rect(wire)))
            self.play(*self.get_shooting_beam_anims(wire))
            self.wait()

        diagram = self.diagram.copy()
        diagram.clear_updaters()
        self.play(
            FadeIn(diagram.rect),
            ShowCreation(diagram.mirror),
            LaggedStartMap(ShowCreation, diagram.wires),
            run_time=1
        )
        self.remove(diagram)
        self.add(self.diagram)

        self.wait()

    def show_illusion(self):
        g_trajectory = self.ghost_trajectory
        d_trajectory = self.d_trajectory = Line(
            self.diagram.wires[0].get_start(),
            self.diagram.wires[3].get_start(),
        )
        d_trajectory.match_style(g_trajectory)

        g_trajectory.get_points()[0] += 0.2 * RIGHT + 0.1 * DOWN
        g_trajectory.make_jagged()
        for x in range(3):
            self.play(
                *self.get_shooting_beam_anims(g_trajectory),
                *self.get_shooting_beam_anims(d_trajectory),
            )
            self.wait()

    def show_angles(self):
        dl_wire = self.diagram.wires[0]
        dr_wire = self.diagram.wires[1]
        center = self.diagram.get_center()
        arc_config = {
            "radius": 0.5,
            "arc_center": center,
        }

        def get_dl_arc():
            return Arc(
                start_angle=PI,
                angle=dl_wire.get_angle(),
                **arc_config,
            )
        dl_arc = always_redraw(get_dl_arc)

        def get_dr_arc():
            return Arc(
                start_angle=0,
                angle=dr_wire.get_angle() - PI,
                **arc_config,
            )
        dr_arc = always_redraw(get_dr_arc)

        incidence = OldTexText("Incidence")
        reflection = OldTexText("Reflection")
        words = VGroup(incidence, reflection)
        words.scale(0.75)
        incidence.add_updater(
            lambda m: m.next_to(dl_arc, LEFT, SMALL_BUFF)
        )
        reflection.add_updater(
            lambda m: m.next_to(dr_arc, RIGHT, SMALL_BUFF)
        )
        for word in words:
            word.set_background_stroke(width=0)
            word.add_updater(lambda m: m.shift(SMALL_BUFF * DOWN))

        self.add(incidence)
        self.play(
            ShowCreation(dl_arc),
            UpdateFromAlphaFunc(
                VMobject(),
                lambda m, a: incidence.set_fill(opacity=a),
                remover=True
            ),
        )
        self.wait()
        self.add(reflection)
        self.play(
            ShowCreation(dr_arc),
            UpdateFromAlphaFunc(
                VMobject(),
                lambda m, a: reflection.set_fill(opacity=a),
                remover=True
            ),
        )
        self.wait()

        # Change dr wire angle
        # dr_wire.suspend_updating()
        dr_wire.clear_updaters()
        for angle in [20 * DEGREES, -20 * DEGREES]:
            self.play(
                Rotate(
                    dr_wire, angle,
                    about_point=dr_wire.get_end(),
                    run_time=2,
                ),
            )
            self.play(
                *self.get_shooting_beam_anims(self.ghost_trajectory),
                *self.get_shooting_beam_anims(self.d_trajectory),
            )
            self.wait()

    def show_reflecting_beam(self):
        self.play(
            *self.get_shooting_beam_anims(self.trajectory),
            *self.get_shooting_beam_anims(self.ghost_trajectory),
        )
        self.wait()
