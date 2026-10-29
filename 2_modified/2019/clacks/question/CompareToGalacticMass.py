# ==============================================================================
# Scene:      CompareToGalacticMass
# Source:     videos/_2019/clacks/question.py (lines 1090-1292)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl CompareToGalacticMass.py CompareToGalacticMass -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Complete the migration of ClackFlashes to updaters with dt and Animation.interpolate.
#   - Explicitly pass Block's fill and stroke to Square; GL overwrote them with its defaults.
#   - Access the glyphs of OldTex in the digits and the final counter.
#   - Build the static geometry of the blocks from the configuration without a nested GL scene.
#   - Use the numeric glyphs of the mass label for the brace, excluding the units.
#   - Keep explicit spaces between the words of the mass label that are animated separately.
# ==============================================================================

from manim_imports_ext import *

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


class CompareToGalacticMass(Scene):
    def construct(self):
        self.add_digits_of_pi()
        self.show_mass()
        self.show_galactic_black_holes()
        self.show_total_count()

    def add_digits_of_pi(self):
        # 20 digits of pi
        # CHANGE: expose the glyphs inside GL's single OldTex string part.
        digits = OldTex("3.1415926535897932384...")[0]
        digits.set_width(FRAME_WIDTH - 3)
        digits.to_edge(UP)

        highlighted_digits = VGroup(*[
            d.copy().set_background_stroke(color=BLUE, width=5)
            for d in [digits[0], *digits[2:-3]]
        ])
        counter = Integer(0)
        counter.scale(1.5)
        counter.set_color(BLUE)
        brace = VMobject()
        self.add(counter, brace)

        for k in range(len(highlighted_digits)):
            if k == 0:
                self.add(digits[0])
            else:
                self.remove(highlighted_digits[k - 1])
            self.add(digits[k + 1])
            self.add(highlighted_digits[k])
            counter.increment_value()
            brace.become(Brace(highlighted_digits[:k + 1], DOWN))
            counter.next_to(brace, DOWN)
            self.wait(0.1)
        self.add(digits)
        self.remove(*highlighted_digits)

        digits_word = OldTexText("digits")
        digits_word.scale(1.5)
        digits_word.match_color(counter)
        counter.generate_target()
        group = VGroup(counter.target, digits_word)
        group.arrange(
            RIGHT,
            index_of_submobject_to_align=0,
            aligned_edge=DOWN,
            buff=0.7,
        )
        group.next_to(brace, DOWN)
        self.play(
            MoveToTarget(counter),
            FadeIn(digits_word, LEFT),
        )
        self.wait()

        self.pi_digits_group = VGroup(
            digits, brace, counter, digits_word
        )

    def show_mass(self):
        # CHANGE: build the static block geometry without initializing a nested renderer.
        bw_scene = BlocksAndWallExample.__new__(BlocksAndWallExample)
        digest_config(bw_scene, dict(
            count_clacks=False,
            show_flash_animations=False,
            floor_y=0,
            wall_x=-2,
            n_wall_ticks=8,
            sliding_blocks_config={
                "block1_config": {
                    "mass": 1e6,
                    "velocity": -0.01,
                    "distance": 4.5,
                    "label_text": "$100^{(20 - 1)}$ kg",
                    "fill_color": BLACK,
                },
                "block2_config": {
                    "distance": 1,
                    "velocity": 0,
                },
            }
        ))
        bw_scene.floor = bw_scene.get_floor()
        bw_scene.wall = bw_scene.get_wall()
        bw_scene.blocks = SlidingBlocks(bw_scene, **bw_scene.sliding_blocks_config)
        block1 = bw_scene.blocks.block1
        block2 = bw_scene.blocks.block2
        group = VGroup(
            bw_scene.wall, bw_scene.floor,
            block1, block2
        )
        group.center()
        group.to_edge(DOWN)

        arrow = Vector(2 * LEFT, color=RED)
        arrow.shift(block1.get_center())
        group.add(arrow)

        # CHANGE: bracket the number glyphs rather than the outer OldTexText part.
        brace = Brace(block1.label[0][:-2], UP, buff=SMALL_BUFF)
        # CHANGE: preserve word spacing between the separately animated text parts.
        number_words = OldTexText(
            "100", *["billion"] * 4,
            arg_separator=" ",
        )
        number_words.next_to(brace, UP, buff=SMALL_BUFF)
        VGroup(brace, number_words).set_color(YELLOW)

        self.play(Write(group))
        self.wait()
        last_word = number_words[0].copy()
        last_word.next_to(brace, UP, SMALL_BUFF)
        self.play(
            GrowFromCenter(brace),
            FadeInFromDown(last_word),
        )
        for k in range(1, len(number_words) + 1):
            self.remove(last_word)
            last_word = number_words[:k].copy()
            last_word.next_to(brace, UP, SMALL_BUFF)
            self.add(last_word)
            self.wait(0.4)
        self.wait()
        self.remove(last_word)
        self.add(number_words)
        group.add(brace, number_words)
        self.play(group.to_corner, DL)

        self.block1 = block1
        self.block2 = block2
        self.block_setup_group = group

    def show_galactic_black_holes(self):
        black_hole = SVGMobject(file_name="black_hole")
        black_hole.set_color(BLACK)
        black_hole.set_sheen(0.2, UL)
        black_hole.set_height(1)
        black_holes = VGroup(*[
            black_hole.copy() for k in range(10)
        ])
        black_holes.arrange_in_grid(5, 2)
        black_holes.to_corner(DR)
        random.shuffle(black_holes.submobjects)
        for bh in black_holes:
            bh.save_state()
            bh.scale(3)
            bh.set_fill(GREY_D, 0)

        equals = OldTex("=")
        equals.scale(2)
        equals.next_to(self.block1, RIGHT)

        words = OldTexText("10x Sgr A$^*$ \\\\ supermassive \\\\ black hole")
        words.next_to(equals, RIGHT)
        self.add(words)

        self.play(
            Write(equals),
            Write(words),
            LaggedStartMap(
                Restore, black_holes,
                run_time=3
            )
        )
        self.wait()

        self.black_hole_words = VGroup(equals, words)
        self.black_holes = black_holes

    def show_total_count(self):
        digits = self.pi_digits_group[0]
        to_fade = self.pi_digits_group[1:]
        tex_string = "{:,}".format(31415926535897932384)
        # CHANGE: expose glyphs for digit and comma grouping in the final count.
        number = OldTex(tex_string)[0]
        number.scale(1.5)
        number.to_edge(UP)

        commas = VGroup(*[
            mob
            for c, mob in zip(tex_string, number)
            if c is ","
        ])
        dots = VGroup(*[
            mob
            for c, mob in zip(digits.get_tex(), digits)
            if c is "."
        ])

        self.play(FadeOut(to_fade))
        self.play(
            ReplacementTransform(
                VGroup(*filter(lambda m: m not in dots, digits)),
                VGroup(*filter(lambda m: m not in commas, number)),
            ),
            ReplacementTransform(
                dots, commas,
                lag_ratio=0.5,
                run_time=2
            )
        )

        group0 = number[:2].copy()
        group1 = number[3:3 + 9 + 2].copy()
        group2 = number[-(9 + 2):].copy()
        for group in group0, group1, group2:
            group.set_background_stroke(color=BLUE, width=5)
            self.add(group)
            self.wait(0.5)
            self.remove(group)
