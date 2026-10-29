# ==============================================================================
# Scene:      ManyParallelPropagations
# Source:     videos/_2023/optics_puzzles/e_field.py (lines 2205-2237)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl ManyParallelPropagations.py ManyParallelPropagations -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
#   - ChargedParticle.update(dt, recurse) did not accept frame_rate, which manimgl passes since PR #2481 (TypeError); the parameter was added
#   - self.dot_centers does not exist (leftover from a refactor in the original); the points of self.dot_center_refs are used
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

def get_influence_ring(center_point, color=WHITE, speed=2.0, max_width=3.0, width_decay_exp=0.5):
    ring = Circle()
    ring.set_stroke(color)
    ring.move_to(center_point)
    ring.time = 0

    def update_ring(ring, dt):
        ring.time += dt
        radius = ring.time * speed
        ring.set_width(max(2 * radius, 1e-3))
        ring.set_stroke(width=max_width / (1 + radius)**width_decay_exp)
        return ring

    ring.add_updater(update_ring)
    return ring


class OneOfManyCharges(InteractiveScene):
    speed = 1.5
    wave_len = 3
    default_frame_orientation=(0, 70, 0)
    dot_amplitude_factor = 0.2
    plane_wave_field_config = dict(
        x_density=4.0,
        y_density=0.5,
        z_density=1.0,
        width=28,
        height=0,
        depth=12,
        tip_width_ratio=3,
        stroke_color=TEAL,
        stroke_width=3,
        stroke_opacity=0.5,
        norm_to_opacity_func=(lambda n: 2 * n),
        max_vect_len=1.0
    )
    plane_wave_amlpitude = 0.5
    charge_field_config = dict(
        x_density=4.0,
        y_density=4.0,
        z_density=4.0,
        width=28,
        height=0,
        depth=16,
        tip_width_ratio=3,
        stroke_color=BLUE,
        stroke_width=3,
        norm_to_opacity_func=(lambda n: np.tanh(n)),
    )
    charge_index = 3155

    dots_dims = (11, 20, 20)
    dots_shape = (6, 4, 4)

    def setup(self):
        super().setup()

        # Axes
        self.axes = ThreeDAxes()
        self.add(self.axes)

        # Add incoming wave
        omega = TAU * self.speed / self.wave_len
        k = TAU / self.wave_len
        amplitude = 0.5

        def plane_wave_func(points, t):
            return self.plane_wave_amlpitude * np.outer(
                np.cos(k * np.dot(points, RIGHT) - omega * t),
                OUT
            )

        plane_wave = TimeVaryingVectorField(
            plane_wave_func,
            **self.plane_wave_field_config
        )

        plane_wave.opacity_multiplier = ValueTracker(1)
        plane_wave.add_updater(lambda m: m.set_stroke(opacity=m.opacity_multiplier.get_value() * m.get_stroke_opacities()))

        self.plane_wave_func = plane_wave_func
        self.plane_wave = plane_wave
        self.add(plane_wave)

        # Add 3d grid of charges
        dots = DotCloud(color=BLUE)
        dots.to_grid(*self.dots_dims, height=None)
        dots.set_radius(0)
        dots.set_shape(*self.dots_shape)
        dots.set_radius(0.05)
        dots.make_3d(0.1)

        self.dot_center_refs = dots.copy()
        self.dot_center_refs.set_opacity(0)
        self.dot_center_refs.set_radius(0)

        def update_dots(dots):
            centers = self.dot_center_refs.get_points()
            offsets =  plane_wave.func(centers)
            offsets *= self.dot_amplitude_factor
            dots.set_points(centers + offsets)

        dots.add_updater(update_dots)

        dots.opacity_multiplier = ValueTracker(0.75)
        dots.add_updater(lambda m: m.set_opacity(m.opacity_multiplier.get_value()))

        self.dots = dots
        self.add(dots)


    def construct(self):
        # Pan a little to start
        frame = self.frame
        self.play(
            frame.animate.reorient(25, 72, 0),
            run_time=4
        )

        # Create field based on the charges
        if self.charge_index > 0:
            charge = ChargedParticle(
                charge=-5,
                color=BLUE,
                show_sign=False,
                radius=0.1
            )
            charge.add_updater(lambda m: m.move_to(self.dots.get_points()[self.charge_index]))
            charge.update()
            charge.ignore_last_motion()
            charge_field = LorentzField(
                charge,
                center=charge.get_y() * UP,
                radius_of_suppression=0.2,
                **self.charge_field_config
            )
            # acc_vect = AccelerationVector(charge)
            acc_vect = VectorizedPoint()

            self.add(charge_field, acc_vect, charge, self.dots)
            self.play(
                self.plane_wave.opacity_multiplier.animate.set_value(0),
                self.dots.opacity_multiplier.animate.set_value(0.1),
                FadeIn(charge, suspend_mobject_updating=False),
                VFadeIn(acc_vect),
                run_time=2,
            )
        else:
            self.play(
                self.dots.opacity_multiplier.animate.set_value(0.2),
                run_time=2
            )
        self.play(
            frame.animate.reorient(25, 72, 0),
            run_time=8
        )
        self.play(
            frame.animate.reorient(-25, 72, 0),
            run_time=8
        )


class ManyParallelPropagations(OneOfManyCharges):
    dots_dims = (11, 20, 20)
    dots_shape = (6, 0, 4)

    def construct(self):
        # Test
        dots = self.dots
        plane_wave = self.plane_wave
        self.axes.y_axis.set_opacity(0)

        frame = self.frame
        frame.reorient(0, 90, 0)
        frame.set_focal_distance(10)

        dots.set_radius(0.05)
        dots.opacity_multiplier.set_value(1)
        plane_wave.opacity_multiplier.set_value(0)

        rings = []
        for _ in range(10):
            # CHANGE: self.dot_centers does not exist (leftover from a refactor in the original); the centers are in self.dot_center_refs
            min_x, min_y, min_z = self.dot_center_refs.get_points()[0]
            max_x, max_y, max_z = self.dot_center_refs.get_points()[-1]
            for x in np.linspace(min_x, max_x, 6):
                for z in np.linspace(min_z, max_z, 10):
                    ring = get_influence_ring([x, 0, z], speed=self.speed, max_width=1, width_decay_exp=2)
                    ring.rotate(PI / 2, RIGHT)
                    rings.append(ring)
                    self.add(ring)
            self.wait()
            for ring in rings:
                if ring.get_stroke_width() < 0.01:
                    self.remove(ring)
        self.wait(5)
