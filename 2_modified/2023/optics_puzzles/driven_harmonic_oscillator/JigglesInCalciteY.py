# ==============================================================================
# Scene:      JigglesInCalciteY
# Source:     videos/_2023/optics_puzzles/driven_harmonic_oscillator.py (lines 1134-1135)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl JigglesInCalciteY.py JigglesInCalciteY -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField


# ----- From _2023/optics_puzzles/objects.py -----

class Molecule(Group):
    # List of characters
    atoms = []

    # List of 3d coordinates
    coordinates = np.zeros((0, 3))

    # List of pairs of indices
    bonds = []

    atom_to_color = {
        "H": WHITE,
        "O": RED,
        "C": GREY,
    }
    atom_to_radius = {
        "H": 0.1,
        "O": 0.2,
        "C": 0.19,
    }
    ball_config = dict(shading=(0.25, 0.5, 0.5), glow_factor=0.25)
    stick_config = dict(stroke_width=1, stroke_color=GREY_A, flat_stroke=False)

    def __init__(self, height=2.0, **kwargs):
        coords = np.array(self.coordinates)
        radii = np.array([self.atom_to_radius[atom] for atom in self.atoms])
        rgbas = np.array([color_to_rgba(self.atom_to_color[atom]) for atom in self.atoms])

        balls = DotCloud(coords, **self.ball_config)
        balls.set_radii(radii)
        balls.set_rgba_array(rgbas)

        sticks = VGroup()
        for i, j in self.bonds:
            c1, c2 = coords[[i, j], :]
            r1, r2 = radii[[i, j]]
            unit_vect = normalize(c2 - c1)

            sticks.add(Line(
                c1 + r1 * unit_vect, c2 - r2 * unit_vect,
                **self.stick_config
            ))

        super().__init__(balls, sticks, **kwargs)

        self.apply_depth_test()
        self.balls = balls
        self.sticks = sticks
        self.set_height(height)


class Calcite(Molecule):
    atoms = [
        "C", "C", "Ca", "C", "O", "O", "C", "Ca", "C", "O", "O", "O", "Ca", "C", "O", "O", "C", "Ca", "C", "O", "C", "Ca", "C", "O", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "C", "Ca", "C", "O", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "O", "C", "C", "Ca", "C", "O", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "C", "Ca", "C", "O", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "O", "Ca", "C", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "O", "Ca", "C", "O", "O", "O", "Ca", "C", "O", "Ca", "C", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "Ca", "C", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "O", "Ca", "Ca", "C", "O", "O", "O", "O", "O", "Ca", "C", "O", "O", "O", "O", "O", "O", 
    ]
    atom_to_color = {
        "Ca": GREEN,
        "O": RED,
        "C": GREY,
    }
    atom_to_radius = {
        "Ca": 0.25,
        "O": 0.2,
        "C": 0.19,
    }

    coordinates = np.array([
        [-1.43769337, -2.49015797,  1.41822405],
        [-1.43769337,  2.49015797,  1.41822405],
        [-2.87538675,   .00000000,  2.83644809],
        [-2.87538675,   .00000000,  7.09112022],
        [-2.48577184,  1.88504958,  1.41822404],
        [-1.43769337, -1.27994119,  1.41822404],
        [-1.43769337,  7.47047390,  1.41822405],
        [-2.87538675,  4.98031594,  2.83644809],
        [-2.87538675,  4.98031594,  7.09112022],
        [-2.48577184,  6.86536552,  1.41822404],
        [-1.43769337,  3.70037474,  1.41822404],
        [-2.87538675,  1.21021677,  7.09112022],
        [-2.87538675,  9.96063187,  2.83644809],
        [-2.87538675,  9.96063187,  7.09112022],
        [-1.43769337,  8.68069068,  1.41822404],
        [-2.87538675,  6.19053271,  7.09112022],
        [ 2.87538675,   .00000000,  1.41822405],
        [ 1.43769337, -2.49015797,  2.83644809],
        [ 1.43769337, -2.49015797,  7.09112022],
        [ 1.82730828,  -.60510839,  1.41822404],
        [ 2.87538675,  4.98031594,  1.41822405],
        [ 1.43769337,  2.49015797,  2.83644809],
        [ 1.43769337,  2.49015797,  7.09112022],
        [ -.38961490,  1.88504958,  1.41822404],
        [ 1.82730828,  4.37520755,  1.41822404],
        [ 2.87538675,  1.21021677,  1.41822404],
        [  .00000000,   .00000000,   .00000000],
        [  .00000000,   .00000000,  8.50934427],
        [  .00000000,   .00000000,  4.25467213],
        [-1.04807847,   .60510839,  4.25467213],
        [ 1.04807847,   .60510839,  4.25467213],
        [  .00000000, -1.21021677,  4.25467213],
        [-1.82730828,  -.60510839,  7.09112022],
        [  .38961490,  1.88504958,  7.09112022],
        [ 1.43769337, -1.27994119,  7.09112022],
        [-1.43769337, -2.49015797,  5.67289618],
        [-1.43769337, -2.49015797,  9.92756831],
        [-2.48577184, -1.88504958,  9.92756831],
        [ -.38961490, -1.88504958,  9.92756831],
        [ 2.87538675,  9.96063187,  1.41822405],
        [ 1.43769337,  7.47047390,  2.83644809],
        [ 1.43769337,  7.47047390,  7.09112022],
        [ -.38961490,  6.86536552,  1.41822404],
        [ 1.82730828,  9.35552349,  1.41822404],
        [ 2.87538675,  6.19053271,  1.41822404],
        [  .00000000,  4.98031594,   .00000000],
        [  .00000000,  4.98031594,  8.50934427],
        [  .00000000,  4.98031594,  4.25467213],
        [-1.04807847,  5.58542432,  4.25467213],
        [ 1.04807847,  5.58542432,  4.25467213],
        [  .00000000,  3.77009916,  4.25467213],
        [-1.82730828,  4.37520755,  7.09112022],
        [  .38961490,  6.86536552,  7.09112022],
        [ 1.43769337,  3.70037474,  7.09112022],
        [-1.43769337,  2.49015797,  5.67289618],
        [-1.43769337,  2.49015797,  9.92756831],
        [-2.48577184,  3.09526635,  9.92756831],
        [ -.38961490,  3.09526635,  9.92756831],
        [-1.43769337,  1.27994120,  9.92756831],
        [  .00000000,  9.96063187,   .00000000],
        [  .00000000,  9.96063187,  8.50934427],
        [  .00000000,  9.96063187,  4.25467213],
        [-1.04807847, 10.56574026,  4.25467213],
        [ 1.04807847, 10.56574026,  4.25467213],
        [  .00000000,  8.75041510,  4.25467213],
        [-1.82730828,  9.35552349,  7.09112022],
        [ 1.43769337,  8.68069068,  7.09112022],
        [-1.43769337,  7.47047390,  5.67289618],
        [-1.43769337,  7.47047390,  9.92756831],
        [-2.48577184,  8.07558229,  9.92756831],
        [ -.38961490,  8.07558229,  9.92756831],
        [-1.43769337,  6.26025713,  9.92756831],
        [ 7.18846687, -2.49015797,  1.41822405],
        [ 7.18846687,  2.49015797,  1.41822405],
        [ 5.75077349,   .00000000,  2.83644809],
        [ 5.75077349,   .00000000,  7.09112022],
        [ 3.92346522,  -.60510839,  1.41822404],
        [ 6.14038840,  1.88504958,  1.41822404],
        [ 7.18846687, -1.27994119,  1.41822404],
        [ 4.31308012, -2.49015797,   .00000000],
        [ 4.31308012, -2.49015797,  8.50934427],
        [ 4.31308012, -2.49015797,  4.25467213],
        [ 3.26500165, -1.88504958,  4.25467213],
        [ 5.36115859, -1.88504958,  4.25467213],
        [ 4.70269502,  -.60510839,  7.09112022],
        [ 7.18846687,  7.47047390,  1.41822405],
        [ 5.75077349,  4.98031594,  2.83644809],
        [ 5.75077349,  4.98031594,  7.09112022],
        [ 3.92346522,  4.37520755,  1.41822404],
        [ 6.14038840,  6.86536552,  1.41822404],
        [ 7.18846687,  3.70037474,  1.41822404],
        [ 4.31308012,  2.49015797,   .00000000],
        [ 4.31308012,  2.49015797,  8.50934427],
        [ 4.31308012,  2.49015797,  4.25467213],
        [ 3.26500165,  3.09526635,  4.25467213],
        [ 5.36115859,  3.09526635,  4.25467213],
        [ 4.31308012,  1.27994120,  4.25467213],
        [ 2.48577184,  1.88504958,  7.09112022],
        [ 4.70269502,  4.37520755,  7.09112022],
        [ 5.75077349,  1.21021677,  7.09112022],
        [ 2.87538675,   .00000000,  5.67289618],
        [ 2.87538675,   .00000000,  9.92756831],
        [ 1.82730828,   .60510839,  9.92756831],
        [ 3.92346522,   .60510839,  9.92756831],
        [ 2.87538675, -1.21021677,  9.92756831],
        [ 5.75077349,  9.96063187,  2.83644809],
        [ 5.75077349,  9.96063187,  7.09112022],
        [ 3.92346522,  9.35552349,  1.41822404],
        [ 7.18846687,  8.68069068,  1.41822404],
        [ 4.31308012,  7.47047390,   .00000000],
        [ 4.31308012,  7.47047390,  8.50934427],
        [ 4.31308012,  7.47047390,  4.25467213],
        [ 3.26500165,  8.07558229,  4.25467213],
        [ 5.36115859,  8.07558229,  4.25467213],
        [ 4.31308012,  6.26025713,  4.25467213],
        [ 2.48577184,  6.86536552,  7.09112022],
        [ 4.70269502,  9.35552349,  7.09112022],
        [ 5.75077349,  6.19053271,  7.09112022],
        [ 2.87538675,  4.98031594,  5.67289618],
        [ 2.87538675,  4.98031594,  9.92756831],
        [ 1.82730828,  5.58542432,  9.92756831],
        [ 3.92346522,  5.58542432,  9.92756831],
        [ 2.87538675,  3.77009916,  9.92756831],
        [ 2.87538675,  9.96063187,  5.67289618],
        [ 2.87538675,  9.96063187,  9.92756831],
        [ 1.82730828, 10.56574026,  9.92756831],
        [ 3.92346522, 10.56574026,  9.92756831],
        [ 2.87538675,  8.75041510,  9.92756831],
        [10.06385361, -2.49015797,  2.83644809],
        [10.06385361, -2.49015797,  7.09112022],
        [10.45346852,  -.60510839,  1.41822404],
        [10.06385361,  2.49015797,  2.83644809],
        [10.06385361,  2.49015797,  7.09112022],
        [ 8.23654533,  1.88504958,  1.41822404],
        [10.45346852,  4.37520755,  1.41822404],
        [ 8.62616024,   .00000000,   .00000000],
        [ 8.62616024,   .00000000,  8.50934427],
        [ 8.62616024,   .00000000,  4.25467213],
        [ 7.57808177,   .60510839,  4.25467213],
        [ 9.67423871,   .60510839,  4.25467213],
        [ 8.62616024, -1.21021677,  4.25467213],
        [ 6.79885196,  -.60510839,  7.09112022],
        [ 9.01577514,  1.88504958,  7.09112022],
        [10.06385361, -1.27994119,  7.09112022],
        [ 7.18846687, -2.49015797,  5.67289618],
        [ 7.18846687, -2.49015797,  9.92756831],
        [ 6.14038840, -1.88504958,  9.92756831],
        [ 8.23654533, -1.88504958,  9.92756831],
        [10.06385361,  7.47047390,  2.83644809],
        [10.06385361,  7.47047390,  7.09112022],
        [ 8.23654533,  6.86536552,  1.41822404],
        [10.45346852,  9.35552349,  1.41822404],
        [ 8.62616024,  4.98031594,   .00000000],
        [ 8.62616024,  4.98031594,  8.50934427],
        [ 8.62616024,  4.98031594,  4.25467213],
        [ 7.57808177,  5.58542432,  4.25467213],
        [ 9.67423871,  5.58542432,  4.25467213],
        [ 8.62616024,  3.77009916,  4.25467213],
        [ 6.79885196,  4.37520755,  7.09112022],
        [ 9.01577514,  6.86536552,  7.09112022],
        [10.06385361,  3.70037474,  7.09112022],
        [ 7.18846687,  2.49015797,  5.67289618],
        [ 7.18846687,  2.49015797,  9.92756831],
        [ 6.14038840,  3.09526635,  9.92756831],
        [ 8.23654533,  3.09526635,  9.92756831],
        [ 7.18846687,  1.27994120,  9.92756831],
        [ 8.62616024,  9.96063187,   .00000000],
        [ 8.62616024,  9.96063187,  8.50934427],
        [ 8.62616024,  9.96063187,  4.25467213],
        [ 7.57808177, 10.56574026,  4.25467213],
        [ 9.67423871, 10.56574026,  4.25467213],
        [ 8.62616024,  8.75041510,  4.25467213],
        [ 6.79885196,  9.35552349,  7.09112022],
        [10.06385361,  8.68069068,  7.09112022],
        [ 7.18846687,  7.47047390,  5.67289618],
        [ 7.18846687,  7.47047390,  9.92756831],
        [ 6.14038840,  8.07558229,  9.92756831],
        [ 8.23654533,  8.07558229,  9.92756831],
        [ 7.18846687,  6.26025713,  9.92756831],
        [10.45346852,   .60510839,  9.92756831],
        [10.45346852,  5.58542432,  9.92756831],
        [10.45346852, 10.56574026,  9.92756831],
    ])



# ----- From _2023/optics_puzzles/driven_harmonic_oscillator.py -----

class HarmonicOscillator(TrueDot):
    def __init__(
        self,
        center=np.zeros(3),
        initial_velocity=np.zeros(3),
        k=20.0,
        damping=0.1,
        mass=1.0,
        radius=0.5,
        color=BLUE,
        three_d=True,
        **kwargs
    ):
        self.k = k
        self.mass = mass
        self.damping = damping
        self.velocity = initial_velocity
        self.center_of_attraction = center
        self.external_forces = []

        super().__init__(
            radius=radius,
            color=color,
            **kwargs
        )
        if three_d:
            self.make_3d()
        self.move_to(center)
        self.add_updater(lambda m, dt: self.update_position(dt))

    def update_position(self, dt):
        time_step = 1 / 300
        n_divisions = max(int(dt / time_step), 1)
        true_step = dt / n_divisions
        for _ in range(n_divisions):
            self.velocity += self.get_acceleration() * true_step
            self.shift(self.velocity * true_step)

    def get_displacement(self):
        return self.get_center() - self.center_of_attraction

    def get_acceleration(self):
        disp = self.get_displacement()
        result = -self.k * disp / self.mass - self.damping * self.velocity
        for force in self.external_forces:
            result += force() / self.mass
        return result

    def reset_velocity(self):
        self.velocity = 0

    def set_damping(self, damping):
        self.damping = damping

    def set_k(self, k):
        self.k = k
        return self

    def suspend_updating(self):
        super().suspend_updating()
        self.reset_velocity()

    def set_external_forces(self, funcs):
        self.external_forces = list(funcs)
        return self

    def add_external_force(self, func):
        self.external_forces.append(func)
        return self


class Spring(VMobject):
    def __init__(
        self, mobject, base_point,
        edge=ORIGIN,
        stroke_color=GREY,
        stroke_width=2,
        twist_rate=8.0,
        n_twists=8,
        radius=0.1,
        lead_length=0.25,
        **kwargs
    ):
        super().__init__(**kwargs)

        helix = ParametricCurve(
            lambda t: [
                radius * math.cos(TAU * t),
                radius * math.sin(TAU * t),
                t / twist_rate
            ],
            t_range=(0, n_twists, 0.01)
        )
        helix.rotate(PI / 2, UP)
        # helix.make_jagged()

        self.start_new_path(helix.get_start() + lead_length * LEFT)
        self.add_line_to(helix.get_start())
        self.append_vectorized_mobject(helix)
        self.add_line_to(helix.get_end() + lead_length * RIGHT)

        self.set_stroke(color=stroke_color, width=stroke_width)
        self.set_flat_stroke(False)

        reference_points = self.get_points().copy()
        width = self.get_width()
        self.add_updater(lambda m: m.set_points(reference_points))
        self.add_updater(lambda m: m.stretch(
            get_norm(base_point - mobject.get_edge_center(edge)) / width, 0
        ))
        self.add_updater(lambda m: m.put_start_and_end_on(
            base_point, mobject.get_edge_center(edge)
        ))

    def get_length(self):
        return get_norm(self.get_end() - self.get_start())


class JigglesInCalcite(InteractiveScene):
    polarization_direction = 1

    def construct(self):
        # Set up crystal
        calcite = Calcite(height=8)
        calcite.center()

        index = 118
        calcium_center = calcite.balls.get_points()[index]
        radii = calcite.balls.get_radii()
        radii[index] = 0
        calcite.balls.set_radii(radii)

        calcium = HarmonicOscillator(center=calcium_center)
        calcium.set_radius(np.max(radii))
        calcium.set_color(GREEN)
        calcium.set_glow_factor(calcite.balls.get_glow_factor())
        calcium.move_to(calcium_center)

        self.add(calcite, calcium)

        # Initial panning
        frame = self.frame
        frame.reorient(12, 64, 0).move_to([0.21, -0.18, -0.77]).set_height(9)
        self.play(
            frame.animate.reorient(1, 84, 0).move_to([-0.08, -0.16, -0.53]).set_height(9),
            run_time=3
        )
        self.wait()

        # Add springs
        spring_length = 2.5
        springs = VGroup(
            *(
                Spring(
                    calcium,
                    calcium.get_center() + spring_length * (v_vect + 0.2 * h_vect),
                    edge=v_vect
                )
                for v_vect in [UP, DOWN]
                for h_vect in [LEFT, ORIGIN, RIGHT]
            ),
            *(
                Spring(
                    calcium,
                    calcium.get_center() + spring_length * h_vect,
                    edge=h_vect
                )
                for h_vect in [LEFT, RIGHT]
            )
        )
        springs.set_stroke(opacity=0.7)
        self.play(
            VFadeIn(springs),
            calcium.animate.shift(RIGHT),
            calcite.balls.animate.set_opacity(0.1),
            frame.animate.reorient(-2, 25, 0).move_to(calcium).set_height(6),
            run_time=2,
        )

        # Show two resonant frequencies
        def wait_until_centered():
            disp = calcium.get_displacement()
            self.wait_until(lambda: np.dot(calcium.get_displacement(), disp) <= 0)
            calcium.move_to(calcium_center)
            calcium.reset_velocity()

        for vect, k in [(RIGHT, 5), (UP, 30)]:
            self.play(calcium.animate.move_to(calcium_center + vect), run_time=0.5)
            calcium.reset_velocity()
            calcium.set_k(k)
            self.wait(6)
            wait_until_centered()

        # Shine in light
        omega = -4.0
        F_max = 1.0
        wave_number = 2.0

        def time_func(points, time):
            result = np.zeros(points.shape)
            result[:, self.polarization_direction] = F_max * np.cos(wave_number * points[:, 2] - omega * time)
            return result

        field_config = dict(
            stroke_color=TEAL,
            stroke_width=3,
            stroke_opacity=0.5,
            max_vect_len=1.0,
            x_density=1.0,
            y_density=1.0,
            center=calcium_center,
        )
        z_axis_field = TimeVaryingVectorField(
            time_func,
            height=0, width=0, depth=16,
            z_density=5,
            **field_config
        )

        z_axis_field.set_stroke(opacity=0.5)

        calcium.set_k([5, 30][self.polarization_direction])
        calcium.set_damping(1)
        calcium.set_external_forces([
            lambda: 3 * z_axis_field.func(np.array([calcium_center]))[0]
        ])

        self.play(
            VFadeIn(z_axis_field),
            frame.animate.reorient(108, 46, -102).move_to(calcium).set_height(12),
            run_time=3
        )
        self.wait(25)


class JigglesInCalciteY(JigglesInCalcite):
    polarization_direction = 0
