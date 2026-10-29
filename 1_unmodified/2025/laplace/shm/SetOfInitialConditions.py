# ==============================================================================
# Scene:      SetOfInitialConditions
# Source:     videos/_2025/laplace/shm.py (lines 1563-1747)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SetOfInitialConditions.py SetOfInitialConditions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SrpingMassSystem(VGroup):
    def __init__(
        self,
        x0=0,
        v0=0,
        k=3,
        mu=0.1,
        equilibrium_length=7,
        equilibrium_position=ORIGIN,
        direction=RIGHT,
        spring_stroke_color=GREY_B,
        spring_stroke_width=2,
        spring_radius=0.25,
        n_spring_curls=8,
        mass_width=1.0,
        mass_color=BLUE_E,
        mass_label="m",
        external_force=None,
    ):
        super().__init__()
        self.equilibrium_position = equilibrium_position
        self.fixed_spring_point = equilibrium_position - (equilibrium_length - 0.5 * mass_width) * direction
        self.direction = direction
        self.rot_off_horizontal = angle_between_vectors(RIGHT, direction)
        self.mass = self.get_mass(mass_width, mass_color, mass_label)
        self.spring = self.get_spring(spring_stroke_color, spring_stroke_width, n_spring_curls, spring_radius)
        self.add(self.spring, self.mass)

        self.k = k
        self.mu = mu
        self.set_x(x0)
        self.velocity = v0

        self.external_force = external_force

        self._is_running = True
        self.add_updater(lambda m, dt: m.time_step(dt))

    def get_spring(self, stroke_color, stroke_width, n_curls, radius):
        spring = ParametricCurve(
            lambda t: [t, -radius * math.sin(TAU * t), radius * math.cos(TAU * t)],
            t_range=(0, n_curls, 1e-2),
            stroke_color=stroke_color,
            stroke_width=stroke_width,
        )
        spring.rotate(self.rot_off_horizontal)
        return spring

    def get_mass(self, mass_width, mass_color, mass_label):
        mass = Square(mass_width)
        mass.set_fill(mass_color, 1)
        mass.set_stroke(WHITE, 1)
        mass.set_shading(0.1, 0.1, 0.1)
        label = Tex(mass_label)
        label.set_max_width(0.5 * mass.get_width())
        label.move_to(mass)
        mass.add(label)
        mass.label = label
        return mass

    def set_x(self, x):
        self.mass.move_to(self.equilibrium_position + x * self.direction)
        spring_width = SMALL_BUFF + get_norm(self.mass.get_left() - self.fixed_spring_point)
        self.spring.rotate(-self.rot_off_horizontal)
        self.spring.set_width(spring_width, stretch=True)
        self.spring.rotate(self.rot_off_horizontal)
        self.spring.move_to(self.fixed_spring_point, -self.direction)

    def get_x(self):
        return (self.mass.get_center() - self.equilibrium_position)[0]

    def time_step(self, delta_t, dt_size=1e-3):
        if not self._is_running:
            return
        if delta_t == 0:
            return

        state = [self.get_x(), self.velocity]
        sub_steps = max(int(delta_t / dt_size), 1)
        true_dt = delta_t / sub_steps
        for _ in range(sub_steps):
            # ODE
            x, v = state
            state += np.array([v, self.get_force(x, v)]) * true_dt

        self.set_x(state[0])
        self.velocity = state[1]

    def pause(self):
        self._is_running = False

    def unpause(self):
        self._is_running = True

    def set_k(self, k):
        self.k = k
        return self

    def set_mu(self, mu):
        self.mu = mu
        return self

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        return self

    def get_velocity_vector(self, scale_factor=0.5, thickness=3.0, v_offset=-0.25, color=GREEN):
        """Get a vector showing the mass's velocity"""
        vector = Vector(RIGHT, fill_color=color)
        v_shift = v_offset * UP
        vector.add_updater(lambda m: m.put_start_and_end_on(
            self.mass.get_center() + v_shift,
            self.mass.get_center() + v_shift + scale_factor * self.velocity * RIGHT
        ))
        return vector

    def get_force_vector(self, scale_factor=0.5, thickness=3.0, v_offset=-0.25, color=RED):
        """Get a vector showing the mass's velocity"""
        vector = Vector(RIGHT, fill_color=color)
        v_shift = v_offset * UP
        vector.add_updater(lambda m: m.put_start_and_end_on(
            self.mass.get_center() + v_shift,
            self.mass.get_center() + v_shift + scale_factor * self.get_force(self.get_x(), self.velocity) * RIGHT
        ))
        return vector

    def add_external_force(self, func):
        self.external_force = func

    def get_force(self, x, v):
        force = -self.k * x - self.mu * v
        if self.external_force is not None:
            force += self.external_force()
        return force


class SetOfInitialConditions(InteractiveScene):
    graph_time = 8

    def construct(self):
        # Set up all boxes
        frame = self.frame
        box = Rectangle(width=3.5, height=2.0)
        box.set_stroke(WHITE, 1)
        v_line = DashedLine(box.get_top(), box.get_bottom())
        v_line.set_stroke(GREY_C, 1, 0.5)
        v_line.scale(0.9)
        box.add(v_line)

        n_rows = 5
        n_cols = 5
        box_row = box.get_grid(1, n_cols, buff=0)
        box_grid = box_row.get_grid(n_rows, 1, buff=0)
        for row, v0 in zip(box_grid, np.linspace(1, -1, n_rows)):
            for box, x0 in zip(row, np.linspace(-1, 1, n_cols)):
                box.spring = self.get_spring_in_a_box(box, x0=x0, v0=v0)

        # Show the first example
        mid_row = box_grid[n_rows // 2]
        x0_labels = VGroup(
            Tex(Rf"x_0 = {x0}", font_size=48).next_to(box, UP, SMALL_BUFF)
            for x0, box in zip(range(-2, 3), mid_row)
        )
        mid_row_springs = VGroup(box.spring for box in mid_row)

        mid_row_solutions = VGroup(
            self.get_solution_graph(box, x0=x0)
            for box, x0 in zip(mid_row, range(-2, 3))
        )
        last_solution = mid_row_solutions[-1]

        last_box = mid_row[-1]
        last_spring = last_box.spring
        top_line = Line(last_box.get_center(), last_spring.mass.get_center())
        top_line.set_y(last_spring.mass.get_y(UP))
        brace = LineBrace(Line(ORIGIN, 1.5 * RIGHT))
        brace.match_width(top_line)
        brace.next_to(top_line, UP, SMALL_BUFF)
        brace.stretch(0.5, 1, about_edge=DOWN)
        last_x = last_spring.get_x()
        last_spring.set_x(0)

        self.add(last_box, last_spring)
        frame.move_to(mid_row[-1]).set_height(5)

        self.play(
            GrowFromPoint(brace, brace.get_left()),
            last_spring.animate.set_x(last_x),
            Write(x0_labels[-1]),
        )
        self.wait()
        last_spring.unpause()
        last_spring.v_vect.set_opacity(0)
        self.play(
            frame.animate.reorient(0, 0, 0, (6.7, -0.61, 0.0), 6.16).set_anim_args(run_time=2),
            FadeIn(last_solution[0]),
            ShowCreation(last_solution[1], rate_func=linear, run_time=self.graph_time)
        )
        last_spring.pause()

        # Show the full middle row
        self.play(
            frame.animate.center().set_width(box_grid.get_width() + 2).set_anim_args(time_span=(0, 1.5)),
            last_spring.animate.set_x(1).set_anim_args(time_span=(0, 1)),
            LaggedStartMap(FadeIn, VGroup(*reversed(mid_row[:-1])), lag_ratio=0.75),
            LaggedStartMap(FadeIn, VGroup(*reversed(mid_row_springs[:-1])), lag_ratio=0.75),
            LaggedStartMap(FadeIn, VGroup(*reversed(x0_labels[:-1])), lag_ratio=0.75),
            LaggedStartMap(FadeIn, VGroup(*reversed(mid_row_solutions[:-1])), lag_ratio=0.75),
            run_time=3
        )
        self.wait()

        graphs = VGroup(solution[1] for solution in mid_row_solutions)
        faint_graphs = graphs.copy().set_stroke(width=1, opacity=0.25)
        for spring in mid_row_springs:
            spring.unpause()
            spring.v_vect.set_opacity(0)
            spring.x0 = spring.get_x()
        self.add(faint_graphs)
        self.play(
            ShowCreation(graphs, lag_ratio=0, run_time=self.graph_time, rate_func=linear),
        )
        self.wait()
        self.remove(faint_graphs)
        for spring in mid_row_springs:
            spring.pause()
            spring.v_vect.set_opacity(0)
            spring.set_velocity(0)
        self.play(
            FadeOut(mid_row_solutions),
            *(spring.animate.set_x(spring.x0) for spring in mid_row_springs)
        )

        # Show initial velocities
        v0_labels = VGroup(
            Tex(Rf"v_0 = {v0}", font_size=48).next_to(row, LEFT).set_fill(TEAL)
            for v0, row in zip(range(2, -3, -1), box_grid)
        )
        other_indices = [0, 1, 3, 4]
        row_springs = VGroup(VGroup(box.spring for box in row) for row in box_grid)

        self.play(
            frame.animate.set_width(box_grid.get_width() + 3, about_edge=DR),
            Write(v0_labels[2])
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, VGroup(box_grid[i] for i in other_indices), lag_ratio=0.5, run_time=3),
            LaggedStartMap(FadeIn, VGroup(v0_labels[i] for i in other_indices), lag_ratio=0.5, run_time=3),
            LaggedStartMap(FadeIn, VGroup(row_springs[i] for i in other_indices), lag_ratio=0.5, run_time=3),
            x0_labels.animate.next_to(box_grid, UP, SMALL_BUFF).set_anim_args(run_time=1),
            FadeOut(brace),
        )
        self.wait()

        # Let it play
        for row in box_grid:
            for box in row:
                box.spring.unpause()

        self.wait(20)

        # Add graphs
        all_solutions = VGroup(
            self.get_solution_graph(box, x0=x0, v0=v0, graph_color=YELLOW).move_to(box).scale(0.8)
            for row, v0 in zip(box_grid, range(2, -3, -1))
            for box, x0 in zip(row, range(-2, 3))
        )
        all_axes = VGroup(s[0] for s in all_solutions)
        all_graphs = VGroup(s[1] for s in all_solutions)

        self.remove(*(box.spring for row in box_grid for box in row))
        self.add(all_axes)
        self.play(ShowCreation(all_graphs, lag_ratio=1e-1, run_time=3))
        self.wait()

        # Highlight one
        highlight = all_solutions[14].copy()
        self.add(highlight)
        self.play(all_solutions.animate.fade(0.75))
        self.wait()

    def get_spring_in_a_box(self, box, x0=0, v0=0, k=9, mu=0.5):
        box_width = box.get_width()
        spring = SrpingMassSystem(
            x0=x0,
            v0=v0,
            k=k,
            mu=mu,
            mass_width=0.1 * box_width,
            equilibrium_length=0.5 * box_width,
            equilibrium_position=box.get_center(),
            spring_radius=0.035 * box_width,
        )
        v_vect = spring.get_velocity_vector(v_offset=-box_width * 0.1, scale_factor=0.5)
        spring.add(v_vect)
        spring.v_vect = v_vect
        spring.pause()
        return spring

    def get_solution_graph(self, box, x0=2, v0=0, k=9, mu=0.5, width_factor=0.8, graph_color=TEAL):
        axes = Axes(
            x_range=(0, self.graph_time, 1),
            y_range=(-2, 2),
            width=width_factor * box.get_width(),
            height=box.get_height(),
        )
        axes.set_stroke(GREY, 1)
        axes.next_to(box, DOWN)

        s = 0.5 * (-mu + 1j * math.sqrt(4 * k - mu**2))
        z0 = complex(
            x0,
            (s.real * x0 - v0) / s.imag
        )

        graph = axes.get_graph(
            lambda t: (z0 * np.exp(s * t)).real,
        )
        graph.set_stroke(graph_color, 2)
        return VGroup(axes, graph)
