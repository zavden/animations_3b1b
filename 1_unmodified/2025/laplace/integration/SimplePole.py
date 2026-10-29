# ==============================================================================
# Scene:      SimplePole
# Source:     videos/_2025/laplace/integration.py (lines 1833-1842)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SimplePole.py SimplePole -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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


class SimplePole(InteractiveScene):
    def construct(self):
        frame = self.frame
        plane = ComplexPlane((-3, 3), (-3, 3))
        a = complex(-0.5 + 1.5j)
        graph = get_complex_graph(plane, lambda s: np.divide(1.0, (s - a)))

        self.add(plane, graph)
        frame.reorient(-22, 89, 0, (0.31, 0.85, 3.73), 12.49)
        self.play(frame.animate.reorient(23, 88, 0, (0.31, 0.85, 3.73), 12.49), run_time=10)
