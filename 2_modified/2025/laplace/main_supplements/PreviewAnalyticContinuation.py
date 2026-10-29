# ==============================================================================
# Scene:      PreviewAnalyticContinuation
# Source:     videos/_2025/laplace/main_supplements.py (lines 618-640)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl PreviewAnalyticContinuation.py PreviewAnalyticContinuation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - graph.set_sort_to_camera() -> graph[0].set_sort_to_camera(): graph is a Group and the method belongs to Surface
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



# ----- From _2025/laplace/main_supplements.py -----

class PreviewAnalyticContinuation(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        plane = ComplexPlane((-3, 3), (-3, 3))
        plane.add_coordinate_labels(font_size=16)

        pole_values = [1 - 2.0j, -1 - 2.0j, 2 + 1j, -2 + 1j, 2.5j]
        graph = get_complex_graph(
            plane,
            lambda s: -1 * sum((np.divide(1, (s - p)) for p in pole_values))
        )
        graph.rotate(90 * DEG, about_point=plane.n2p(0))
        # CHANGE: graph is Group(surface, mesh) and set_sort_to_camera exists only on Surface; it is called on graph[0].
        graph[0].set_sort_to_camera()
        graph.set_opacity(0.8)

        frame.reorient(-1, 75, 0, (0.35, 0.49, 1.27), 7.85)
        self.add(plane, graph)
        self.play(
            ShowCreation(graph),
            frame.animate.reorient(-24, 72, 0, (0.97, 0.24, 0.97), 9.65),
            run_time=12
        )
