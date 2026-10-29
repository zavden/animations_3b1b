# ==============================================================================
# Scene:      CircleDiagramFromSlidingBlocks1e2
# Source:     videos/_2019/clacks/solution1.py (lines 1316-1319)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/clacks/question.py
#
# Run from this folder:
#     manimgl CircleDiagramFromSlidingBlocks1e2.py CircleDiagramFromSlidingBlocks1e2 -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Complete the migration of ClackFlashes to updaters with dt and Animation.interpolate.
#   - Explicitly pass Block's fill and stroke to Square; GL overwrote them with its defaults.
#   - Compute the collision times with the original geometry and configuration of the blocks without initializing a nested GL scene.
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


class BlocksAndWallExampleMass1e2(BlocksAndWallExample):
    CONFIG = {
        "sliding_blocks_config": {
            "block1_config": {
                "mass": 1e2,
                "velocity": -0.6,
            }
        },
        "wait_time": 35,
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
        # CHANGE: compute collision times from block geometry without a nested renderer.
        sliding_blocks_scene = self.BlocksAndWallSceneClass.__new__(self.BlocksAndWallSceneClass)
        digest_config(sliding_blocks_scene, dict(
            show_flash_animations=False,
            count_clacks=False,
        ))
        sliding_blocks_scene.floor = sliding_blocks_scene.get_floor()
        sliding_blocks_scene.wall = sliding_blocks_scene.get_wall()
        sliding_blocks_scene.blocks = SlidingBlocks(
            sliding_blocks_scene, **sliding_blocks_scene.sliding_blocks_config
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


class CircleDiagramFromSlidingBlocks1e2(CircleDiagramFromSlidingBlocks):
    CONFIG = {
        "BlocksAndWallSceneClass": BlocksAndWallExampleMass1e2
    }
