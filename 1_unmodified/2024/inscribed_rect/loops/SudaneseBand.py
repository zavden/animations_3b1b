# ==============================================================================
# Scene:      SudaneseBand
# Source:     videos/_2024/inscribed_rect/loops.py (lines 2110-2154)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl SudaneseBand.py SudaneseBand -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/inscribed_rect/helpers.py -----

def alt_mobius_strip_func(u, v):
    phi = TAU * v
    vect = rotate_vector(RIGHT, phi / 2, axis=UP)
    vect = rotate_vector(vect, phi, axis=OUT)
    ref_point = np.array([np.cos(phi), np.sin(phi), 0])
    return ref_point + 0.7 * (u - 0.5) * vect


def stereo_project_point(point, axis=0, r=1, max_norm=10000):
    point = fdiv(point * r, point[axis] + r)
    point[axis] = 0
    norm = get_norm(point)
    if norm > max_norm:
        point *= max_norm / norm
    return point


def sudanese_band_func(u, v):
    eta = PI * u
    phi = TAU * v
    z1 = math.sin(eta) * np.exp(complex(0, phi))
    z2 = math.cos(eta) * np.exp(complex(0, phi / 2))
    r4_point = np.array([z1.real, z1.imag, z2.real, z2.imag])
    r4_point[:3] = rotate_vector(r4_point[:3], PI / 3, axis=[1, 1, 1])
    result = stereo_project_point(r4_point, axis=0)[1:]
    result = rotate_vector(result, 60 * DEG, OUT)
    result = rotate_vector(result, 90 * DEG, RIGHT)
    return result



# ----- From _2024/inscribed_rect/loops.py -----

class SudaneseBand(InteractiveScene):
    def construct(self):
        # Tranform mobius to Sudanese
        frame = self.frame
        sudanese_band = self.get_full_surface(sudanese_band_func)
        strip = self.get_full_surface(alt_mobius_strip_func)
        strip.set_height(6)
        og_strip = strip.copy()
        sudanese_band.set_height(6)

        frame.reorient(28, 75, 0, ORIGIN, 8)
        self.add(strip)
        self.play(frame.animate.increment_theta(180 * DEG), run_time=12)
        self.play(
            frame.animate.reorient(99, 102, 0),
            Transform(strip, sudanese_band, time_span=(0, 6)),
            run_time=10
        )
        self.wait(30)  # Examine

        # Back to strip
        self.play(
            Transform(strip, og_strip),
            run_time=6
        )

    def get_full_surface(self, surface_func, resolution=(101, 101)):
        surface = ParametricSurface(surface_func, resolution=resolution)
        surface.set_color(BLUE_E, 1)
        surface.set_shading(0.25, 0.25, 0)

        mesh = VGroup(
            *SurfaceMesh(surface, resolution=(21, 21), normal_nudge=1e-3),
            *SurfaceMesh(surface, resolution=(21, 21), normal_nudge=-1e-3),
        )
        mesh.set_stroke(WHITE, 0.5, 0.2)

        edge = VGroup(
            ParametricCurve(lambda t: surface_func(0, t), (0, 1, 0.01)),
            ParametricCurve(lambda t: surface_func(1, t), (0, 1, 0.01)),
        )
        edge.set_stroke(Color("red"), 2)
        edge.apply_depth_test()

        return Group(surface, mesh, edge)
