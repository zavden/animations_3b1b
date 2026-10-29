# ==============================================================================
# Scene:      MobiusTransformation2BiggerGridTest
# Source:     videos/_2026/print_gallery/misc_scenes.py (lines 200-285)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl MobiusTransformation2BiggerGridTest.py MobiusTransformation2BiggerGridTest -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Grid reduced from 50x50 to 25x25 (scale 7.5 instead of 15, same square size) and 40 curves per square instead of 80: the original took ~19 s per frame (~2 h of render)
#
# Notes:
#   The published video is the one from the 360p, 10 fps test: at 720p it takes too long (more than 500 s at 360p).
# ==============================================================================

from manim_imports_ext import *

class MobiusTransformation2BiggerGridTest(InteractiveScene):
    def construct(self):
        # Create a unit plane
        unit_plane = ComplexPlane((-1, 1), (-1, 1))
        unit_plane.set_height(FRAME_HEIGHT * 0.85)
        unit_plane.add_coordinate_labels([-1, 0, 1, -1j, 1j])
        unit_plane.set_stroke(GREY_D, 1)
        self.add(unit_plane)

        # Set up updaters and dots
        angle_trackers = [
            ValueTracker(a) for a in sorted([random.uniform(0, TAU) for _ in range(3)])
        ]

        def get_mobius_func():
            z_ang, o_ang, i_ang = [t.get_value() for t in angle_trackers]

            w0 = np.exp(1j * z_ang)
            w1 = np.exp(1j * o_ang)
            winf = np.exp(1j * i_ang)

            a = winf
            c = 1
            d = (w1 - winf) / (w0 - w1)
            b = w0 * d

            return lambda z: (a * z + b) / (c * z + d)

        # CHANGE: the original grid (50x50 squares, 80 extra curves each, redrawn on every frame) took
        # ~19 s per frame (~2 h of render). It is reduced to 25x25 with scale(7.5) instead of 15 (same
        # square size, half the extent) and 40 curves per square.
        grid_size_x = 25
        grid_size_y = 25
        squares_template = Square().get_grid(grid_size_y, grid_size_x, buff=0)
        squares_template.match_width(unit_plane[0]).move_to(unit_plane[0]).align_to(unit_plane.n2p(0), DOWN)
        squares_template.scale(7.5, about_point=squares_template.get_bottom())
        squares_template.insert_n_curves(40)
        for square in squares_template:
            square.set_stroke(width=max(1, 3 / unit_plane.p2n(square.get_center()).imag**0.4))

        mobius_grid = always_redraw(lambda:
                                    squares_template.copy().set_submobject_colors_by_gradient(
                                        BLUE, YELLOW, interp_by_hsl=True
                                    ).apply_function(
                                        lambda p: unit_plane.n2p(get_mobius_func()(unit_plane.p2n(p)))
                                    )
                                    )
        self.add(mobius_grid)

        dots = always_redraw(lambda:
                             Group(
                                 Group(TrueDot(), GlowDot()).set_color(RED).move_to(unit_plane.n2p(get_mobius_func()(0))),
                                 Group(TrueDot(), GlowDot()).set_color(GREEN).move_to(unit_plane.n2p(get_mobius_func()(1))),
                                 Group(TrueDot(), GlowDot()).set_color(ORANGE).move_to(unit_plane.n2p(get_mobius_func()(1e8)))
                             )
                             )
        self.add(dots)

        # Move the dots around
        for i in range(6):
            min_gap = TAU / 8

            remaining_tau = TAU - (3 * min_gap)
            breaks = sorted([random.uniform(0, remaining_tau) for _ in range(2)])

            gaps = [
                breaks[0],
                breaks[1] - breaks[0],
                remaining_tau - breaks[1]
            ]

            new_angles = []
            current_angle = random.uniform(0, TAU)  # Random starting rotation
            for gap in gaps:
                current_angle += gap + min_gap
                new_angles.append(current_angle % TAU)

            new_angles.sort()

            animations = [
                angle_trackers[j].animate.set_value(new_angles[j])
                for j in range(3)
            ]

            self.play(
                *animations,
                run_time=3
            )
            self.wait(1)
