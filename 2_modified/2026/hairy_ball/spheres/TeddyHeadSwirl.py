# ==============================================================================
# Scene:      TeddyHeadSwirl
# Source:     videos/_2026/hairy_ball/spheres.py (lines 164-208)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TeddyHeadSwirl.py TeddyHeadSwirl -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/raster_images/TeddyHead.png  (placeholder 1920x1080)
#
# Notes:
#   ImageMobject("TeddyHead") is only created as a reference image: the self.add(img) is commented out in the original, so the image is never seen in the video and the placeholder is enough for the scene to build. No code change was needed.
# ==============================================================================

from manim_imports_ext import *
import numpy as np

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


class SphereStreamLines(StreamLines):
    def __init__(self, func, coordinate_system, density=50, sample_coords=None, **kwargs):
        self.sample_coords = sample_coords
        super().__init__(func, coordinate_system, density=density, **kwargs)

    def get_sample_coords(self):
        if self.sample_coords is None:
            coords = fibonacci_sphere(int(4 * PI * self.density))
        else:
            coords = self.sample_coords
        return coords

    def draw_lines(self):
        super().draw_lines()
        for submob in self.submobjects:
            submob.set_points(normalize_along_axis(submob.get_points(), 1))
        return self


class TeddyHeadSwirl(InteractiveScene):
    def construct(self):
        img = ImageMobject("TeddyHead")
        img.set_height(FRAME_HEIGHT)
        img.fix_in_frame()
        # self.add(img)

        # Add sphere
        frame = self.frame
        axes = ThreeDAxes()

        def v_func(points):
            perp = np.cross(points, OUT)
            alt_perp = np.cross(points, perp)
            return 0.4 * (perp + alt_perp)

        top_sample_points = np.array([
            point for point in fibonacci_sphere(10_000) if point[2] > 0.95
        ])
        full_sample_points = fibonacci_sphere(1000)

        top_lines, full_lines = lines = VGroup(*(
            SphereStreamLines(
                v_func,
                axes,
                sample_coords=samples,
                arc_len=0.25,
                dt=0.05,
                max_time_steps=10,
            )
            for samples in [top_sample_points, full_sample_points]
        ))
        lines.set_stroke(WHITE, 2, 0.7)
        full_lines.set_stroke(WHITE, 2, 0.7)
        top_animated_lines = AnimatedStreamLines(top_lines)
        full_animated_lines = AnimatedStreamLines(full_lines)

        frame.reorient(-50, 12, 0, (0.15, -0.04, 0.0), 3.09)
        self.add(top_animated_lines)
        self.wait(4)
        self.add(full_animated_lines)
        self.play(
            frame.animate.reorient(-39, 75, 0),
            run_time=6
        )
