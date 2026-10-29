# ==============================================================================
# Scene:      SimplicityToGenerality
# Source:     videos/_2024/holograms/supplements.py (lines 1230-1296)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SimplicityToGenerality.py SimplicityToGenerality -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `Surface.get_shader_data()['point']` no longer exists: the triangle vertices are rebuilt from `get_points()` with the mesh indices of the previous version (same triangle list)
# ==============================================================================

from manim_imports_ext import *

class SimplicityToGenerality(InteractiveScene):
    def construct(self):
        # Initialize little triangles
        frame = self.frame
        surface = Torus(resolution=(49, 49))
        surface.set_width(4)
        # CHANGE: Surface no longer has get_shader_data (its points are the mesh and the shader builds the
        # triangles); the vertices of each triangle are rebuilt with the same index order the previous version used
        nu, nv = surface.get_resolution()
        index_grid = np.arange(nu * nv).reshape((nu, nv))
        indices = np.zeros(6 * (nu - 1) * (nv - 1), dtype=int)
        indices[0::6] = index_grid[:-1, :-1].flatten()  # Top left
        indices[1::6] = index_grid[+1:, :-1].flatten()  # Bottom left
        indices[2::6] = index_grid[:-1, +1:].flatten()  # Top right
        indices[3::6] = index_grid[:-1, +1:].flatten()  # Top right
        indices[4::6] = index_grid[+1:, :-1].flatten()  # Bottom left
        indices[5::6] = index_grid[+1:, +1:].flatten()  # Bottom right
        verts = surface.get_points()[indices]
        triangles = VGroup(
            Polygon(*tri)
            for tri in zip(verts[0::3], verts[1::3], verts[2::3])
        )
        triangles.set_stroke(WHITE, 0.5, 0.5)

        tri1 = triangles[3500]
        dists = [get_norm(tri.get_center() - tri1.get_center()) for tri in triangles]
        neighbors = VGroup(triangles[idx] for idx in np.argsort(dists))
        ng1 = neighbors[1:10]
        ng2 = neighbors[10:200]
        ng3 = neighbors[200:]
        for group in [ng1, ng2, ng3]:
            group.save_state()
            for tri in group:
                tri.become(tri1)
                tri.set_stroke(width=0.1, opacity=0.25)
        ng3.set_stroke(opacity=0.05)

        frame.reorient(4, 83, 0, (-0.11, -0.05, -0.34), 1.91)

        self.add(tri1)
        self.play(
            LaggedStart(
                Restore(ng1, lag_ratio=0.3),
                Restore(ng2, lag_ratio=0.02),
                Restore(ng3, lag_ratio=3e-4),
                lag_ratio=0.4
            ),
            frame.animate.reorient(29, 64, 0, (-0.15, 0.02, -0.43), 3.21),
            run_time=9,
        )
        self.add(triangles)

        # True surface
        equation = Tex(R"\left(x^2+y^2+z^2+R^2-r^2\right)^2=4 R^2\left(x^2+y^2\right)")
        equation.fix_in_frame()
        equation.to_edge(UP, buff=0.35)

        new_surface = ParametricSurface(
            lambda u, v: surface.uv_func(v, u),
            u_range=(0, TAU),
            v_range=(0, TAU),
            resolution=(250, 250)
        )
        new_surface.set_width(4)
        new_surface.set_opacity(0.5)
        new_surface.always_sort_to_camera(self.camera)

        triangles.shuffle()
        self.play(
            FadeOut(triangles, scale=0.8, lag_ratio=3e-4),
            frame.animate.reorient(77, 62, 0, (-0.27, -0.05, -0.23), 4.29),
            run_time=2
        )
        self.play(
            ShowCreation(new_surface, run_time=3),
            frame.animate.reorient(58, 66, 0, (-0.27, -0.05, -0.23), 4.29).set_anim_args(run_time=4),
        )
        self.play(frame.animate.reorient(50, 79, 0, (-0.27, -0.05, -0.23), 4.29), run_time=3)
