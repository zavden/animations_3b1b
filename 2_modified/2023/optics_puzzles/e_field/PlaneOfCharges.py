# ==============================================================================
# Scene:      PlaneOfCharges
# Source:     videos/_2023/optics_puzzles/e_field.py (lines 1430-1455)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl PlaneOfCharges.py PlaneOfCharges -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
#   - ChargedParticle.update(dt, recurse) did not accept frame_rate, which manimgl passes since PR #2481 (TypeError); the parameter was added
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField
from typing import TYPE_CHECKING


# ----- From _2023/optics_puzzles/objects.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3


def points_to_particle_info(particle, points, radius=None, c=2.0):
    """
    Given an origin, a set of points, and a radius, this returns:

    1) The unit vectors directed from the origin to each point

    2) The distances from the origin to each point

    3) An adjusted version of those distances where points
    within a given radius of the origin are considered to
    be farther away, approaching infinity at the origin.
    The intent is that when this is used for coulomb/lorenz
    forces, field vectors within a radius of a particle don't
    blow up
    """
    if radius is None:
        radius = particle.get_radius()

    if particle.track_position_history:
        approx_delays = np.linalg.norm(points - particle.get_center(), axis=1) / c
        centers = particle.get_past_position(approx_delays)
    else:
        centers = particle.get_center()

    diffs = points - centers
    norms = np.linalg.norm(diffs, axis=1)[:, np.newaxis]
    unit_diffs = np.zeros_like(diffs)
    np.true_divide(diffs, norms, out=unit_diffs, where=(norms > 0))

    adjusted_norms = norms.copy()
    mask = (0 < norms) & (norms < radius)
    adjusted_norms[mask] = radius * radius / norms[mask]
    adjusted_norms[norms == 0] = np.inf

    return unit_diffs, norms, adjusted_norms


def lorentz_force(
    points,
    particle,
    radius=None,
    c=2.0,
    epsilon0=0.025,
):
    unit_diffs, norms, adjusted_norms = points_to_particle_info(particle, points, radius, c)
    delays = norms[:, 0] / c

    acceleration = particle.get_past_acceleration(delays)
    dot_prods = (unit_diffs * acceleration).sum(1)[:, np.newaxis]
    a_perp = acceleration - dot_prods * unit_diffs

    denom = 4 * PI * epsilon0 * c**2 * adjusted_norms
    return -particle.get_charge() * a_perp / denom


class ChargedParticle(Group):
    def __init__(
        self,
        point=ORIGIN,
        charge=1.0,
        mass=1.0,
        color=RED,
        show_sign=True,
        sign="+",
        radius=0.2,
        rotation=0,
        sign_stroke_width=2,
        track_position_history=True,
        history_size=7200,
        euler_steps_per_frame=10,
    ):
        self.charge = charge
        self.mass = mass

        sphere = TrueDot(radius=radius, color=color)
        sphere.make_3d()
        sphere.move_to(point)
        self.sphere = sphere

        self.track_position_history = track_position_history
        self.history_size = history_size
        self.velocity = np.zeros(3)  # Only used if force are added
        self.euler_steps_per_frame = euler_steps_per_frame
        self.init_clock(point)

        super().__init__(sphere)

        if show_sign:
            sign = Tex(sign)
            sign.set_width(radius)
            sign.rotate(rotation, RIGHT)
            sign.set_stroke(WHITE, sign_stroke_width)
            sign.move_to(sphere)
            self.add(sign)
            self.sign = sign

    # Related to updaters

    # CHANGE: Mobject.update now also receives frame_rate (manimgl PR #2481); it is accepted and passed to the parent
    def update(self, dt: float = 0, recurse: bool = True, frame_rate: float | None = None):
        super().update(dt, recurse, frame_rate)
        # Do this instead of adding an updater, because
        # otherwise all animations require the
        # suspend_mobject_updating=false flag
        self.increment_clock(dt)

    def init_clock(self, start_point):
        self.time = 0
        self.time_step = 1 / 30  # This will be updated
        self.recent_positions = np.tile(start_point, 3).reshape((3, 3))
        if self.track_position_history:
            self.position_history = np.zeros((self.history_size, 3))
            self.acceleration_history = np.zeros((self.history_size, 3))
            self.history_index = -1

    def increment_clock(self, dt):
        if dt == 0:
            return self
        self.time += dt
        self.time_step = dt
        self.recent_positions[0:2] = self.recent_positions[1:3]
        self.recent_positions[2] = self.get_center()
        if self.track_position_history:
            self.add_to_position_history()

    def add_to_position_history(self):
        self.history_index += 1
        hist_size = self.history_size
        # If overflowing, copy second half of history
        # lists to the first half, and reset index
        if self.history_index >= hist_size:
            for arr in [self.position_history, self.acceleration_history]:
                arr[:hist_size // 2, :] = arr[hist_size // 2:, :]
            self.history_index = (hist_size // 2) + 1

        self.position_history[self.history_index] = self.get_center()
        self.acceleration_history[self.history_index] = self.get_acceleration()
        return self

    def ignore_last_motion(self):
        self.recent_positions[:] = self.get_center()
        return self

    def add_force(self, force_func: Callable[[Vect3], Vect3]):
        espf = self.euler_steps_per_frame

        def update_from_force(particle, dt):
            if dt == 0:
                return
            for _ in range(espf):
                acc = force_func(particle.get_center()) / self.mass
                self.velocity += acc * dt / espf
                self.shift(self.velocity * dt / espf)

        self.add_updater(update_from_force)
        return self

    def add_spring_force(self, k=1.0, center=None):
        center = center if center is not None else self.get_center().copy()
        self.add_force(lambda p: k * (center - p))
        return self

    def add_field_force(self, field):
        charge = self.get_charge()
        self.add_force(lambda p: charge * field.get_forces([p])[0])
        return self

    def fix_x(self):
        x = self.get_x()
        self.add_updater(lambda m: m.set_x(x))

    # Getters

    def get_charge(self):
        return self.charge

    def get_radius(self):
        return self.sphere.get_radius()

    def get_internal_time(self):
        return self.time

    def scale(self, factor, *args, **kwargs):
        super().scale(factor, *args, **kwargs)
        self.sphere.set_radius(factor * self.sphere.get_radius())
        return self

    def get_acceleration(self):
        p0, p1, p2 = self.recent_positions
        # if (p0 == p1).all() or (p1 == p2).all():
        if np.isclose(p0, p1).all() or np.isclose(p1, p2).all():
            # Otherwise, starts and stops have artificially
            # high acceleration
            return np.zeros(3)
        return (p0 + p2 - 2 * p1) / self.time_step**2

    def get_info_from_delays(self, info_arr, delays):
        if not hasattr(self, "acceleration_history"):
            raise Exception("track_position_history is not turned on")

        if len(info_arr) == 0:
            return np.zeros((len(delays), 3))

        pre_indices = self.history_index - delays / self.time_step
        indices = np.clip(pre_indices, 0, self.history_index).astype(int)

        return info_arr[indices]

    def get_past_acceleration(self, delays):
        return self.get_info_from_delays(self.acceleration_history, delays)

    def get_past_position(self, delays):
        return self.get_info_from_delays(self.position_history, delays)


class AccelerationVector(Vector):
    def __init__(
        self,
        particle,
        stroke_color=PINK,
        stroke_width=4,
        flat_stroke=False,
        norm_func=lambda n: np.tanh(n),
        **kwargs
    ):
        self.norm_func = norm_func

        super().__init__(
            RIGHT,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            flat_stroke=flat_stroke,
            **kwargs
        )
        self.add_updater(lambda m: m.pin_to_particle(particle))

    def pin_to_particle(self, particle):
        a_vect = particle.get_acceleration()
        norm = get_norm(a_vect)
        if self.norm_func is not None and norm > 0:
            a_vect *= self.norm_func(norm) / norm
        center = particle.get_center()
        self.put_start_and_end_on(center, center + a_vect)


class ChargeBasedVectorField(VectorField):
    default_color = BLUE

    def __init__(self, *charges, **kwargs):
        self.charges = list(charges)
        super().__init__(
            self.get_forces,
            color=kwargs.pop("color", self.default_color),
            **kwargs
        )
        self.add_updater(lambda m: m.update_vectors())

    def get_forces(self, points):
        # To be implemented in subclasses
        return np.zeros_like(points)


class LorentzField(ChargeBasedVectorField):
    def __init__(
        self, *charges,
        radius_of_suppression=None,
        c=2.0,
        **kwargs
    ):
        self.radius_of_suppression = radius_of_suppression
        self.c = c
        super().__init__(*charges, **kwargs)

    def get_forces(self, points):
        return sum(
            lorentz_force(
                points, charge,
                radius=self.radius_of_suppression,
                c=self.c
            )
            for charge in self.charges
        )



# ----- From _2023/optics_puzzles/e_field.py -----

class ShowTheEffectsOfOscillatingCharge(InteractiveScene):
    amplitude = 0.25
    frequency = 0.5
    direction = UP

    show_acceleration_vector = True
    origin = None

    axes_config = dict(
        axis_config=dict(stroke_opacity=0.7),
        x_range=(-10, 10),
        y_range=(-5, 5),
        z_range=(-3, 3),
    )
    particle_config = dict(
        track_position_history=True,
        radius=0.15,
    )
    acceleration_vector_config = dict()
    field_config = dict(
        max_vect_len=0.35,
        stroke_opacity=0.75,
        radius_of_suppression=1.0,
        height=10,
        x_density=4.0,
        y_density=4.0,
        c=2.0,
        norm_to_opacity_func=lambda n: np.clip(2 * n, 0, 0.8)
    )
    field_class = LorentzField

    def setup(self):
        super().setup()
        self.add_axes()
        self.add_axis_labels(self.axes)
        self.add_particles(self.axes)
        self.add_field(self.particles)
        if self.show_acceleration_vector:
            self.add_acceleration_vectors(self.particles)

    def add_axes(self):
        self.axes = ThreeDAxes(**self.axes_config)
        if self.origin is not None:
            self.axes.shift(self.origin - self.axes.get_origin())
        self.add(self.axes)

    def add_axis_labels(self, axes):
        axis_labels = label = Tex("xyz")
        if axes.z_axis.get_stroke_opacity() > 0:
            axis_labels.rotate(PI / 2, RIGHT)
            axis_labels[0].next_to(axes.x_axis.get_right(), OUT)
            axis_labels[1].next_to(axes.y_axis.get_top(), OUT)
            axis_labels[2].next_to(axes.z_axis.get_zenith(), RIGHT)
        else:
            axis_labels[1].clear_points()
            axis_labels[0].next_to(axes.x_axis.get_right(), UP)
            axis_labels[2].next_to(axes.y_axis.get_top(), RIGHT)

        self.axis_labels = axis_labels
        self.add(self.axis_labels)

    def add_particles(self, axes):
        self.particles = self.get_particles()
        self.particles.add_updater(lambda m: m.move_to(
            axes.c2p(*self.oscillation_function(self.time))
        ))
        for particle in self.particles:
            particle.ignore_last_motion()
        self.add(self.particles)

    def get_particles(self):
        return Group(ChargedParticle(**self.particle_config))

    def add_field(self, particles):
        self.field = self.field_class(*particles, **self.field_config)
        self.add(self.field, particles)

    def add_acceleration_vectors(self, particles):
        self.acceleration_vectors = VGroup(*(
            AccelerationVector(particle)
            for particle in particles
        ))
        self.add(self.acceleration_vectors, self.particles)

    def oscillation_function(self, time):
        return self.amplitude * np.sin(TAU * self.frequency * time) * self.direction

    def construct(self):
        # Test
        self.wait(20)


class ChargeOnZAxis(ShowTheEffectsOfOscillatingCharge):
    default_frame_orientation = (-20, 70)
    direction = OUT

    origin = ORIGIN

    axes_config = dict(
        axis_config=dict(stroke_opacity=0.7),
        x_range=(-8, 8),
        y_range=(-6, 6),
        z_range=(-3, 3),
    )
    particle_config = dict(
        show_sign=False,
        rotation=PI / 2,
        track_position_history=True,
        radius=0.2,
    )
    field_config = dict(
        max_vect_len=0.5,
        stroke_opacity=0.7,
        radius_of_suppression=1.0,
        width=40,
        height=40,
        depth=0,
        x_density=4.0,
        y_density=4.0,
        z_density=1.0,
        c=2.0,
        norm_to_opacity_func=lambda n: np.clip(n, 0, 0.8)
    )

    def construct(self):
        # Test
        self.play(self.frame.animate.reorient(16, 71, 0), run_time=12)
        self.play(self.frame.animate.reorient(-15, 84, 0), run_time=6)
        self.play(self.frame.animate.reorient(-38, 64, 0), run_time=10)
        self.play(self.frame.animate.reorient(24, 66, 0), run_time=10)


class RowOfCharges(ChargeOnZAxis):
    n_charges = 17
    particle_buff = 0.25
    particle_config = dict(
        rotation=PI / 2,
        track_position_history=True,
        radius=0.1,
        show_sign=False,
        charge=0.15
    )
    field_config = dict(
        max_vect_len=0.5,
        stroke_opacity=0.7,
        radius_of_suppression=1.0,
        width=30,
        height=30,
        depth=0,
        x_density=4.0,
        y_density=4.0,
        z_density=1.0,
        c=2.0,
        norm_to_opacity_func=lambda n: np.clip(1.5 * n, 0, 0.8)
    )
    show_acceleration_vector = False

    def construct(self):
        # Test
        self.play(self.frame.animate.reorient(-7, 62, 0).set_height(16), run_time=12)
        self.play(self.frame.animate.reorient(26, 70, 0), run_time=12)
        self.play(self.frame.animate.reorient(-26, 70, 0), run_time=12)

    def get_particles(self):
        return Group(*(
            ChargedParticle(**self.particle_config)
            for n in range(self.n_charges)
        )).arrange(UP, buff=self.particle_buff)


class PlaneOfCharges(RowOfCharges):
    n_rows = 20
    n_cols = 20
    particle_buff = 0.1
    grid_height = 6

    particle_config = dict(
        rotation=PI / 2,
        track_position_history=True,
        radius=0.05,
        show_sign=False,
        charge=2.0 / 400.0,
    )

    def get_particles(self):
        result = Group(*(
            ChargedParticle(**self.particle_config)
            for _ in range(self.n_rows * self.n_cols)
        ))
        result.arrange_in_grid(
            self.n_rows, self.n_cols,
            buff=self.particle_buff
        )
        result.set_width(self.grid_height)
        result.rotate(PI / 2, UP)
        return result
