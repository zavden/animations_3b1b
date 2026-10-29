# ==============================================================================
# Scene:      ThumbnailShot
# Source:     videos/_2025/colliding_blocks_v2/blocks.py (lines 1485-1533)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ThumbnailShot.py ThumbnailShot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed the loop that forced the floor and wall normals with part.data['d_normal_point'] (get_floor_and_wall_3d): this manimgl computes the Surface normals in the shader from the mesh and that field no longer exists.
# ==============================================================================

from manim_imports_ext import *

LITTLE_BLOCK_COLOR = "#51463E"


class StateTracker(ValueTracker):
    """
    Tracks the state of the block collision process as a 4d vector
    [
        x1 * sqrt(m1),
        x2 * sqrt(m2),
        v1 * sqrt(m1),
        v2 * sqrt(m2),
    ]
    """

    def __init__(self, blocks, initial_positions=[8, 5], initial_velocities=[-1, 0]):
        sqrt_m1, sqrt_m2 = self.sqrt_mass_vect = np.sqrt([b.mass for b in blocks])
        self.theta = math.atan2(sqrt_m2, sqrt_m1)

        self.state0 = np.array([
            *np.array(initial_positions) * self.sqrt_mass_vect,
            *np.array(initial_velocities) * self.sqrt_mass_vect,
        ])

        super().__init__(self.state0.copy())

    def set_time(self, t):
        pos0 = self.state0[0:2]
        vel0 = self.state0[2:4]

        self.set_value([*(pos0 + t * vel0), *vel0])

    def reflect_vect(self, vect):
        n_reflections = self.get_n_collisions()
        rot_angle = -2 * self.theta * ((n_reflections + 1) // 2)
        result = rotate_vector_2d(vect, rot_angle)
        result[1] *= (-1)**(n_reflections % 2)
        return result

    def get_block_positions(self):
        scaled_pos = self.get_value()[0:2]
        norm = get_norm(scaled_pos)

        rot_scaled_pos = self.reflect_vect(scaled_pos)
        return rot_scaled_pos / self.sqrt_mass_vect

    def get_scaled_block_velocities(self):
        return self.reflect_vect(self.get_value()[2:4])

    def get_block_velocities(self):
        return self.get_scaled_block_velocities() / self.sqrt_mass_vect

    def get_kinetic_energy(self):
        v1, v2 = self.get_value()[2:4]
        return v1**2 + v2**2

    def get_momentum(self):
        v1, v2 = self.get_block_velocities()
        m1, m2 = self.sqrt_mass_vect**2
        return m1 * v1 + m2 * v2

    def get_n_collisions(self):
        state = self.get_value()  # First two coords are [sqrt(m1) * d1, sqrt(m2) * d2]
        angle = math.atan2(state[1], state[0])
        return int(angle / self.theta)

    def time_from_last_collision(self):
        state = self.get_value()
        angle = math.atan2(state[1], state[0])
        n_collisions = int(angle / self.theta)
        if n_collisions == 0:
            return 0
        collisions_angle = n_collisions * self.theta
        rot_state = rotate_vector_2d(state[:2], collisions_angle - angle)
        collision_state = rot_state * (state[1] / rot_state[1])  # Rescale to match y coordinate
        return (collision_state[0] - state[0]) / state[2]


class ClackAnimation(Restore):
    def __init__(self, point, run_time=0.25, **kwargs):
        circles = Circle(radius=0.25).replicate(3)
        circles.move_to(point)
        circles.set_stroke(YELLOW, 0, 0)
        circles.save_state()
        circles.scale(0.1)
        circles.set_stroke(YELLOW, 2, 1)

        super().__init__(circles, lag_ratio=0.1, run_time=run_time, **kwargs)


class Blocks(InteractiveScene):
    initial_positions = [10.5, 8]
    initial_velocities = [-0.975, 0]
    masses = [10, 1]
    widths = [1.0, 0.5]
    colors = [BLUE_E, LITTLE_BLOCK_COLOR]
    three_d = True
    clack_sound = "clack.wav"
    reverse_clack_sound = "reverse_clack.wav"
    floor_width = 13
    floor_depth = 1.5
    wall_height = 2
    block_shading = [0.5, 0.5, 0]
    field_of_view = 45 * DEG

    def setup(self):
        super().setup()

        self.set_floor_plane("xz")
        self.frame.set_field_of_view(self.field_of_view)

        self.floor_wall = self.get_floor_and_wall_3d() if self.three_d else self.get_floor_and_wall_2d()
        self.floor, self.wall = self.floor_wall
        self.blocks = self.get_block_pair(self.floor, three_d=self.three_d)

        self.state_tracker = StateTracker(self.blocks, self.initial_positions, self.initial_velocities)
        self.time_tracker = ValueTracker(0)
        self.state_tracker.f_always.set_time(self.time_tracker.get_value)

        self.bind_blocks_to_state(self.blocks, self.floor, self.state_tracker)

        self.listen_for_clacks = True
        self.last_collision_count = self.state_tracker.get_n_collisions()
        self.last_clack_time = 0
        self.flashes = []

        self.add(self.state_tracker)
        self.add(self.time_tracker)
        self.add(self.floor_wall)
        self.add(self.blocks)

    def construct(self):
        # Setup the experiment
        light_source = self.camera.light_source
        light_source.set_z(3)
        frame = self.frame
        self.set_floor_plane("xz")

        blocks = self.blocks
        floor = self.floor
        state_tracker = self.state_tracker
        time_tracker = self.time_tracker

        for block in blocks:
            block.mass_label.set_opacity(0)

        # Set up equations
        kw = dict(t2c={
            "m_1": BLUE,
            "m_2": BLUE,
            "v_1": RED,
            "v_2": RED,
        })
        ke_equation = Tex(R"\frac{1}{2} m_1 (v_1)^2 + \frac{1}{2}m_2 (v_2)^2 = \text{E}", **kw)
        p_equation = Tex(R"m_1 v_1 + m_2 v_2 = \text{P}", **kw)
        equations = VGroup(ke_equation, p_equation)
        equations.arrange(DOWN, buff=0.75)
        equations.to_edge(UP, buff=0.5)
        equations.fix_in_frame()

        # Introductory shot
        frame.reorient(-42, -3, 0, (-2.08, -2.25, -1.87), 6.95)
        stop_time = 12
        self.play(
            frame.animate.to_default_state(),
            FadeIn(ke_equation, shift=0.5 * UP, time_span=(7, 8)),
            FadeIn(p_equation, shift=0.5 * UP, time_span=(10, 11)),
            time_tracker.animate.set_value(stop_time).set_anim_args(rate_func=linear),
            run_time=stop_time
        )
        self.wait()

        self.add(equations)

        # Add velocity vectors
        vel = state_tracker.get_block_velocities()
        marked_velocity = ValueTracker(vel)
        marked_velocity.f_always.set_value(state_tracker.get_block_velocities)
        self.add(marked_velocity)
        velocity_vectors = VGroup(
            self.get_velocity_vector(blocks[0], lambda: marked_velocity.get_value()[0]),
            self.get_velocity_vector(blocks[1], lambda: marked_velocity.get_value()[1]),
        )
        velocity_vectors.update()
        velocity_vectors.set_z_index(1)

        # Highlight kinetic energy of each one
        self.play(
            frame.animate.reorient(-12, 3, 0, (-3.41, -1.48, 0.01), 4.63),
            blocks[0].mass_label.animate.set_opacity(1),
            blocks[1].mass_label.animate.set_opacity(1),
            VFadeIn(velocity_vectors),
            FadeOut(p_equation, time_span=(1, 2)),
            run_time=3
        )
        self.wait()

        # Highlight corresponding terms
        tex = ["m_1", "v_1", "m_2", "v_2"]
        labels = [
            blocks[0][2],
            velocity_vectors[0][1],
            blocks[1][2],
            velocity_vectors[1][1],
        ]

        last_rects = VGroup()
        for tex, label in zip(tex, labels):
            rects = VGroup(
                SurroundingRectangle(ke_equation[tex], buff=0.05),
                SurroundingRectangle(label, buff=0.05),
            )
            rects[0].set_stroke(YELLOW, 5)
            rects[1].set_stroke(YELLOW, 3)
            self.play(
                FadeOut(last_rects),
                ShowCreation(rects, lag_ratio=0),
            )
            self.wait()
            last_rects = rects
        self.play(FadeOut(last_rects))
        self.wait()

        # Show constant energy
        dec_equation = Tex(R"\frac{1}{2}(10)(+0.00)^2 + \frac{1}{2}(1)(+0.00)^2 = +0.00", font_size=42)
        dec_equation.next_to(ke_equation, DOWN, LARGE_BUFF)

        terms = dec_equation.make_number_changeable("+0.00", replace_all=True, include_sign=True)
        dec_equation.fix_in_frame()
        dec_equation["(1)"].set_color(BLUE)
        dec_equation["(10)"].set_color(BLUE)
        terms[:2].set_color(RED)
        terms[0].f_always.set_value(lambda: state_tracker.get_block_velocities()[0])
        terms[1].f_always.set_value(lambda: state_tracker.get_block_velocities()[1])
        terms[2].set_value(state_tracker.get_kinetic_energy())
        terms.update()

        label_targets = VGroup(dec_equation["(10)"], terms[0], dec_equation["(1)"], terms[1]).copy()
        label_targets.clear_updaters()

        self.play(
            VFadeIn(dec_equation, time_span=(1.5, 2)),
            Transform(VGroup(*labels).copy().clear_updaters(), label_targets, remover=True, run_time=2, lag_ratio=1e-3),
        )
        self.wait()
        self.play(time_tracker.animate.increment_value(1), rate_func=there_and_back, run_time=6)
        self.wait()
        self.play(
            time_tracker.animate.increment_value(10).set_anim_args(rate_func=linear),
            frame.animate.reorient(-1, 3, 0, (-1.59, -0.79, 0.17), 6.46),
            run_time=10,
            rate_func=linear
        )
        dec_equation.clear_updaters()
        self.play(
            time_tracker.animate.set_value(12),
            frame.animate.reorient(-12, 3, 0, (-3.41, -1.48, 0.01), 4.63),
            FadeOut(dec_equation),
            run_time=2,
        )
        self.wait()

        # Highlight momentum
        self.play(
            ke_equation.animate.set_opacity(0.2),
            FadeIn(p_equation),
            time_tracker.animate.increment_value(-1),
        )
        self.wait()

        # Show the net momentum calculation (much copying here)
        p_dec_equation = Tex(R"(10)(+0.00) + (1)(+0.00) = +0.00", font_size=42)
        p_terms = p_dec_equation.make_number_changeable("+0.00", replace_all=True, include_sign=True)
        p_terms[:2].set_color(RED)
        p_dec_equation["(1)"].set_color(BLUE)
        p_dec_equation["(10)"].set_color(BLUE)
        p_dec_equation.fix_in_frame()
        p_dec_equation.next_to(p_equation, DOWN, buff=0.75)

        p_terms[0].f_always.set_value(lambda: state_tracker.get_block_velocities()[0])
        p_terms[1].f_always.set_value(lambda: state_tracker.get_block_velocities()[1])
        p_terms[2].f_always.set_value(state_tracker.get_momentum)

        label_targets = VGroup(p_dec_equation["(10)"], p_terms[0], p_dec_equation["(1)"], p_terms[1]).copy()
        label_targets.clear_updaters()

        self.play(
            frame.animate.reorient(-2, 2, 0, (-2.82, -0.66, 0.11), 5.96),
            VFadeIn(p_dec_equation),
            Transform(VGroup(*labels).copy().clear_updaters(), label_targets, remover=True),
            run_time=2
        )
        self.play(
            time_tracker.animate.increment_value(8).set_anim_args(rate_func=linear),
            frame.animate.reorient(6, -1, 0, (-0.7, -0.25, -0.17), 7.75),
            run_time=16,
        )
        self.wait()

        # Reset
        marked_velocity.clear_updaters()
        blocks.clear_updaters()
        self.remove(state_tracker)

        state_tracker = StateTracker(blocks, [9.5, 8], [-1, 0])
        time_tracker.set_value(0)
        state_tracker.add_updater(lambda m: m.set_time(time_tracker.get_value()))
        self.state_tracker = state_tracker
        self.bind_blocks_to_state(blocks, floor, state_tracker)
        self.add(state_tracker)

        p_dec_equation.clear_updaters()
        self.play(
            FadeOut(p_dec_equation, 2 * LEFT),
            frame.animate.to_default_state(),
            equations.animate.set_width(4.5).arrange(DOWN, buff=0.5).set_opacity(1).to_corner(UL),
            run_time=2
        )
        self.wait()

        # Highlight velocity terms
        v_terms = VGroup(
            eq[f"v_{n}"]
            for eq in equations
            for n in [1, 2]
        )
        v_point = Point([*marked_velocity.get_value(), 0])
        v_point.target = v_point.generate_target()
        v_point.target.move_to([*state_tracker.get_block_velocities(), 0])

        self.play(
            LaggedStartMap(FlashAround, v_terms, lag_ratio=0.1, time_width=1.0, time_span=(0, 2)),
            MoveToTarget(v_point, path_arc=PI),
            UpdateFromFunc(marked_velocity, lambda m: m.set_value(v_point.get_center()[:2])),
            run_time=3,
        )
        self.wait()

        # Introduce coordinate plane
        plane = NumberPlane((-4, 4, 1), (-4, 4, 1), faded_line_ratio=1)
        plane.set_height(5)
        plane.to_corner(UR, buff=0.25)
        plane.shift(2.0 * LEFT)
        plane.axes.set_stroke(WHITE, 1)
        plane.background_lines.set_stroke(BLUE, 1, 0.5)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)

        state_point = Group(
            TrueDot(radius=0.05).make_3d(),
            GlowDot(radius=0.2),
        )
        state_point.set_color(RED)
        state_point.add_updater(lambda m: m.move_to(plane.c2p(*marked_velocity.get_value())))

        kw["font_size"] = 36
        x_label, y_label = axis_labels = VGroup(
            Tex("x = v_1", **kw),
            Tex("y = v_2", **kw),
        )
        x_label.next_to(plane.x_axis.get_right(), UR, SMALL_BUFF)
        x_label.shift_onto_screen(buff=SMALL_BUFF)
        y_label.next_to(plane.y_axis.get_top(), DR, SMALL_BUFF)

        self.play(ShowCreation(plane, lag_ratio=2e-2))
        self.play(
            Write(x_label[:2]),
            TransformFromCopy(ke_equation["v_1"][0], x_label["v_1"][0]),
            FadeIn(state_point),
        )
        self.add(x_label)
        self.play(
            marked_velocity.animate.set_value([3, 0]),
            run_time=3,
            rate_func=there_and_back,
        )
        self.wait()
        self.play(
            Write(y_label[:2]),
            TransformFromCopy(ke_equation["v_2"][0], y_label["v_2"][0]),
        )
        self.add(y_label)
        self.play(
            marked_velocity.animate.set_value([-1, 3]),
            run_time=5,
            rate_func=wiggle,
        )
        self.wait()

        # Let it play forward
        marked_velocity.add_updater(lambda m: m.set_value(state_tracker.get_block_velocities()))
        self.add(state_tracker, marked_velocity)

        self.play(
            time_tracker.animate.set_value(10),
            run_time=10,
            rate_func=linear,
        )

        # Show coordinates
        coord_label = Tex(R"(+0.00, +0.00)", font_size=36)
        coord_label.set_color(RED)
        terms = coord_label.make_number_changeable("+0.00", replace_all=True, include_sign=True)
        for term, v in zip(terms, state_tracker.get_block_velocities()):
            term.set_value(v)
        coord_label.next_to(state_point, UR, buff=0)

        self.play(LaggedStart(
            TransformFromCopy(velocity_vectors[0][1].copy().clear_updaters(), terms[0]),
            TransformFromCopy(velocity_vectors[1][1].copy().clear_updaters(), terms[1]),
            FadeIn(coord_label[0::2]),
            lag_ratio=0.5,
        ))
        self.wait()

        # Insertion
        if False:
            # This is just for a certain scene we're plugging in,
            # not meant to be part of the main scene
            self.remove(equations)
            self.frame.set_field_of_view(1 * DEG)
            self.camera.light_source.set_z(3)

            blocks.clear_updaters()
            blocks.scale(1.2)
            velocity_vectors.scale(0.8)
            blocks.arrange(LEFT, buff=LARGE_BUFF, aligned_edge=DOWN)
            blocks[0][0].set_opacity(0.5)
            blocks[1][0].set_opacity(0.5)
            blocks.next_to(plane, LEFT, buff=LARGE_BUFF)

            marked_velocity.clear_updaters()

            # Many random points
            for _ in range(15):
                coords = np.random.uniform(-4, 4, 2)
                self.play(marked_velocity.animate.set_value(coords))
                self.wait()

        # Back up and add tail (Maybe just fade to here)
        self.play(
            FadeOut(coord_label),
            time_tracker.animate.set_value(0).set_anim_args(run_time=2)
        )

        traced_path = self.get_traced_path(state_point)
        self.add(traced_path)

        self.play(
            time_tracker.animate.set_value(45),
            run_time=25,
            rate_func=linear,
        )
        traced_path.clear_updaters()

        # Highlight the conservation of energy
        ke_rect = SurroundingRectangle(ke_equation).set_stroke(YELLOW, 2)
        question = Text("How would you plot this?", font_size=36)
        question.next_to(ke_rect, DOWN)
        question.set_color(YELLOW)

        self.play(
            FadeOut(p_equation),
            ShowCreation(ke_rect),
            Write(question, run_time=1),
        )
        self.wait()
        time_tracker.set_value(0)
        blocks.update()

        # Show xy equation
        xy_equation = Tex(R"5.00 {x}^2 + 0.50 {y}^2 = \text{E}", font_size=36)
        xy_equation["{x}"].set_color(RED)
        xy_equation["{y}"].set_color(RED)
        xy_equation.next_to(question, DOWN, buff=MED_LARGE_BUFF)
        x_coef = xy_equation.make_number_changeable("5.00")
        y_coef = xy_equation.make_number_changeable("0.50")

        ellipse = Circle(radius=plane.x_axis.get_unit_size())
        ellipse.set_stroke(YELLOW, 2)
        ellipse.stretch(math.sqrt(10), 1)
        ellipse.move_to(plane.c2p(0, 0))

        state_point.set_z_index(1)

        self.play(FadeIn(xy_equation, DOWN))
        self.wait()
        self.play(
            traced_path.animate.set_stroke(WHITE, 1, 0.25),
            ShowCreation(ellipse),
            run_time=3
        )
        self.wait()

        # Emphasize squish
        self.play(
            FadeOut(state_point),
            FadeOut(traced_path),
            FadeOut(ke_rect),
            FadeOut(question),
            VGroup(
                ke_equation, xy_equation
            ).animate.arrange(DOWN, buff=0.5).next_to(plane, LEFT, buff=LARGE_BUFF),
        )
        underlines = VGroup(
            Underline(x_coef, buff=SMALL_BUFF),
            Underline(ke_equation["m_1"], buff=SMALL_BUFF),
        )
        underlines.set_color(YELLOW)

        l_squish_arrows = Vector(0.75 * RIGHT).get_grid(4, 1, v_buff=0.75)
        l_squish_arrows.next_to(plane.get_origin(), LEFT, buff=0.75)
        r_squish_arrows = l_squish_arrows.copy().flip(about_point=plane.get_origin())
        squish_arrows = VGroup(*l_squish_arrows, *r_squish_arrows)

        self.play(LaggedStartMap(GrowArrow, squish_arrows, lag_ratio=1e-2, run_time=1))
        self.play(
            ShowCreation(underlines, lag_ratio=0),
        )
        self.wait()
        self.play(FadeOut(squish_arrows), FadeOut(underlines))

        # Show the size of the ellipse
        marked_velocity.suspend_updating()
        E_rects = VGroup(
            SurroundingRectangle(ke_equation[R"\text{E}"], buff=SMALL_BUFF),
            SurroundingRectangle(xy_equation[R"\text{E}"], buff=SMALL_BUFF),
        )
        E_rects.set_stroke(YELLOW, 1)
        self.play(ShowCreation(E_rects, lag_ratio=0))
        self.play(
            marked_velocity.animate.set_value([-0.5, 0]),
            ellipse.animate.scale(0.25),
            rate_func=there_and_back,
            run_time=8,
        )
        self.play(FadeOut(E_rects))
        marked_velocity.resume_updating()

        # Show the experiment play out one more time
        traced_path = self.get_traced_path(state_point)
        self.add(traced_path, state_point)

        self.play(
            time_tracker.animate.set_value(20),
            run_time=20,
            rate_func=linear,
        )
        traced_path.clear_updaters()

        # Stretch into a circle
        state_point.clear_updaters()
        new_ke_eq = Tex(
            R"\left(\sqrt{m_1} \cdot v_1\right)^2 + \left(\sqrt{m_2} \cdot v_2\right)^2 = 2 \text{E}",
            **kw
        )
        new_xy_eq = Tex(R"x^2 + y^2 = 2\text{E}", **kw)
        new_xy_eq.scale(48 / 36)
        ke_equation.target = ke_equation.generate_target()
        stack = VGroup(
            ke_equation.target,
            new_ke_eq,
            new_xy_eq,
        )
        stack.arrange(DOWN, buff=0.5)
        stack.next_to(plane, LEFT, buff=1.0)

        self.play(
            Group(ellipse, traced_path, state_point).animate.stretch(math.sqrt(10), 0, about_point=plane.get_origin()),
            FadeOut(axis_labels, time_span=(0, 1)),
            LaggedStart(
                MoveToTarget(ke_equation),
                FadeOut(xy_equation, DOWN),
                FadeIn(new_ke_eq),
                FadeIn(new_xy_eq),
                lag_ratio=0.5,
            ),
            run_time=4
        )
        self.wait()

        # Highlight circle equation
        rect = SurroundingRectangle(new_xy_eq)
        rect.set_stroke(YELLOW, 2)
        words = Text("Equation for a circle", font_size=36)
        words.next_to(rect, DOWN)
        words.set_color(YELLOW)
        self.play(
            ShowCreation(rect),
            Write(words),
            run_time=1
        )
        self.wait()

        # Show new axis labels
        x_axis_label, y_axis_label = axis_labels = VGroup(
            Tex(R"x = \sqrt{m_1} \cdot v_1", **kw),
            Tex(R"y = \sqrt{m_2} \cdot v_2", **kw),
        )
        axis_labels.scale(30 / 36)
        x_axis_label.next_to(plane.x_axis.get_right(), DR, SMALL_BUFF)
        y_axis_label.next_to(plane.y_axis.get_top(), DR, SMALL_BUFF)

        x_rhs_tex = R"\sqrt{m_1} \cdot v_1"
        y_rhs_tex = R"\sqrt{m_2} \cdot v_2"

        rect2 = SurroundingRectangle(new_ke_eq[R"\left(\sqrt{m_1} \cdot v_1\right)^2"])
        rect2.match_style(rect)

        self.play(
            rect.animate.surround(new_xy_eq["x^2"]),
            FadeIn(rect2),
            FadeOut(words),
        )
        self.wait()
        self.play(
            TransformFromCopy(new_xy_eq["x"][0], x_axis_label["x"][0]),
            TransformFromCopy(new_ke_eq[x_rhs_tex][0], x_axis_label[x_rhs_tex][0]),
            Write(x_axis_label["="][0]),
            run_time=2
        )
        self.wait()

        self.play(
            rect.animate.surround(new_xy_eq["y^2"]),
            rect2.animate.surround(new_ke_eq[R"\left(\sqrt{m_2} \cdot v_2\right)^2"]),
        )
        self.wait()
        self.play(
            TransformFromCopy(new_xy_eq["y"][0], y_axis_label["y"][0]),
            TransformFromCopy(new_ke_eq[y_rhs_tex][0], y_axis_label[y_rhs_tex][0]),
            Write(y_axis_label["="][0]),
            run_time=2
        )
        self.wait()
        self.play(
            rect.animate.surround(new_xy_eq),
            rect2.animate.surround(VGroup(ke_equation, new_ke_eq)),
        )
        self.wait()
        self.play(FadeOut(rect), FadeOut(rect2))
        self.wait()

        # Roll back to the beginning once more
        state_point.add_updater(lambda m: m.move_to(
            plane.c2p(*state_tracker.get_scaled_block_velocities())
        ))

        self.play(
            time_tracker.animate.set_value(0),
            FadeOut(new_ke_eq),
            FadeOut(new_xy_eq),
            FadeOut(traced_path),
            run_time=4
        )

        # Shrinking circle
        if False:
            # For an insertion
            time_tracker.clear_updaters()
            time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
            last_n_collisions = state_tracker.get_n_collisions()

            ghost_circles = VGroup()
            self.add(ghost_circles)
            self.add(self.get_traced_path(state_point))
            for _ in range(10):
                self.wait_until(lambda: state_tracker.get_n_collisions() > last_n_collisions)
                ghost_circles.add(ellipse.copy().set_stroke(opacity=0.25))
                ellipse.scale(0.9)
                time_tracker.set_value(time_tracker.get_value() / 0.9)
                time_tracker.increment_value(1 / 30)
                state_tracker.state0[2:] *= 0.9
                last_n_collisions = state_tracker.get_n_collisions()

        # Show the regions of the state space
        region = Square()
        region.set_fill(RED, 0.25)
        region.set_stroke(RED, 0)
        region.replace(plane, stretch=True)
        region.stretch(0.5, 0, about_edge=LEFT)
        region.save_state()
        region.stretch(1e-5, 0, about_edge=RIGHT)

        self.play(Restore(region))
        self.wait()
        self.play(region.animate.stretch(0, 1).set_stroke(RED, 2))
        self.wait()
        self.play(region.animate.scale(0, about_point=state_point.get_center()))
        self.remove(region)
        self.wait()

        # Think through first collision
        self.play(time_tracker.animate.set_value(2), run_time=2, rate_func=linear)

        big_block_rect, lil_block_rect = rects = VGroup(
            SurroundingRectangle(Group(blocks[i], velocity_vectors[i]), buff=buff)
            for i, buff in zip([0, 1], [0.25, 0.1])
        )
        rects.set_stroke(RED, 2)
        x_rect, y_rect = xy_rects = Square().replicate(2)
        xy_rects.set_stroke(RED, width=0).set_fill(RED, 0.2)
        xy_rects.replace(plane, stretch=True)
        y_rect.stretch(0.5, 1, about_edge=DOWN)
        x_rect.stretch(0.05, 0, about_point=plane.c2p(-2.7, 0))

        self.wait()
        self.play(ShowCreation(lil_block_rect))
        self.wait()
        self.play(ReplacementTransform(lil_block_rect, y_rect))
        self.wait()
        self.play(ShowCreation(big_block_rect))
        self.wait()
        self.play(ReplacementTransform(big_block_rect, x_rect))
        self.play(x_rect.animate.shift(0.2 * RIGHT), run_time=4, rate_func=lambda t: wiggle(t, 5))
        self.wait()

        # Constrain to circle
        state_point.clear_updaters()
        marked_velocity.clear_updaters()
        marked_velocity.add_updater(
            lambda m: m.set_value(
                np.array(plane.p2c(state_point.get_center())) / state_tracker.sqrt_mass_vect
            )
        )
        arc = Arc(190 * DEG, 50 * DEG, radius=0.5 * ellipse.get_width(), arc_center=plane.get_center())
        arc.set_stroke(RED, 5)

        self.play(Rotate(state_point, TAU, about_point=plane.get_origin(), run_time=5))
        self.play(
            ReplacementTransform(x_rect, arc),
            ReplacementTransform(y_rect, arc),
        )
        self.play(
            Rotate(
                state_point,
                25 * DEG,
                about_point=plane.get_center(),
                rate_func=lambda t: wiggle(t, 5),
                run_time=8,
            )
        )
        self.wait()

        # Bring in conservation of momentum
        p_equation.next_to(ke_equation, DOWN)
        new_p_eq = Tex(
            R"\sqrt{m_1}\left(\sqrt{m_1} \cdot v_1\right) + \sqrt{m_2}\left(\sqrt{m_2} \cdot v_2\right) = P",
            **kw
        )
        new_p_eq.next_to(p_equation, DOWN, buff=0.75)
        p_xy_eq = Tex(R"\sqrt{m_1} x + \sqrt{m_2} y = P", **kw)
        p_xy_eq.next_to(new_p_eq, DOWN, buff=0.75)

        p1_rects, p2_rects = p_rects = VGroup(
            VGroup(
                SurroundingRectangle(p_equation[f"m_{i} v_{i}"]),
                SurroundingRectangle(p_xy_eq[Rf"\sqrt{{m_{i}}} {x}"]),
            )
            for i, x in [(1, "x"), (2, "y")]
        )
        p_rects.set_stroke(GREEN, 2)

        self.play(
            ke_equation.animate.to_edge(UP).set_opacity(0.33),
            FadeIn(p_equation),
        )
        self.wait()
        self.play(TransformMatchingTex(p_equation.copy(), new_p_eq))
        self.play(
            TransformMatchingTex(
                new_p_eq.copy(),
                p_xy_eq,
                key_map={
                    R"\left(\sqrt{m_1} \cdot v_1\right)": "x",
                    R"\left(\sqrt{m_2} \cdot v_2\right)": "y",
                }
            )
        )
        self.wait()
        self.play(ShowCreation(p1_rects, lag_ratio=0))
        self.wait()
        self.play(ReplacementTransform(p1_rects, p2_rects))
        self.wait()
        self.play(FadeOut(p2_rects))
        self.wait()

        # Show the momentum line
        p_line = Line(LEFT, RIGHT)
        p_line.set_width(6)
        p_line.set_stroke(GREEN, 3)
        p_line.rotate(-90 * DEG + state_tracker.theta)
        p_line.move_to(ellipse.get_left())

        slope_eq = Tex(R"\text{Slope} = -\sqrt{m_1 \over m_2}", font_size=36)
        slope_eq.next_to(p_line.pfp(0.6), RIGHT)

        self.play(
            ShowCreation(p_line),
            FadeOut(arc),
        )
        self.wait()
        self.play(Write(slope_eq))
        self.wait()
        self.play(FadeOut(slope_eq))
        self.play(
            Group(p_line, state_point).animate.shift(4 * RIGHT),
            run_time=8,
            rate_func=there_and_back,
        )
        self.wait()

        # Note the two intersection points
        point2 = state_point.get_center().copy()
        state_point.add_updater(lambda m: m.move_to(plane.c2p(*state_tracker.get_scaled_block_velocities())))
        self.play(time_tracker.animate.set_value(0), run_time=2)
        point1 = state_point.get_center().copy()
        self.wait()
        state_point.suspend_updating()

        intersection_arrows = VGroup(
            Vector(0.5 * DL).next_to(point, UR, buff=SMALL_BUFF)
            for point in [point1, point2]
        )

        self.play(
            state_point.animate.move_to(p_line.get_start()),
            rate_func=lambda t: wiggle(t, 5),
            run_time=8
        )
        self.wait()
        self.play(LaggedStartMap(GrowArrow, intersection_arrows, lag_ratio=0.5))
        self.wait()

        state_point.resume_updating()
        traced_path = self.get_traced_path(state_point)
        self.add(traced_path)
        self.play(time_tracker.animate.set_value(2), run_time=2, rate_func=linear)
        traced_path.suspend_updating()
        self.wait()
        self.play(
            FadeOut(intersection_arrows),
            FadeOut(new_p_eq),
            FadeOut(p_xy_eq),
            ke_equation.animate.set_opacity(1),
        )

        # Little block off wall
        traced_path.resume_updating()
        self.play(time_tracker.animate.set_value(7), run_time=5, rate_func=linear)
        traced_path.suspend_updating()
        self.wait()

        state_point.suspend_updating()
        self.play(
            state_point.animate.move_to(point2),
            rate_func=there_and_back,
            run_time=4,
        )
        self.wait()
        self.play(
            p_line.animate.move_to(plane.c2p(state_tracker.get_momentum() / math.sqrt(self.masses[0]))),
            run_time=2
        )
        self.wait()

        # Let play out for a while
        p_line.add_updater(
            lambda m: m.move_to(plane.c2p(state_tracker.get_momentum() / math.sqrt(self.masses[0])))
        )

        traced_path.resume_updating()
        state_point.resume_updating()

        self.play(
            time_tracker.animate.set_value(25),
            run_time=(25 - time_tracker.get_value()),
            rate_func=linear,
        )

        # Show the end zone
        endzone_line = Line(
            plane.get_origin(),
            plane.c2p(*(state_tracker.sqrt_mass_vect * 4)),
        )
        endzone_line.set_stroke(WHITE, 2)
        endzone = Polygon(
            endzone_line.get_end(),
            plane.get_origin(),
            plane.c2p(10, 0),
        )
        endzone.set_fill(GREEN, 0.25)
        endzone.set_stroke(width=0)

        ur_quadrant = Square(4.0)
        ur_quadrant.set_fill(GREEN, 0.25).set_stroke(width=0)
        ur_quadrant.move_to(plane.get_origin(), DL)

        endzone_line_label = Tex(R"v_1 = v_2", **kw)
        endzone_line_label.next_to(ORIGIN, UP, buff=SMALL_BUFF)
        slope_label = Tex(R"y = x \cdot \sqrt{m_2 / m_1}", **kw)
        slope_label.scale(20 / kw["font_size"])
        slope_label.next_to(ORIGIN, DOWN, SMALL_BUFF)

        VGroup(
            endzone_line_label, slope_label
        ).rotate(state_tracker.theta, about_point=ORIGIN).shift(endzone_line.pfp(0.45))

        time_tracker.clear_updaters()
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt))
        self.wait(5)
        self.play(FadeOut(p_line), FadeIn(ur_quadrant))
        self.wait(5)
        self.play(
            FadeOut(ur_quadrant),
            FadeIn(endzone)
        )
        self.wait(4)
        self.play(ShowCreation(endzone_line), Write(endzone_line_label))
        self.wait(2)
        self.play(Write(slope_label))
        self.wait(20)

    def get_floor_and_wall_2d(
        self,
        width=13,
        stroke_width=2,
        height=2,
        tick_spacing=0.5,
        tick_vect=0.25 * DL,
        buff_to_bottom=0.75,
    ):
        floor = Line(LEFT, RIGHT)
        floor.set_width(width)
        floor.center()
        floor.to_edge(DOWN, buff=buff_to_bottom)
        dl_point = floor.get_left()

        wall = Line(ORIGIN, UP)
        wall.set_height(height)
        wall.move_to(dl_point, DOWN)

        ticks = VGroup()
        for y in np.arange(tick_spacing, height + tick_spacing, tick_spacing):
            start = dl_point + y * UP
            ticks.add(Line(start, start + tick_vect))

        result = VGroup(floor, VGroup(wall, ticks))
        result.set_stroke(WHITE, stroke_width)

        return result

    def get_floor_and_wall_3d(
        self,
        buff_to_bottom=0.75,
        color=GREY_D,
        shading=(0.2, 0.2, 0.2)
    ):
        floor = Square3D(resolution=(20, 20))
        floor.rotate(90 * DEG, LEFT)
        floor.set_shape(self.floor_width, 0, self.floor_depth)
        floor.to_edge(DOWN, buff=buff_to_bottom)

        wall = Square3D()
        wall.rotate(90 * DEG, UP)
        wall.set_shape(0, self.wall_height, self.floor_depth)
        wall.move_to(floor.get_left(), DOWN)

        result = Group(floor, wall)
        result.set_color(color)
        result.set_shading(*shading)
        result.to_corner(DL)

        # CHANGE: this manimgl computes Surface normals in the shader from the mesh and the d_normal_point field no longer exists; the loop that forced the floor and wall normals is removed:
        # for part, vect in zip(result, [OUT, RIGHT]): part.data['d_normal_point'] = part.data['point'] + 1e-3 * vect

        return result

    def get_block_pair(self, floor, three_d=False):
        return Group(
            self.get_block(mass, color, width, floor, three_d=three_d)
            for mass, color, width in zip(self.masses, self.colors, self.widths)
        )

    def get_block(
        self,
        mass,
        color,
        width,
        floor,
        font_size=24,
        three_d=False,
        stroke_width=2,
        shading=None,
        floor_buff=0.01,
    ):
        if shading is None:
            shading = self.block_shading
        if three_d:
            body = Cube()
            body.set_color(color)
            body.set_shading(*shading)

            shell = VCube()
            shell.set_fill(opacity=0)
            shell.set_stroke(WHITE, width=1)
            shell.set_anti_alias_width(3)
            shell.replace(body)
            shell.apply_depth_test()
            shell.set_anti_alias_width(1)

            block = Group(body, shell)
        else:
            block = Square()
            block.set_stroke(WHITE, stroke_width)
            block.set_fill(color, 1)
            block.set_shading(*shading)

        block.set_width(width)
        block.next_to(floor, UP, buff=floor_buff)
        block.mass = mass

        mass_label = Tex(R"10 \, \text{kg}", font_size=font_size)
        mass_label.make_number_changeable("10", edge_to_fix=RIGHT).set_value(mass)
        mass_label.next_to(block, UP, buff=SMALL_BUFF)
        if three_d:
            mass_label.set_backstroke(BLACK, 1)

        block.add(mass_label)
        block.mass_label = mass_label

        return block

    def bind_blocks_to_state(self, blocks, floor, state_tracker):
        min_x = floor.get_x(LEFT) + blocks[1].get_width()

        def update_blocks(blocks):
            pos = state_tracker.get_block_positions()
            blocks[0].set_x(min_x + pos[0], LEFT)
            blocks[1].set_x(min_x + pos[1], RIGHT)

        blocks.add_updater(update_blocks)

    def get_velocity_vector(
        self,
        block,
        vel_function,
        thickness=2,
        scale_factor=0.5,
        color=RED,
        backstroke_width=1,
        label_backstroke_width=1,
        num_decimal_places=2,
        max_width=1.0,
        font_size=18
    ):
        vector = Vector(RIGHT, thickness=thickness)
        vector.set_fill(RED)
        vector.set_backstroke(BLACK, backstroke_width)

        def update_vector(vector):
            start = block[0].get_zenith() + 0.1 * DOWN
            vel = vel_function()
            width = max_width * math.tanh(scale_factor * vel)
            vector.put_start_and_end_on(start, start + width * RIGHT)
            return vector

        vector.add_updater(update_vector)

        label = DecimalNumber(
            0,
            num_decimal_places=num_decimal_places,
            font_size=font_size
        )
        label.set_fill(RED)
        label.set_backstroke(BLACK, label_backstroke_width)
        label.add_updater(lambda m: m.set_value(vel_function()).next_to(
            vector.get_start(), UP, buff=0.1
        ))
        # label.always.next_to(vector, UP, buff=0.05)
        # label.f_always.set_value(vel_function)

        return VGroup(vector, label)

    def get_traced_path(self, state_point):
        return TracedPath(state_point.get_center, stroke_color=RED, stroke_width=1)

    def check_for_clacks(self):
        n_collisions = self.state_tracker.get_n_collisions()

        if n_collisions == self.last_collision_count:
            return
        if n_collisions % 2 == 0:
            point = self.blocks[1][0].get_left()
        else:
            point = self.blocks[1][0].get_right()

        time_since = self.state_tracker.time_from_last_collision()

        if n_collisions > self.last_collision_count:
            flash = turn_animation_into_updater(ClackAnimation(point))
            flash.update(dt=time_since)
            flash.time = self.time - time_since
            self.flashes.append(flash)
            self.add(flash)

        sound_file = self.clack_sound if n_collisions > self.last_collision_count else self.reverse_clack_sound
        self.add_sound(sound_file, time_offset=-time_since)

        for flash in self.flashes:
            if flash.time < self.time - 0.25:
                self.remove(flash)
                self.flashes.remove(flash)

        self.last_collision_count = n_collisions

    def update_frame(self, dt=0, force_draw=False):
        if dt > 0 and self.listen_for_clacks:
            self.check_for_clacks()
        super().update_frame(dt, force_draw)


class BasicBlockCount(Blocks):
    initial_positions = [10, 7]
    initial_velocities = [-2, 0]
    masses = [10, 1]
    widths = [1.0, 0.5]
    colors = [BLUE_E, LITTLE_BLOCK_COLOR]
    total_time = 30
    field_of_view = 10 * DEG
    floor_width = 15
    floor_depth = 6
    wall_height = 5
    initial_orientation = (0, 0, 0)
    samples = 4

    def construct(self):
        self.add_count_label()
        self.frame.reorient(*self.initial_orientation)
        # Test

        self.play(
            self.time_tracker.animate.set_value(self.total_time),
            run_time=self.total_time,
            rate_func=linear,
        )

    def add_count_label(self):
        count_label = Tex(R"\# \text{Collisions} = 0")
        count = count_label.make_number_changeable("0")
        count.f_always.set_value(self.state_tracker.get_n_collisions)
        count_label.to_corner(UL)
        count_label.fix_in_frame()
        self.count_label = count_label
        self.add(count_label)


class ThumbnailShot(BasicBlockCount):
    initial_velocities = [-0.75, 0]
    masses = [int(1e6), 1]
    widths = [1.0, 0.5]
    initial_positions = [3, 2]
    colors = [BLUE_E, LITTLE_BLOCK_COLOR]
    floor_depth = 2
    wall_height = 2

    def construct(self):
        # Orient
        frame = self.frame
        frame.reorient(-40, -5, 0, (-3.45, -2.54, -0.34), 3.00)

        blocks = self.blocks
        blocks.deactivate_depth_test()
        for block in blocks:
            block[2].set_opacity(0).scale(0, about_point=block[0].get_top())
            for cube in block[:2]:
                cube[1].set_opacity(0)
                cube[2].set_opacity(0)
                cube[5].set_opacity(0)

        # Add speed lines
        speed_lines = Line(ORIGIN, 1.5 * RIGHT).get_grid(7, 1)
        speed_lines.set_stroke(YELLOW, width=(5, 0))
        speed_lines.arrange_to_fit_height(0.8 * blocks[0][0].get_height())
        speed_lines.next_to(blocks[0][0], RIGHT, buff=0.05, aligned_edge=OUT)

        self.add(speed_lines)

        lil_speed_lines = speed_lines[1:-1].copy()
        lil_speed_lines.flip()
        lil_speed_lines.set_shape(0.8, 0.3)
        lil_speed_lines.next_to(blocks[1], LEFT, buff=0.05)
        self.add(lil_speed_lines)

        # Test

    def old(self):
        # Add ghosts
        block_template = blocks[0].copy()
        block_template.clear_updaters()
        for a in np.linspace(0, 1, 4):
            ghost_block = block_template.copy()
            ghost_block.set_opacity(interpolate(0.9, 0.1, a))
            ghost_block.shift(a * 2 * RIGHT)
            self.add(ghost_block)
        self.add(blocks)
