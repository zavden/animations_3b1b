# ==============================================================================
# Scene:      ZetaFunctionPlot
# Source:     videos/_2025/laplace/main_equations.py (lines 1667-1726)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl ZetaFunctionPlot.py ZetaFunctionPlot -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Resolution of the zeta graph from (1001, 1001) to (301, 301): the mpmath computation (≈2 mp.zeta per point, 2 passes) took more than an hour before the first frame
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/laplace/integration.py -----

def z_to_color(z, sat=0.5, lum=0.5):
    angle = math.atan2(z.imag, z.real)
    return Color(hsl=(angle / TAU, sat, lum))


def get_complex_graph(
    s_plane,
    func,
    min_real=None,
    pole_buff=1e-3,
    color_by_phase=True,
    opacity=0.7,
    shading=(0.1, 0.1, 0.1),
    resolution=(301, 301),
    saturation=0.5,
    luminance=0.5,
    mesh_resolution=(61, 61),
    mesh_stroke_style=dict(
        color=WHITE,
        width=1,
        opacity=0.15
    )
):
    u_range = list(s_plane.x_range[:2])
    v_range = list(s_plane.y_range[:2])

    if min_real is not None:
        u_range[0] = min_real + pole_buff

    unit_size = s_plane.x_axis.get_unit_size()
    graph = ParametricSurface(
        lambda u, v: [
            *s_plane.c2p(u, v)[:2],
            unit_size * abs(func(complex(u, v)))
        ],
        u_range=u_range,
        v_range=v_range,
        resolution=resolution
    )
    graph.set_shading(*shading)

    if color_by_phase:
        graph.color_by_uv_function(
            lambda u, v: z_to_color(func(complex(u, v)), sat=saturation, lum=luminance)
        )

    graph.set_opacity(opacity)
    graph.set_sort_to_camera()

    # Add mesh
    mesh = SurfaceMesh(graph, resolution=mesh_resolution)
    mesh.set_stroke(**mesh_stroke_style)

    return Group(graph, mesh)



# ----- From _2025/laplace/main_equations.py -----

class ZetaFunctionPlot(InteractiveScene):
    # resolution = (51, 51)
    # CHANGE: (1001, 1001) is ~1M points with 2 mp.zeta each (the original warns that it takes about an hour and the render stayed at 0 frames); it is lowered to (301, 301).
    resolution = (301, 301)  # Probably takes like an hour to compute

    def construct(self):
        # Planes
        x_max = 25
        s_plane = ComplexPlane((-x_max, x_max), (-x_max, x_max), faded_line_ratio=5)
        s_plane.set_height(40)
        s_plane.add_coordinate_labels(font_size=16)

        partial_plane = ComplexPlane((1, x_max), (-x_max, x_max))
        partial_plane.shift(s_plane.n2p(0) - partial_plane.n2p(0))

        self.add(s_plane)

        # True function
        import mpmath as mp

        def zeta_log_deriv(s):
            epsilon = 1e-4
            if s == 1:
                return 1 / epsilon
            out = mp.zeta(s)
            if abs(out) < 1e-3:
                return 1 / epsilon
            out_prime = (mp.zeta(s + epsilon) - out) / epsilon
            # return mp.zeta(s, derivative=1) / out
            return out_prime / out

        graph = get_complex_graph(
            s_plane,
            zeta_log_deriv,
            resolution=self.resolution,
        )
        graph.set_clip_plane(RIGHT, -1)
        graph.set_opacity(0.6)

        self.add(graph)

        # Panning
        frame = self.frame
        frame.reorient(24, 82, 0, (0.39, 0.58, 0.49), 4.02)
        self.play(
            frame.animate.reorient(-14, 79, 0, (-0.62, -0.08, 1.41), 8.12),
            run_time=8
        )
        self.play(
            graph.animate.set_clip_plane(RIGHT, x_max),
            frame.animate.reorient(-13, 80, 0, (-0.28, -0.01, 2.17), 12.57),
            run_time=5
        )
        self.play(
            frame.animate.reorient(32, 81, 0, (-0.98, -2.23, 5.19), 32.31),
            run_time=20
        )
        self.play(
            frame.animate.reorient(91, 84, 0, (-0.25, -1.54, 7.01), 32.31),
            run_time=15,
        )
