# ==============================================================================
# Scene:      ShowSolutionPoles
# Source:     videos/_2025/laplace/derivatives.py (lines 1377-1438)
# Category:   1 · Renders unmodified
# Includes code copied from: _2025/laplace/integration.py
#
# Run from this folder:
#     manimgl ShowSolutionPoles.py ShowSolutionPoles -w -m --fps 15
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



# ----- From _2025/laplace/derivatives.py -----

class ShowSolutionPoles(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        F_0 = 1
        m = 1
        k = 2
        mu = 2
        omega = 2

        def func(s):
            denom = (s**2 + omega**2) * (m * s**2 + mu * s + k)
            return np.divide(F_0 * s, denom)

        plane = ComplexPlane((-3, 3), (-3, 3), faded_line_ratio=0)
        plane.add_coordinate_labels(font_size=16)
        plot = get_complex_graph(plane, func)

        self.add(plane, plot)

        # Pan around
        self.play(
            frame.animate.reorient(45, 82, 0, (-0.54, 0.3, 1.06), 5.71),
            run_time=3
        )
        self.play(
            frame.animate.reorient(-31, 83, 0, (-0.13, 0.5, 1.02), 5.71),
            run_time=13,
        )
        self.wait()

        # Emphasize the four roots
        roots = [-1 + 1j, -1 - 1j, 2j, -2j]
        s_points = [plane.n2p(s) for s in roots]
        s_dots = Group(Group(TrueDot(p), GlowDot(p)) for p in s_points)
        s_dots.set_color(YELLOW)
        s_labels = VGroup(
            Tex(Rf"s_{n}").next_to(point, RIGHT)
            for n, point in enumerate(s_points, 1)
        )
        s_labels.set_color(YELLOW)
        s_labels.set_backstroke(BLACK, 5)

        self.play(
            frame.animate.to_default_state().set_field_of_view(1 * DEG),
            plot[0].animate.set_opacity(0.25),
            plot[1].animate.set_stroke(opacity=0.01),
            run_time=2
        )
        self.play(
            FadeIn(s_labels, lag_ratio=0.25),
            FadeIn(s_dots, lag_ratio=0.25),
        )
        self.wait()

        # Highlight certain roots
        rect = SurroundingRectangle(Group(s_labels[:2], s_dots[:2]))
        self.play(ShowCreation(rect))
        self.wait()
        self.play(rect.animate.surround(Group(s_labels[2:], s_dots[2:])))
        self.wait()
        self.play(FadeOut(rect))
