# ==============================================================================
# Scene:      WhyComplexNumbers
# Source:     videos/_2026/print_gallery/conformal_maps.py (lines 704-804)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyComplexNumbers.py WhyComplexNumbers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyComplexNumbers(InteractiveScene):
    def construct(self):
        # Create two planes
        x_max = 4
        in_plane, out_plane = planes = VGroup(
            NumberPlane((-x_max, x_max), (-x_max, x_max)),
            NumberPlane((-x_max, x_max), (-x_max, x_max)),
        )
        planes.set_height(5)
        planes.arrange(RIGHT, buff=2)

        squares = Square().get_grid(2 * x_max * 5, 2 * x_max * 5, buff=0).match_width(in_plane)
        squares.replace(in_plane)
        squares.set_stroke(WHITE, 1, 0.5)

        moving_plane = squares.copy()
        moving_plane.insert_n_curves(10)
        moving_plane.generate_target()

        def func(p):
            return out_plane.c2p(in_plane.p2c(p)[0] + in_plane.p2c(p)[1], 2 * in_plane.p2c(p)[0] * in_plane.p2c(p)[1])

        moving_plane.target.apply_function(func)
        # moving_plane.set_clip_plane(RIGHT, 8)
        # moving_plane.target.set_clip_plane(RIGHT, 0)

        in_plane.set_stroke(GREY_D, 1)
        out_plane.set_stroke(GREY_D, 1)

        # Draw the input and output space
        f_of_x_y = Tex(
            "f(x, y) = (x + y, 2xy)",
            font_size=55,
            tex_to_color_map={"f": PINK, "x": RED, "y": GREEN}
        ).set_stroke(
            width=15, color=BLACK, behind=True
        ).next_to(
            out_plane, UP
        )
        x_y_copy = f_of_x_y["(x, y)"].copy().next_to(
            in_plane, UP
        )
        self.add(in_plane, out_plane, moving_plane, Point(), x_y_copy, f_of_x_y)

        # Show the transformation
        square_index = 499
        moving_plane.save_state()
        self.camera.frame.save_state()
        self.play(FadeIn(moving_plane))
        square = moving_plane[square_index]
        moving_plane.target[square_index].set_stroke(width=6, color=BLUE, opacity=1)
        self.play(square.animate.set_stroke(width=6, color=BLUE, opacity=1))
        self.wait(2)
        target_center_in_input = moving_plane[square_index].get_center()
        self.play(self.camera.frame.animate(run_time=4).restore(), MoveToTarget(moving_plane, run_time=6))
        self.wait(1)

        # Zoom in on grid to show limiting behavior
        zoomed_in_planes = []
        frame = self.camera.frame
        initial_area = frame.get_width() * frame.get_height()

        for i in range(1, 7):
            grid_res = 20
            grid_width = in_plane.get_width() / (2**i)

            squares = Square().get_grid(grid_res, grid_res, buff=0)
            squares.set_width(grid_width)
            squares.move_to(target_center_in_input)

            plane = squares.copy()
            plane.insert_n_curves(5)
            plane.set_stroke(width=2 / (2**i), color=WHITE)
            plane.apply_function(func)

            def update_opacity(m, index=i):
                current_area = frame.get_width() * frame.get_height()
                start_a = initial_area / (4**index)
                end_a = initial_area / (4**(index + 1))

                if start_a == end_a:
                    alpha = 1
                else:
                    alpha = (current_area - start_a) / (end_a - start_a)

                alpha = max(0, min(1, alpha))
                m.set_stroke(opacity=alpha)

            plane.add_updater(update_opacity)
            zoomed_in_planes.append(plane)
            self.add(plane)

        self.play(
            FadeOut(moving_plane[square_index]),
            frame.animate.scale(
                2**-(len(zoomed_in_planes) + 1),
                about_point=moving_plane.target[square_index].get_center()
            ),
            run_time=12
        )
        self.wait(3)
