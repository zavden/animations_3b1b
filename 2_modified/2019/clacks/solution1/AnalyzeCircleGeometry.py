# ==============================================================================
# Scene:      AnalyzeCircleGeometry
# Source:     videos/_2019/clacks/solution1.py (lines 1367-1754)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/clacks/question.py
#
# Run from this folder:
#     manimgl AnalyzeCircleGeometry.py AnalyzeCircleGeometry -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Complete the migration of ClackFlashes to updaters with dt and Animation.interpolate.
#   - Explicitly pass Block's fill and stroke to Square; GL overwrote them with its defaults.
# ==============================================================================

from manim_imports_ext import *


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


class BlocksAndWallExampleMass1e1(BlocksAndWallExample):
    CONFIG = {
        "sliding_blocks_config": {
            "block1_config": {
                "mass": 1e1,
                "velocity": -1.5,
            }
        },
        "wait_time": 20,
    }



# ----- From _2019/clacks/solution1.py -----

class CircleDiagramFromSlidingBlocks(Scene):
    CONFIG = {
        "BlocksAndWallSceneClass": BlocksAndWallExampleMass1e1,
        "circle_config": {
            "radius": 2,
            "stroke_color": YELLOW,
            "stroke_width": 3,
        },
        "lines_style": {
            "stroke_color": WHITE,
            "stroke_width": 2,
        },
        "axes_config": {
            "style": {
                "stroke_color": GREY_B,
                "stroke_width": 1,
            },
            "width": 5,
            "height": 4.5,
        },
        "end_zone_style": {
            "stroke_width": 0,
            "fill_color": GREEN,
            "fill_opacity": 0.3,
        },
        "show_dot": True,
        "show_vector": False,
    }

    def construct(self):
        sliding_blocks_scene = self.BlocksAndWallSceneClass(
            show_flash_animations=False,
            write_to_movie=False,
            wait_time=0,
            file_writer_config={
                "output_directory": ".",
            }
        )
        blocks = sliding_blocks_scene.blocks
        times = [pair[1] for pair in blocks.clack_data]
        self.mass_ratio = 1 / blocks.mass_ratio
        self.show_circle_lines(
            times=times,
            slope=(-1 / np.sqrt(blocks.mass_ratio))
        )

    def show_circle_lines(self, times, slope):
        circle = self.get_circle()
        axes = self.get_axes()
        lines = self.get_lines(circle.radius, slope)
        end_zone = self.get_end_zone()

        dot = Dot(color=RED, radius=0.06)
        dot.move_to(lines[0].get_start())

        vector = Vector(lines[0].get_start())
        vector.set_color(RED)
        vector.add_updater(lambda v: v.put_start_and_end_on(
            ORIGIN, dot.get_center()
        ))
        vector.set_stroke(BLACK, 2, background=True)

        dot.set_opacity(int(self.show_dot))
        vector.set_opacity(int(self.show_vector))

        self.add(end_zone, axes, circle, dot, vector)

        last_time = 0
        for time, line in zip(times, lines):
            if time > 300:
                time = last_time + 1
            self.wait(time - last_time)
            last_time = time
            dot.move_to(line.get_end())
            self.add(line, dot, vector)
        self.wait()

    def get_circle(self):
        circle = Circle(**self.circle_config)
        circle.rotate(PI)  # Nice to have start point on left
        return circle

    def get_axes(self):
        config = self.axes_config
        axes = VGroup(
            Line(LEFT, RIGHT).set_width(config["width"]),
            Line(DOWN, UP).set_height(config["height"])
        )
        axes.set_style(**config["style"])
        return axes

    def get_lines(self, radius, slope):
        theta = np.arctan(-1 / slope)
        n_clacks = int(PI / theta)
        points = []
        for n in range(n_clacks + 1):
            theta_mult = (n + 1) // 2
            angle = 2 * theta * theta_mult
            if n % 2 == 0:
                angle *= -1
            new_point = radius * np.array([
                -np.cos(angle), -np.sin(angle), 0
            ])
            points.append(new_point)

        lines = VGroup(*[
            Line(p1, p2)
            for p1, p2 in zip(points, points[1:])
        ])
        lines.set_style(**self.lines_style)
        return lines

    def get_end_zone(self):
        slope = 1 / np.sqrt(self.mass_ratio)
        x = self.axes_config["width"] / 2
        zone = Polygon(
            ORIGIN, x * RIGHT, x * RIGHT + slope * x * UP,
        )
        zone.set_style(**self.end_zone_style)
        return zone


class AnalyzeCircleGeometry(CircleDiagramFromSlidingBlocks, MovingCameraScene):
    CONFIG = {
        "mass_ratio": 16,
        "circle_config": {
            "radius": 3,
        },
        "axes_config": {
            "width": FRAME_WIDTH,
            "height": FRAME_HEIGHT,
        },
        "lines_style": {
            "stroke_width": 2,
        },
    }

    def construct(self):
        self.add_mass_ratio_label()
        self.add_circle_with_lines()
        self.show_equal_arc_lengths()
        self.use_arc_lengths_to_count()
        self.focus_on_three_points()
        self.show_likewise_for_all_jumps()
        self.drop_arc_for_each_hop()
        self.try_adding_one_more_arc()
        self.zoom_out()

    def add_mass_ratio_label(self, mass_ratio=None):
        mass_ratio = mass_ratio or self.mass_ratio
        mass_ratio_label = OldTexText(
            "Mass ratio =", "{:,} : 1".format(mass_ratio)
        )
        mass_ratio_label.to_corner(UL, buff=MED_SMALL_BUFF)
        self.add(mass_ratio_label)
        self.mass_ratio_label = mass_ratio_label

    def add_circle_with_lines(self):
        circle = self.get_circle()
        axes = self.get_axes()
        axes_labels = self.get_axes_labels(axes)
        slope = -np.sqrt(self.mass_ratio)
        lines = self.get_lines(
            radius=circle.radius,
            slope=slope,
        )
        end_zone = self.get_end_zone()

        end_zone_words = OldTexText("End zone")
        end_zone_words.set_height(0.25)
        end_zone_words.next_to(ORIGIN, UP, SMALL_BUFF)
        end_zone_words.to_edge(RIGHT, buff=MED_SMALL_BUFF)
        end_zone_words.set_color(GREEN)

        self.add(
            axes, axes_labels,
            circle, end_zone, end_zone_words,
        )
        self.play(ShowCreation(lines, run_time=3, rate_func=linear))
        self.wait()

        self.set_variables_as_attrs(
            circle, axes, lines,
            end_zone, end_zone_words,
        )

    def show_equal_arc_lengths(self):
        circle = self.circle
        radius = circle.radius
        theta = self.theta = np.arctan(1 / np.sqrt(self.mass_ratio))
        n_arcs = int(PI / (2 * theta))

        lower_arcs = VGroup(*[
            Arc(
                start_angle=(PI + n * 2 * theta),
                angle=(2 * theta),
                radius=radius
            )
            for n in range(n_arcs + 1)
        ])
        lower_arcs[0::2].set_color(RED)
        lower_arcs[1::2].set_color(BLUE)

        upper_arcs = lower_arcs.copy()
        upper_arcs.rotate(PI, axis=RIGHT, about_point=ORIGIN)
        upper_arcs[0::2].set_color(BLUE)
        upper_arcs[1::2].set_color(RED)

        all_arcs = VGroup(*it.chain(*zip(lower_arcs, upper_arcs)))
        if int(PI / theta) % 2 == 1:
            all_arcs.remove(all_arcs[-1])

        arc_copies = lower_arcs.copy()
        for arc_copy in arc_copies:
            arc_copy.generate_target()
        for arc in arc_copies:
            arc.target.rotate(-(arc.start_angle - PI + theta))

        equal_signs = VGroup(*[
            OldTex("=") for x in range(len(lower_arcs))
        ])
        equal_signs.scale(0.8)
        for sign in equal_signs:
            sign.generate_target()

        movers = VGroup(*it.chain(*zip(
            arc_copies, equal_signs
        )))
        movers.remove(movers[-1])
        mover_targets = VGroup(*[mover.target for mover in movers])
        mover_targets.arrange(RIGHT, buff=SMALL_BUFF)
        mover_targets.next_to(ORIGIN, DOWN)
        mover_targets.to_edge(LEFT)

        equal_signs.scale(0)
        equal_signs.fade(1)
        equal_signs.move_to(mover_targets)

        all_arcs.save_state()
        for arc in all_arcs:
            arc.rotate(90 * DEGREES)
            arc.fade(1)
            arc.set_stroke(width=20)
        self.play(Restore(
            all_arcs, lag_ratio=0.5,
            run_time=2,
        ))
        self.wait()
        self.play(LaggedStartMap(MoveToTarget, movers))
        self.wait()

        self.arcs_equation = movers
        self.lower_arcs = lower_arcs
        self.upper_arcs = upper_arcs
        self.all_arcs = all_arcs

    def use_arc_lengths_to_count(self):
        all_arcs = self.all_arcs
        lines = self.lines

        arc_counts = VGroup()
        for n, arc in enumerate(all_arcs):
            count_mob = Integer(n + 1)
            count_mob.scale(0.75)
            buff = SMALL_BUFF
            if len(all_arcs) > 100:
                count_mob.scale(0.1)
                count_mob.set_stroke(WHITE, 0.25)
                buff = 0.4 * SMALL_BUFF
            point = arc.point_from_proportion(0.5)
            count_mob.next_to(point, normalize(point), buff)
            arc_counts.add(count_mob)

        self.play(
            FadeOut(lines),
            FadeOut(all_arcs),
            FadeOut(self.arcs_equation),
        )
        self.play(
            ShowIncreasingSubsets(all_arcs),
            ShowIncreasingSubsets(lines),
            ShowIncreasingSubsets(arc_counts),
            run_time=5,
            rate_func=bezier([0, 0, 1, 1])
        )
        self.wait()

        for group in all_arcs, arc_counts:
            targets = VGroup()
            for elem in group:
                elem.generate_target()
                targets.add(elem.target)
            targets.space_out_submobjects(1.2)

        kwargs = {
            "rate_func": there_and_back,
            "run_time": 3,
        }
        self.play(
            LaggedStartMap(MoveToTarget, all_arcs, **kwargs),
            LaggedStartMap(MoveToTarget, arc_counts, **kwargs),
        )

        self.arc_counts = arc_counts

    def focus_on_three_points(self):
        lines = self.lines
        arcs = self.all_arcs
        arc_counts = self.arc_counts
        theta = self.theta

        arc = arcs[4]

        lines.save_state()
        line_pair = lines[3:5]
        lines_to_fade = VGroup(*lines[:3], *lines[5:])

        three_points = [
            line_pair[0].get_start(),
            line_pair[1].get_start(),
            line_pair[1].get_end(),
        ]
        three_dots = VGroup(*map(Dot, three_points))
        three_dots.set_color(RED)

        theta_arc = Arc(
            radius=1,
            start_angle=-90 * DEGREES,
            angle=theta
        )
        theta_arc.shift(three_points[1])
        theta_label = OldTex("\\theta")
        theta_label.next_to(theta_arc, DOWN, SMALL_BUFF)

        center_lines = VGroup(
            Line(three_points[0], ORIGIN),
            Line(ORIGIN, three_points[2]),
        )
        center_lines.match_style(line_pair)

        two_theta_arc = Arc(
            radius=1,
            start_angle=(center_lines[0].get_angle() + PI),
            angle=2 * theta
        )
        two_theta_label = OldTex("2\\theta")
        arc_center = two_theta_arc.point_from_proportion(0.5)
        two_theta_label.next_to(
            arc_center, normalize(arc_center), SMALL_BUFF
        )
        two_theta_label.shift(SMALL_BUFF * RIGHT)

        to_fade = VGroup(arc_counts, arcs, lines_to_fade)

        self.play(
            LaggedStartMap(
                FadeOut, VGroup(*to_fade.family_members_with_points())
            )
        )
        lines_to_fade.fade(1)
        self.play(FadeInFromLarge(three_dots[0]))
        self.play(TransformFromCopy(*three_dots[:2]))
        self.play(TransformFromCopy(*three_dots[1:3]))
        self.wait()
        self.play(
            ShowCreation(theta_arc),
            FadeIn(theta_label, UP)
        )
        self.wait()
        self.play(
            line_pair.set_stroke, WHITE, 1,
            TransformFromCopy(line_pair, center_lines),
            TransformFromCopy(theta_arc, two_theta_arc),
            TransformFromCopy(theta_label, two_theta_label),
        )
        self.wait()
        self.play(
            TransformFromCopy(two_theta_arc, arc),
            two_theta_label.move_to, 2.7 * arc_center,
        )
        self.wait()

        self.three_dots = three_dots
        self.theta_group = VGroup(theta_arc, theta_label)
        self.center_lines_group = VGroup(
            center_lines, two_theta_arc,
        )
        self.two_theta_label = two_theta_label

    def show_likewise_for_all_jumps(self):
        lines = self.lines
        arcs = self.all_arcs

        every_other_line = lines[::2]

        self.play(
            Restore(
                lines,
                lag_ratio=0.5,
                run_time=2
            ),
            FadeOut(self.center_lines_group),
            FadeOut(self.three_dots),
        )
        self.play(LaggedStartMap(
            ApplyFunction, every_other_line,
            lambda line: (
                lambda l: l.scale(10 / l.get_length()).set_stroke(BLUE, 3),
                line
            )
        ))
        self.play(Restore(lines))
        self.wait()

        # Shift theta label
        last_point = lines[3].get_end()
        last_arc = arcs[4]
        two_theta_label = self.two_theta_label
        theta_group_copy = self.theta_group.copy()
        for line, arc in zip(lines[5:10:2], arcs[6:11:2]):
            new_point = line.get_end()
            arc_point = arc.point_from_proportion(0.5)
            self.play(
                theta_group_copy.shift, new_point - last_point,
                two_theta_label.move_to, 1.1 * arc_point,
                FadeIn(arc),
                FadeOut(last_arc),
            )
            self.wait()
            last_point = new_point
            last_arc = arc
        self.play(
            FadeOut(theta_group_copy),
            FadeOut(two_theta_label),
            FadeOut(last_arc),
        )
        self.wait()

    def drop_arc_for_each_hop(self):
        lines = self.lines
        arcs = self.all_arcs

        two_theta_labels = VGroup()
        wedges = VGroup()
        for arc in arcs:
            label = OldTex("2\\theta")
            label.scale(0.8)
            label.move_to(1.1 * arc.point_from_proportion(0.5))
            two_theta_labels.add(label)

            wedge = arc.copy()
            wedge.add_line_to(ORIGIN)
            wedge.add_line_to(wedge.get_points()[0])
            wedge.set_stroke(width=0)
            wedge.set_fill(arc.get_color(), 0.2)
            wedges.add(wedge)

        self.remove(lines)
        for line, arc, label, wedge in zip(lines, arcs, two_theta_labels, wedges):
            self.play(
                ShowCreation(line),
                FadeIn(arc, normalize(arc.get_center())),
                FadeIn(label, normalize(arc.get_center())),
                FadeIn(wedge),
            )

        self.wedges = wedges
        self.two_theta_labels = two_theta_labels

    def try_adding_one_more_arc(self):
        wedges = self.wedges
        theta = self.theta

        last_wedge = wedges[-1]
        new_wedge = last_wedge.copy()
        new_wedge.set_color(PURPLE)
        new_wedge.set_stroke(WHITE, 1)

        self.play(FadeIn(new_wedge))
        for angle in [-2 * theta, 4 * DEGREES, -2 * DEGREES]:
            self.play(Rotate(new_wedge, angle, about_point=ORIGIN))
            self.wait()
        self.play(
            new_wedge.shift, 10 * RIGHT,
            rate_func=running_start,
            path_arc=-30 * DEGREES,
        )
        self.remove(new_wedge)

    def zoom_out(self):
        frame = self.camera_frame
        self.play(
            frame.scale, 2, {"about_point": (TOP + RIGHT_SIDE)},
            run_time=3
        )
        self.wait()

    # Helpers
    def get_axes_labels(self, axes):
        axes_labels = VGroup(
            OldTex("x = ", "\\sqrt{m_1}", "\\cdot", "v_1"),
            OldTex("y = ", "\\sqrt{m_2}", "\\cdot", "v_2"),
        )
        for label in axes_labels:
            label.set_height(0.4)
        axes_labels[0].next_to(ORIGIN, DOWN, SMALL_BUFF)
        axes_labels[0].to_edge(RIGHT, MED_SMALL_BUFF)
        axes_labels[1].next_to(ORIGIN, RIGHT, SMALL_BUFF)
        axes_labels[1].to_edge(UP, SMALL_BUFF)
        return axes_labels
