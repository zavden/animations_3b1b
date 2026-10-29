# ==============================================================================
# Scene:      AskAboutFindingNewVelocities
# Source:     videos/_2019/clacks/solution1.py (lines 180-618)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/clacks/question.py
#
# Run from this folder:
#     manimgl AskAboutFindingNewVelocities.py AskAboutFindingNewVelocities -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
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



# ----- From _2019/clacks/solution1.py -----

class AskAboutFindingNewVelocities(Scene):
    CONFIG = {
        "floor_y": -3,
        "wall_x": -6.5,
        "wall_height": 7,
        "block1_config": {
            "mass": 10,
            "fill_color": BLUE_E,
            "velocity": -1,
        },
        "block2_config": {"mass": 1},
        "block1_start_x": 7,
        "block2_start_x": 3,
        "v_arrow_scale_value": 1.0,
        "is_halted": False,
    }

    def setup(self):
        self.add_clack_sound_file()

    def construct(self):
        self.add_clack_sound_file()
        self.add_floor()
        self.add_wall()
        self.add_blocks()
        self.add_velocity_labels()

        self.ask_about_transfer()
        self.show_ms_and_vs()
        self.show_value_on_equations()

    def add_clack_sound_file(self):
        self.clack_file = os.path.join(SOUND_DIR, "clack.wav")

    def add_floor(self):
        floor = self.floor = Line(
            self.wall_x * RIGHT,
            (FRAME_WIDTH / 2) * RIGHT,
        )
        floor.shift(self.floor_y * UP)
        self.add(floor)

    def add_wall(self):
        wall = self.wall = Wall(height=self.wall_height)
        wall.move_to(
            self.wall_x * RIGHT + self.floor_y * UP,
            DR,
        )
        self.add(wall)

    def add_blocks(self):
        block1 = self.block1 = Block(**self.block1_config)
        block2 = self.block2 = Block(**self.block2_config)
        blocks = self.blocks = VGroup(block1, block2)
        block1.move_to(self.block1_start_x * RIGHT + self.floor_y * UP, DOWN)
        block2.move_to(self.block2_start_x * RIGHT + self.floor_y * UP, DOWN)

        self.add_velocity_phase_space_point()
        # Add arrows
        for block in blocks:
            arrow = Vector(self.block_to_v_vector(block))
            arrow.set_color(RED)
            arrow.set_stroke(BLACK, 1, background=True)
            arrow.move_to(block.get_center(), RIGHT)
            block.arrow = arrow
            block.add(arrow)

            block.v_label = DecimalNumber(
                block.velocity,
                num_decimal_places=2,
                background_stroke_width=2,
            )
            block.v_label.set_color(RED)
            block.add(block.v_label)

        # Add updater
        blocks.add_updater(self.update_blocks)
        self.add(
            blocks,
            block2.arrow, block1.arrow,
            block2.v_label, block1.v_label,
        )

    def add_velocity_phase_space_point(self):
        self.vps_point = VectorizedPoint([
            np.sqrt(self.block1.mass) * self.block1.velocity,
            np.sqrt(self.block2.mass) * self.block2.velocity,
            0
        ])

    def add_velocity_labels(self):
        v_labels = self.get_next_velocity_labels()

        self.add(v_labels)

    def ask_about_transfer(self):
        energy_expression, momentum_expression = \
            self.get_energy_and_momentum_expressions()
        energy_words = OldTexText("Conservation of energy:")
        energy_words.move_to(UP)
        energy_words.to_edge(LEFT, buff=1.5)
        momentum_words = OldTexText("Conservation of momentum:")
        momentum_words.next_to(
            energy_words, DOWN,
            buff=0.7,
        )

        energy_expression.next_to(energy_words, RIGHT, MED_LARGE_BUFF)
        momentum_expression.next_to(energy_expression, DOWN)
        momentum_expression.next_to(momentum_words, RIGHT)

        velocity_labels = self.all_velocity_labels
        randy = Randolph(height=2)
        randy.next_to(velocity_labels, DR)
        randy.save_state()
        randy.fade(1)

        # Up to collisions
        self.go_through_next_collision(include_velocity_label_animation=True)
        self.play(
            randy.restore,
            randy.change, "pondering", velocity_labels[0],
        )
        self.halt()
        self.play(randy.look_at, velocity_labels[-1])
        self.play(Blink(randy))
        self.play(randy.change, "confused")
        self.play(Blink(randy))
        self.wait()
        self.play(
            FadeIn(energy_words, RIGHT),
            FadeInFromDown(energy_expression),
            FadeOut(randy),
        )
        self.wait()
        self.play(
            FadeIn(momentum_words, RIGHT),
            FadeInFromDown(momentum_expression)
        )
        self.wait()

        self.energy_expression = energy_expression
        self.energy_words = energy_words
        self.momentum_expression = momentum_expression
        self.momentum_words = momentum_words

    def show_ms_and_vs(self):
        block1 = self.block1
        block2 = self.block2
        energy_expression = self.energy_expression
        momentum_expression = self.momentum_expression

        for block in self.blocks:
            block.shift_onto_screen()

        m1_labels = VGroup(
            block1.label,
            energy_expression.get_part_by_tex("m_1"),
            momentum_expression.get_part_by_tex("m_1"),
        )
        m2_labels = VGroup(
            block2.label,
            energy_expression.get_part_by_tex("m_2"),
            momentum_expression.get_part_by_tex("m_2"),
        )
        v1_labels = VGroup(
            block1.v_label,
            energy_expression.get_part_by_tex("v_1"),
            momentum_expression.get_part_by_tex("v_1"),
        )
        v2_labels = VGroup(
            block2.v_label,
            energy_expression.get_part_by_tex("v_2"),
            momentum_expression.get_part_by_tex("v_2"),
        )
        label_groups = VGroup(
            m1_labels, m2_labels,
            v1_labels, v2_labels,
        )
        for group in label_groups:
            group.rects = VGroup(*map(
                SurroundingRectangle,
                group
            ))

        for group in label_groups:
            self.play(LaggedStartMap(
                ShowCreation, group.rects,
                lag_ratio=0.8,
                run_time=1,
            ))
            self.play(FadeOut(group.rects))

    def show_value_on_equations(self):
        energy_expression = self.energy_expression
        momentum_expression = self.momentum_expression
        energy_text = VGroup(energy_expression, self.energy_words)
        momentum_text = VGroup(momentum_expression, self.momentum_words)
        block1 = self.block1
        block2 = self.block2
        block1.save_state()
        block2.save_state()

        v_terms, momentum_v_terms = [
            VGroup(*[
                expr.get_part_by_tex("v_{}".format(d))
                for d in [1, 2]
            ])
            for expr in [energy_expression, momentum_expression]
        ]
        v_braces = VGroup(*[
            Brace(term, UP, buff=SMALL_BUFF)
            for term in v_terms
        ])
        v_decimals = VGroup(*[DecimalNumber(0) for x in range(2)])

        def update_v_decimals(v_decimals):
            values = self.get_velocities()
            for decimal, value, brace in zip(v_decimals, values, v_braces):
                decimal.set_value(value)
                decimal.next_to(brace, UP, SMALL_BUFF)

        update_v_decimals(v_decimals)

        energy_const_brace, momentum_const_brace = [
            Brace(
                expr.get_part_by_tex("const"), UP,
                buff=SMALL_BUFF,
            )
            for expr in [energy_expression, momentum_expression]
        ]

        sqrt_m_vect = np.array([
            np.sqrt(self.block1.mass),
            np.sqrt(self.block2.mass),
            0
        ])

        def get_energy():
            return 0.5 * get_norm(self.vps_point.get_location())**2

        def get_momentum():
            return np.dot(self.vps_point.get_location(), sqrt_m_vect)

        energy_decimal = DecimalNumber(get_energy())
        energy_decimal.next_to(energy_const_brace, UP, SMALL_BUFF)
        momentum_decimal = DecimalNumber(get_momentum())
        momentum_decimal.next_to(momentum_const_brace, UP, SMALL_BUFF)

        VGroup(
            energy_const_brace, energy_decimal,
            momentum_const_brace, momentum_decimal,
        ).set_color(YELLOW)

        self.play(
            ShowCreationThenFadeAround(energy_expression),
            momentum_text.set_fill, {"opacity": 0.25},
            FadeOut(self.all_velocity_labels),
        )
        self.play(*[
            *map(GrowFromCenter, v_braces),
            *map(VFadeIn, v_decimals),
            GrowFromCenter(energy_const_brace),
            FadeIn(energy_decimal),
        ])
        energy_decimal.add_updater(
            lambda m: m.set_value(get_energy())
        )
        v_decimals.add_updater(update_v_decimals)
        self.add(v_decimals)
        self.unhalt()
        self.vps_point.save_state()
        for x in range(8):
            self.go_through_next_collision()
        energy_decimal.clear_updaters()
        momentum_decimal.set_value(get_momentum())
        self.halt()
        self.play(*[
            momentum_text.set_fill, {"opacity": 1},
            FadeOut(energy_text),
            FadeOut(energy_const_brace),
            FadeOut(energy_decimal),
            GrowFromCenter(momentum_const_brace),
            FadeIn(momentum_decimal),
            *[
                ApplyMethod(b.next_to, vt, UP, SMALL_BUFF)
                for b, vt in zip(v_braces, momentum_v_terms)
            ],
        ])
        self.unhalt()
        self.vps_point.restore()
        momentum_decimal.add_updater(
            lambda m: m.set_value(get_momentum())
        )
        momentum_decimal.add_updater(
            lambda m: m.next_to(momentum_const_brace, UP, SMALL_BUFF)
        )
        for x in range(9):
            self.go_through_next_collision()
        self.wait(10)

    # Helpers

    def get_energy_and_momentum_expressions(self):
        tex_to_color_map = {
            "v_1": RED_B,
            "v_2": RED_B,
            "m_1": BLUE_C,
            "m_2": BLUE_C,
        }
        energy_expression = OldTex(
            "\\frac{1}{2} m_1 (v_1)^2 + ",
            "\\frac{1}{2} m_2 (v_2)^2 = ",
            "\\text{const.}",
            tex_to_color_map=tex_to_color_map,
        )
        momentum_expression = OldTex(
            "m_1 v_1 + m_2 v_2 =", "\\text{const.}",
            tex_to_color_map=tex_to_color_map
        )
        return VGroup(
            energy_expression,
            momentum_expression,
        )

    def go_through_next_collision(self, include_velocity_label_animation=False):
        block2 = self.block2
        if block2.velocity >= 0:
            self.wait_until(self.blocks_are_hitting)
            self.add_sound(self.clack_file)
            self.transfer_momentum()
            edge = RIGHT
        else:
            self.wait_until(self.block2_is_hitting_wall)
            self.add_sound(self.clack_file)
            self.reflect_block2()
            edge = LEFT
        anims = [Flash(block2.get_edge_center(edge))]
        if include_velocity_label_animation:
            anims.append(self.get_next_velocity_labels_animation())
        self.play(*anims, run_time=0.5)

    def get_next_velocity_labels_animation(self):
        return FadeIn(
            self.get_next_velocity_labels(),
            LEFT,
            run_time=0.5
        )

    def get_next_velocity_labels(self, v1=None, v2=None):
        new_labels = self.get_velocity_labels(v1, v2)
        if hasattr(self, "all_velocity_labels"):
            arrow = Vector(RIGHT)
            arrow.next_to(self.all_velocity_labels)
            new_labels.next_to(arrow, RIGHT)
            new_labels.add(arrow)
        else:
            self.all_velocity_labels = VGroup()
        self.all_velocity_labels.add(new_labels)
        return new_labels

    def get_velocity_labels(self, v1=None, v2=None):
        default_vs = self.get_velocities()
        v1 = v1 or default_vs[0]
        v2 = v2 or default_vs[1]
        labels = VGroup(
            OldTex("v_1 = {:.2f}".format(v1)),
            OldTex("v_2 = {:.2f}".format(v2)),
        )
        labels.arrange(
            DOWN,
            buff=MED_SMALL_BUFF,
            aligned_edge=LEFT,
        )
        labels.scale(0.9)
        for label in labels:
            label[:2].set_color(RED)
        labels.next_to(self.wall, RIGHT)
        labels.to_edge(UP, buff=MED_SMALL_BUFF)
        return labels

    def update_blocks(self, blocks, dt):
        for block, velocity in zip(blocks, self.get_velocities()):
            block.velocity = velocity
            if not self.is_halted:
                block.shift(block.velocity * dt * RIGHT)
            center = block.get_center()
            block.arrow.put_start_and_end_on(
                center,
                center + self.block_to_v_vector(block),
            )
            max_height = 0.25
            block.v_label.set_value(block.velocity)
            if block.v_label.get_height() > max_height:
                block.v_label.set_height(max_height)
            block.v_label.next_to(
                block.arrow.get_start(), UP,
                buff=SMALL_BUFF,
            )
        return blocks

    def block_to_v_vector(self, block):
        return block.velocity * self.v_arrow_scale_value * RIGHT

    def blocks_are_hitting(self):
        x1 = self.block1.get_left()[0]
        x2 = self.block2.get_right()[0]
        buff = 0.01
        return (x1 < x2 + buff)

    def block2_is_hitting_wall(self):
        x2 = self.block2.get_left()[0]
        buff = 0.01
        return (x2 < self.wall_x + buff)

    def get_velocities(self):
        m1 = self.block1.mass
        m2 = self.block2.mass
        vps_coords = self.vps_point.get_location()
        return [
            vps_coords[0] / np.sqrt(m1),
            vps_coords[1] / np.sqrt(m2),
        ]

    def transfer_momentum(self):
        m1 = self.block1.mass
        m2 = self.block2.mass
        theta = np.arctan(np.sqrt(m2 / m1))
        self.reflect_block2()
        self.vps_point.rotate(2 * theta, about_point=ORIGIN)

    def reflect_block2(self):
        self.vps_point.get_points()[:, 1] *= -1

    def halt(self):
        self.is_halted = True

    def unhalt(self):
        self.is_halted = False
