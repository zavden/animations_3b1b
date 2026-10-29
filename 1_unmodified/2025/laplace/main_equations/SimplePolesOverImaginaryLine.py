# ==============================================================================
# Scene:      SimplePolesOverImaginaryLine
# Source:     videos/_2025/laplace/main_equations.py (lines 2135-2152)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl SimplePolesOverImaginaryLine.py SimplePolesOverImaginaryLine -w -m --fps 15
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

class SimplePolesOverImaginaryLine(InteractiveScene):
    def construct(self):
        s_plane = ComplexPlane((-5, 5), (-5, 5))
        s_plane.add_coordinate_labels()
        omega = 2
        graph = get_complex_graph(
            s_plane,
            lambda s: (s**2) / (s**2 + omega**2 + 1e-6),
            resolution=(301, 301)
        )
        graph[0].set_sort_to_camera()
        graph[1].set_clip_plane(OUT, 0)
        self.add(s_plane, graph)

        # Pan
        frame = self.frame
        frame.reorient(-57, 78, 0, (-1.28, 0.48, 0.92), 9.65)
        self.play(frame.animate.reorient(59, 78, 0, (-0.31, -0.1, 0.87), 10.53), run_time=12)
