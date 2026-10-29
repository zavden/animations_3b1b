# ==============================================================================
# Scene:      ResponsiveCharge
# Source:     videos/_2023/optics_puzzles/e_field.py (lines 2240-2297)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl ResponsiveCharge.py ResponsiveCharge -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
#   - ChargedParticle.update(dt, recurse) did not accept frame_rate, which manimgl passes since PR #2481 (TypeError); the parameter was added
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField
from matplotlib import colormaps
from typing import TYPE_CHECKING


# ----- From _2023/optics_puzzles/objects.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3


spectral_cmap = colormaps.get_cmap("Spectral")


def get_spectral_color(alpha):
    return Color(rgb=spectral_cmap(alpha)[:3])


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


class OscillatingWave(VMobject):
    def __init__(
        self,
        axes,
        y_amplitude=0.0,
        z_amplitude=0.75,
        z_phase=0.0,
        y_phase=0.0,
        wave_len=0.5,
        twist_rate=0.0,  # In rotations per unit distance
        speed=1.0,
        sample_resolution=0.005,
        stroke_width=2,
        offset=ORIGIN,
        color=None,
        **kwargs,
    ):
        self.axes = axes
        self.y_amplitude = y_amplitude
        self.z_amplitude = z_amplitude
        self.z_phase = z_phase
        self.y_phase = y_phase
        self.wave_len = wave_len
        self.twist_rate = twist_rate
        self.speed = speed
        self.sample_resolution = sample_resolution
        self.offset = offset

        super().__init__(**kwargs)

        color = color or self.get_default_color(wave_len)
        self.set_stroke(color, stroke_width)
        self.set_flat_stroke(False)

        self.time = 0
        self.clock_is_stopped = False

        self.add_updater(lambda m, dt: m.update_points(dt))

    def update_points(self, dt):
        if not self.clock_is_stopped:
            self.time += dt
        xs = np.arange(
            self.axes.x_axis.x_min,
            self.axes.x_axis.x_max,
            self.sample_resolution
        )
        self.set_points_as_corners(
            self.offset + self.xt_to_point(xs, self.time)
        )

    def stop_clock(self):
        self.clock_is_stopped = True

    def start_clock(self):
        self.clock_is_stopped = False

    def xt_to_yz(self, x, t):
        phase = TAU * t * self.speed / self.wave_len
        y_outs = self.y_amplitude * np.sin(TAU * x / self.wave_len - phase - self.y_phase)
        z_outs = self.z_amplitude * np.sin(TAU * x / self.wave_len - phase - self.z_phase)
        twist_angles = x * self.twist_rate * TAU
        y = np.cos(twist_angles) * y_outs - np.sin(twist_angles) * z_outs
        z = np.sin(twist_angles) * y_outs + np.cos(twist_angles) * z_outs

        return y, z

    def xt_to_point(self, x, t):
        y, z = self.xt_to_yz(x, t)
        return self.axes.c2p(x, y, z)

    def get_default_color(self, wave_len):
        return get_spectral_color(inverse_interpolate(
            1.5, 0.5, wave_len
        ))


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


class GraphAsVectorField(VectorField):
    def __init__(
        self,
        axes: Axes | ThreeDAxes,
        # Maps x to y, or x to (y, z)
        graph_func: Callable[[VectN], VectN] | Callable[[VectN], Tuple[VectN, VectN]],
        x_density=10.0,
        max_vect_len=np.inf,
        **kwargs,
    ):
        self.sample_xs = np.arange(axes.x_axis.x_min, axes.x_axis.x_max, 1.0 / x_density)
        self.axes = axes

        def vector_func(points):
            output = graph_func(self.sample_xs)
            if isinstance(axes, ThreeDAxes):
                graph_points = axes.c2p(self.sample_xs, *output)
            else:
                graph_points = axes.c2p(self.sample_xs, output)
            base_points = axes.x_axis.n2p(self.sample_xs)
            return graph_points - base_points

        super().__init__(
            func=vector_func,
            max_vect_len=max_vect_len,
            **kwargs
        )
        always(self.update_vectors)

    def reset_sample_points(self):
        self.sample_points = self.get_sample_points()

    def get_sample_points(self, *args, **kwargs):
        # Override super class and ignore all length/density information
        return self.axes.x_axis.n2p(self.sample_xs)


class OscillatingFieldWave(GraphAsVectorField):
    def __init__(self, axes, wave, **kwargs):
        self.wave = wave
        if "stroke_color" not in kwargs:
            kwargs["stroke_color"] = wave.get_color()
        super().__init__(
            axes=axes,
            graph_func=lambda x: wave.xt_to_yz(x, wave.time),
            **kwargs
        )

    def get_sample_points(self, *args, **kwargs):
        # Override super class and ignore all length/density information
        return self.wave.offset + self.axes.x_axis.n2p(self.sample_xs)



# ----- From _2023/optics_puzzles/e_field.py -----

class ResponsiveCharge(InteractiveScene):
    def construct(self):
        # Driving chrage
        charge1 = ChargedParticle(charge=0.25)
        charge1.add_spring_force(k=10)
        charge1.move_to(0.3 * DOWN)

        # Responsive charge
        k = 20
        charge2 = ChargedParticle(charge=1.0, radius=0.1, show_sign=False)
        charge2.move_to(2.5 * RIGHT)
        # charge2.add_field_force(field)
        charge2.add_spring_force(k=k)
        charge2.add_force(lambda p: wave.xt_to_point(p[0], wave.time) * [0, 1, 1])
        # charge2.fix_x()
        self.add(charge2)

        # E field
        # field_type = ColoumbPlusLorentzField
        field_type = LorentzField
        field = field_type(
            charge1, charge2,
            x_density=4.0,
            y_density=4.0,
            norm_to_opacity_func=lambda n: np.clip(0.5 * n, 0, 1),
            c=1.0,
        )
        self.add(field)

        # Pure wave
        axes = ThreeDAxes()
        wave = OscillatingWave(axes, y_amplitude=1.0, z_amplitude=0.0, wave_len=2.0)
        field_wave = OscillatingFieldWave(axes, wave)
        wave.set_stroke(opacity=0.5)


        self.add(axes, wave, field_wave)

        # omega = (wave.speed / wave.wave_len) * TAU
        # omega_0 = math.sqrt(k / charge2.mass)
        # v0 = omega / (omega_0**2 - omega**2)
        # charge2.velocity = v0 * UP

        self.wait(20)

        # Plane
        plane = NumberPlane()
        plane.fade(0.5)
        self.add(plane)

        # Test wiggle
        self.play(
            charge1.animate.shift(UP).set_anim_args(
                rate_func=wiggle,
                run_time=3,
            )
        )
        self.wait(4)
