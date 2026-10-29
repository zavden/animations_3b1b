# ==============================================================================
# Scene:      Prism
# Source:     videos/_2023/optics_puzzles/bending_waves.py (lines 700-829)
# Category:   1 · Renders unmodified
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl Prism.py Prism -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from matplotlib import colormaps


# ----- From _2023/optics_puzzles/objects.py -----

spectral_cmap = colormaps.get_cmap("Spectral")


def get_spectral_color(alpha):
    return Color(rgb=spectral_cmap(alpha)[:3])



# ----- From _2023/optics_puzzles/bending_waves.py -----

class Prism(InteractiveScene):
    def construct(self):
        # Add flat
        flat_prism = Triangle()
        flat_prism.set_height(4)
        flat_prism.set_stroke(WHITE, 1)
        flat_prism.set_fill(BLUE, 0.2)

        prism = Prismify(flat_prism, depth=5)
        prism.set_fill(BLUE_D, 0.25, border_width=0)
        prism.set_stroke(WHITE, 0)
        prism.sort(lambda p: -p[2])
        prism.apply_depth_test()
        prism.deactivate_depth_test()
        prism.set_shading(0.5, 0.5, 0)

        verts = flat_prism.get_vertices()
        in_edge = Line(verts[0], verts[1])
        out_edge = Line(verts[0], verts[2])

        self.add(flat_prism)

        # Beams of light
        frame = self.frame
        self.camera.light_source.move_to((-10, -10, 10))

        left_side = 10 * LEFT
        in_beam = Line(left_side, in_edge.get_center())
        in_beam.set_stroke(WHITE, 3)

        def get_beams(light_in):
            return self.get_beams(
                min_index=1.3,
                # max_index=1.4,
                max_index=1.45,
                n_beams=200,
                in_beam=light_in,
                in_edge=in_edge,
                out_edge=out_edge,
            )

        beams = always_redraw(lambda: get_beams(in_beam))
        self.play(
            ShowCreation(beams, time_span=(0.5, 1.5), lag_ratio=0),
            ShowCreation(in_beam, time_span=(0, 1.0)),
            rate_func=linear
        )

        # Show x-ray
        x_ray = self.get_beams(0.8, 0.8, 1, in_beam, in_edge, out_edge)
        x_ray.set_stroke("#FF00D5", 8)

        self.add(x_ray, in_beam)
        self.play(ShowCreation(x_ray, run_time=2))
        self.wait()
        self.remove(x_ray)

        # Transition to 3d
        self.play(
            FadeOut(flat_prism),
            FadeIn(prism),
            frame.animate.reorient(-90, 35, 90).set_height(15).move_to(RIGHT + 4 * DOWN),
            run_time=4,
        )
        turn_animation_into_updater(
            ApplyMethod(frame.reorient, -90, 10, 90, run_time=15)
        )

        # for vect, alpha in zip([DOWN, 2 * UP, ORIGIN], [0.3, 0.3, 0.5]):
        for vect, alpha in zip([5 * DOWN, 3 * DOWN, 4 * DOWN], [0.3, 0.3, 0.5]):
            self.play(
                in_beam.animate.put_start_and_end_on(left_side + vect, in_edge.pfp(alpha)),
                # run_time=5
            )

        # Back to 2d
        frame.clear_updaters()
        self.play(
            frame.animate.reorient(0, 0, 0).set_height(8),
            in_beam.animate.put_start_and_end_on(left_side + 2 * DOWN, in_edge.get_center()),
            FadeOut(prism, time_span=(1, 2)),
            FadeIn(flat_prism, time_span=(1, 2)),
            run_time=2,
        )

        self.wait()

    def get_beams(self, min_index, max_index, n_beams, in_beam, in_edge: Line, out_edge: Line):
        alphas = np.linspace(0, 1, n_beams)**1.5
        indices = interpolate(min_index, max_index, alphas)

        normal1 = rotate_vector(normalize(in_edge.get_vector()), PI / 2)
        normal2 = rotate_vector(normalize(out_edge.get_vector()), PI / 2)
        in_point = in_beam.get_end()
        vect1 = normalize(in_beam.get_vector())

        theta1 = angle_between_vectors(normal1, vect1)
        theta2s = np.arcsin(np.sin(theta1) / indices)
        vect2s = np.array([
            rotate_vector(normal1, theta2)
            for theta2 in theta2s
        ])
        out_points = np.array([
            find_intersection(in_point, vect2, out_edge.get_start(), out_edge.get_vector())
            for vect2 in vect2s
        ])
        theta3s = np.array([
            angle_between_vectors(normal2, vect2)
            for vect2 in vect2s
        ])
        theta4s = np.arcsin(np.sin(theta3s) * indices)
        vect3s = np.array([
            rotate_vector(normal2, -theta4)
            for theta4 in theta4s
        ])

        beams = VGroup(*(
            VMobject().set_points_as_corners([
                in_point - 1.0 * FRAME_WIDTH * vect1,
                in_point,
                out_point,
                out_point + 3.0 * FRAME_WIDTH * vect3
            ])
            for out_point, vect3 in zip(out_points, vect3s)
        ))

        for alpha, beam in zip(np.linspace(0, 1, n_beams), beams):
            beam.set_stroke(get_spectral_color(alpha), 1, opacity=0.8)

        return beams
