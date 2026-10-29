# ==============================================================================
# Scene:      MobiusTransformation1
# Source:     videos/_2026/print_gallery/misc_scenes.py (lines 111-197)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MobiusTransformation1.py MobiusTransformation1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MobiusTransformation1(InteractiveScene):
    def construct(self):
        # Create planes
        x_max = 3
        a_plane, b_plane, c_plane, d_plane, out_plane = planes = VGroup(
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-1, 1), (-1, 1)),
        )
        for plane in [a_plane, b_plane, c_plane, d_plane]:
            plane.set_width(2.5)
            plane.add_coordinate_labels(
                list(range(-x_max, x_max + 1)) + [x * 1j for x in list(range(-x_max, x_max + 1)) if x != 0],
                font_size=10
            )
            plane.coordinate_labels.shift(UR * 0.04)
            plane.set_stroke(GREY_D, 1)
        out_plane.set_width(5.5)
        out_plane.add_coordinate_labels([-1, 0, 1, -1j, 1j])
        out_plane.set_stroke(GREY_D, 1)
        VGroup(
            VGroup(a_plane, b_plane, c_plane, d_plane).arrange_in_grid(buff=0.2),
            out_plane
        ).arrange(buff=0.75).to_edge(DOWN, buff=0.5)
        VGroup(a_plane, b_plane, c_plane, d_plane).scale(1.02).shift(out_plane[0].get_bottom()[1] - c_plane[0].get_bottom()[1])
        self.add(planes)
        var_colors = [RED, GREEN, BLUE, ORANGE]
        f_of_z = Tex(
            r"f(z) = \displaystyle\frac{az + b}{cz + d}",
            font_size=32,
            tex_to_color_map={"f": PINK, "z": YELLOW, "a": var_colors[0], "b": var_colors[1], "c": var_colors[2], "d": var_colors[3]}
        ).set_stroke(
            width=7, color=BLACK, behind=True
        ).next_to(
            out_plane, UP, buff=0.2
        ).set_x(
            out_plane.c2p(0)[0]
        )
        self.add(f_of_z)

        # Add dots for a, b, c, and d
        # random.uniform(-x_max, x_max) + random.uniform(-x_max, x_max)*1j for _ in range(4)
        var_trackers = [ValueTracker([1, 0]), ValueTracker([0, 0]), ValueTracker([0, 0]), ValueTracker([0, 1])]
        dots = Group(*[Group(TrueDot(), GlowDot()).set_color(var_colors[i]) for i in range(4)])
        for i in range(len(dots)):
            dots[i].add_updater(lambda m, i=i: m.move_to(planes[i].n2p(complex(*var_trackers[i].get_value()))))
        labels = VGroup(*[
            Tex("abcd"[i], font_size=35).set_color(var_colors[i]).set_stroke(width=7, color=BLACK, behind=True)
            for i in range(4)
        ])
        for i in range(4):
            labels[i].add_updater(lambda m, i=i: m.next_to(dots[i], UR, buff=-0.1))
        self.add(dots, labels)

        # Add result_plane
        grid_size = 20
        squares = Square().get_grid(grid_size, grid_size, buff=0)
        squares.match_width(out_plane[0]).move_to(out_plane[0])
        squares.set_stroke(PINK, 1, 0.5)
        squares.insert_n_curves(10)
        squares.save_state()

        def update_squares(m):
            m.restore()
            m.apply_function(
                lambda z: out_plane.n2p(
                    (
                        complex(*var_trackers[0].get_value()) * out_plane.p2n(z) + complex(*var_trackers[1].get_value())
                    ) / (
                        complex(*var_trackers[2].get_value()) * out_plane.p2n(z) + complex(*var_trackers[3].get_value())
                    )
                )
            )
        squares.add_updater(update_squares)
        self.add(squares, f_of_z, planes[:4], dots, labels)

        # Move around a, b, c, and d
        for _ in range(6):
            new_variables_values = [[random.uniform(-x_max, x_max) for _ in range(2)] for _ in range(4)]
            self.play(
                AnimationGroup(*[
                    var_trackers[i].animate.set_value(new_variables_values[i])
                    for i in range(4)
                ]), run_time=3)
            self.wait(1)
