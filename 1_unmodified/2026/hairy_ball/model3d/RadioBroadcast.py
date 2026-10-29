# ==============================================================================
# Scene:      RadioBroadcast
# Source:     videos/_2026/hairy_ball/model3d.py (lines 463-633)
# Category:   1 · Renders unmodified
# Includes code copied from: _2026/hairy_ball/spheres.py
#
# Run from this folder:
#     manimgl RadioBroadcast.py RadioBroadcast -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np


# ----- From _2026/hairy_ball/spheres.py -----

def fibonacci_sphere(samples=1000):
    """
    Create uniform-ish points on a sphere

    Parameters
    ----------
    samples : int
        Number of points to create. The default is 1000.

    Returns
    -------
    points : NumPy array
        Points on the unit sphere.

    """

    # Define the golden angle
    phi = np.pi * (np.sqrt(5) - 1)

    # Define y-values of points
    pos = np.array(range(samples), ndmin=2)
    y = 1 - (pos / (samples - 1)) * 2

    # Define radius of cross-section at y
    radius = np.sqrt(1 - y * y)

    # Define the golden angle increment
    theta = phi * pos

    # Define x- and z- values of poitns
    x = np.cos(theta) * radius
    z = np.sin(theta) * radius

    # Merge together x,y,z
    points = np.concatenate((x, y, z))

    # Transpose to get coordinates in right place
    points = np.transpose(points)

    return points



# ----- From _2026/hairy_ball/model3d.py -----

class RadioTower(VGroup):
    def __init__(self, height=4, stroke_color=GREY_A, stroke_width=2, **kwargs):
        self.legs = self.get_legs()
        self.struts = VGroup(
            self.get_struts(leg1, leg2)
            for leg1, leg2 in adjacent_pairs(self.legs)
        )

        super().__init__(self.legs, self.struts, **kwargs)

        self.set_stroke(stroke_color, stroke_width)
        self.set_depth(height)
        self.center()

    def get_legs(self):
        return VGroup(
            Line(point, 4 * OUT)
            for point in compass_directions(4, UR)
        )

    def get_struts(self, leg1, leg2, n_crosses=4):
        points1, points2 = [
            [leg.pfp(a) for a in np.linspace(0, 1, n_crosses + 1)]
            for leg in [leg1, leg2]
        ]
        return VGroup(
            *(Line(*pair) for pair in zip(points1, points2[1:])),
            *(Line(*pair) for pair in zip(points1[1:], points2)),
        )


class RadioBroadcast(InteractiveScene):
    def construct(self):
        # Add tower
        frame = self.frame
        tower = RadioTower()
        tower.center()
        tower.move_to(ORIGIN, OUT)

        frame.reorient(-26, 93, 0, (0.44, -0.33, 1.02), 11.76)
        frame.add_ambient_rotation(3 * DEG)
        self.add(tower)

        # Add shells
        n_shells = 12
        shells = Group(Sphere() for n in range(n_shells))
        shells.set_color(RED)
        for shell in shells:
            shell.always_sort_to_camera(self.camera)

        time_tracker = ValueTracker(0)
        rate_tracker = ValueTracker(1)
        time_tracker.add_updater(lambda m, dt: m.increment_value(dt * rate_tracker.get_value()))

        def update_shells(shells):
            alpha = 1e-3 + time_tracker.get_value() % 1
            for n, shell in enumerate(shells):
                radius = n + alpha
                shell.set_width(2 * radius)
                shell.move_to(ORIGIN)
                dimmer = inverse_interpolate(n_shells, 0, radius)
                shell.set_opacity(0.25 * dimmer / radius)

        shells.add_updater(update_shells)

        self.add(shells, time_tracker)
        self.wait(8)

        # Show characters
        n_characters = 12
        characters = VGroup()
        modes = ["pondering", "thinking", "hesitant", "erm", "concentrating", "tease", "happy", "plain"]
        for theta in np.linspace(0, PI, n_characters):
            character = PiCreature(
                height=1.0,
                mode=random.choice(modes),
                color=random.choice([BLUE_A, BLUE_B, BLUE_C, BLUE_D, BLUE_D])
            )
            point = 6 * (math.cos(theta) * RIGHT + math.sin(theta) * UP)
            character.move_to(point)
            character.look_at(ORIGIN)
            characters.add(character)
        characters.rotate(90 * DEG, RIGHT, about_point=ORIGIN)

        frame.clear_updaters()
        self.play(
            LaggedStartMap(FadeIn, characters, lag_ratio=0.2, run_time=3),
            frame.animate.set_theta(0),
        )
        self.play(LaggedStartMap(Blink, characters, lag_ratio=0.2))
        self.wait(4)

        # Show a wave
        axes = ThreeDAxes()

        def wave_func(points, t, magnetic=False):
            real_time = time_tracker.get_value()
            normal = normalize_along_axis(points, 1)
            radii = np.linalg.norm(points, axis=1)
            perp = normalize_along_axis(np.cross(points, OUT), 1)
            if magnetic:
                direction = perp
            else:
                direction = np.cross(normal, perp)
            direction *= 1.0 - np.abs(np.dot(normal, OUT))[:, np.newaxis]
            return 0.25 * direction * np.cos(TAU * (radii - real_time))[:, np.newaxis]

        def E_wave_func(points, t):
            return wave_func(points, t, False)

        def B_wave_func(points, t):
            return wave_func(points, t, True)

        sample_points = np.linspace(ORIGIN, 10 * RIGHT, 100)
        E_wave, B_wave = [
            TimeVaryingVectorField(
                func, axes,
                sample_coords=sample_points,
                color=color,
                max_vect_len_to_step_size=np.inf,
                stroke_width=3
            )
            for color, func in zip([RED, TEAL], [E_wave_func, B_wave_func])
        ]

        points = sample_points

        self.play(
            VFadeIn(E_wave, time_span=(0, 1)),
            VFadeIn(B_wave, time_span=(0, 1)),
            FadeOut(characters, time_span=(0, 1)),
            frame.animate.reorient(49, 69, 0, (4.48, -0.2, -0.1), 2.71),
            rate_tracker.animate.set_value(0.5),
            run_time=3
        )
        self.play(
            frame.animate.reorient(122, 73, 0, (4.48, -0.2, -0.1), 2.71),
            run_time=11
        )

        # Show propagation direction
        radius = 5
        sample_point = radius * RIGHT
        prop_vect = Vector(sample_point, fill_color=YELLOW)

        def get_sample_vects(point):
            curr_time = time_tracker.get_value()
            result = VGroup(
                Vector(
                    func(point.reshape(1, -1), curr_time).flatten(),
                    fill_color=color
                )
                for color, func in zip([RED, TEAL], [E_wave_func, B_wave_func])
            )
            result.shift(point)
            return result

        sample_vects = always_redraw(lambda: get_sample_vects(sample_point))

        self.play(
            GrowArrow(prop_vect),
            E_wave.animate.set_stroke(opacity=0.1),
            B_wave.animate.set_stroke(opacity=0.1),
            VFadeIn(sample_vects),
        )
        self.wait(6)
        self.play(rate_tracker.animate.set_value(0))
        sample_vects.clear_updaters()

        # Show on the whole sphere
        sample_coords = radius * fibonacci_sphere(3000)
        sample_coords = np.array(list(sorted(sample_coords, key=lambda p: get_norm(p - sample_point))))
        fields = VGroup(
            VectorField(
                lambda p: func(p, time_tracker.get_value()),
                axes,
                sample_coords=sample_coords,
                stroke_width=3,
                max_vect_len_to_step_size=np.inf,
                max_vect_len=np.inf,
                color=color,
            )
            for func, color in zip([E_wave_func, B_wave_func], [RED, TEAL])
        )
        fields.set_stroke(opacity=0.5)
        fields.apply_depth_test()
        fields.set_scale_stroke_with_zoom(True)

        sphere = Sphere(radius=0.99 * radius)
        sphere.set_color(GREY_D, 0.5)
        sphere.always_sort_to_camera(self.camera)

        shells.clear_updaters()
        self.play(FadeOut(shells))
        self.play(
            FadeIn(sphere, time_span=(0, 2)),
            ShowCreation(fields, lag_ratio=0),
            frame.animate.reorient(36, 39, 0, (0.11, -0.24, 0.76), 11.24),
            run_time=12
        )
        self.play(frame.animate.reorient(-48, 69, 0, (0.4, -1.3, 0.14), 10.81), run_time=12)
        self.wait()
