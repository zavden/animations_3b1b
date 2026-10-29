# ==============================================================================
# Scene:      MoreComplicatedExamples1
# Source:     videos/_2026/print_gallery/conformal_maps.py (lines 490-701)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MoreComplicatedExamples1.py MoreComplicatedExamples1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MoreComplicatedExamples1(InteractiveScene):
    def construct(self):
        # Show f(z) = z^2
        f_of_z = Tex(
            "f(z) = z^2", font_size=120, tex_to_color_map={"f": PINK, "z": YELLOW}
        ).set_stroke(width=10, color=BLACK, behind=True)
        self.play(Write(f_of_z, stroke_color=WHITE))
        self.wait(0.5)

        # Create two planes
        x_max = 4
        in_plane, out_plane = planes = VGroup(
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
            ComplexPlane((-x_max, x_max), (-x_max, x_max)),
        )
        planes.set_height(5)
        planes.arrange(RIGHT, buff=2)

        squares = Square().get_grid(2 * x_max * 5, 2 * x_max * 5, buff=0)
        squares.replace(in_plane)
        squares.set_stroke(WHITE, 1, 0.5)

        in_plane.add_coordinate_labels(
            list(range(-x_max, x_max + 1)) + [x * 1j for x in list(range(-x_max, x_max + 1)) if x != 0],
            font_size=16
        )
        out_plane.add_coordinate_labels(
            list(range(-x_max, x_max + 1)) + [x * 1j for x in list(range(-x_max, x_max + 1)) if x != 0],
            font_size=16
        )

        moving_plane = squares.copy()
        moving_plane.insert_n_curves(10)
        moving_plane.target = moving_plane.generate_target()
        moving_plane.target.apply_function(lambda p: out_plane.n2p(in_plane.p2n(p)**2))
        moving_plane.target.set_color(PINK)
        # moving_plane.set_clip_plane(RIGHT, 8)
        # moving_plane.target.set_clip_plane(RIGHT, 0)

        in_plane.set_stroke(GREY_D, 1)
        out_plane.set_stroke(GREY_D, 1)

        # Draw the input and output space
        zCopy = f_of_z[2].copy()
        self.play(
            zCopy.animate.scale(0.5).next_to(in_plane, UP),
            f_of_z.animate.scale(0.5).next_to(out_plane, UP),
            FadeIn(in_plane, shift=UP),
            FadeIn(out_plane, shift=UP), run_time=1.5)

        # Evaluate f(2)
        f_of_2 = Tex("f({2}) = {2}^2 = 4", font_size=20, tex_to_color_map={"f": PINK, "{2}": YELLOW}).align_to(in_plane, UP)
        twoDot = Group(TrueDot(), GlowDot()).move_to(in_plane.n2p(2))
        self.play(FadeIn(twoDot))
        twoDotResult = twoDot.copy().set_color(PINK).move_to(out_plane.n2p(4))
        self.play(Write(f_of_2), TransformFromCopy(twoDot, twoDotResult, path_arc=-PI * 0.3), run_time=3)

        # Evaluate f(i)
        f_of_i = Tex("f({i}) = {i}^2 = -1", font_size=20, tex_to_color_map={"f": PINK, "{i}": YELLOW}).next_to(f_of_2, DOWN)
        iDot = Group(TrueDot(), GlowDot()).move_to(in_plane.n2p(1j))
        self.play(FadeIn(iDot))
        iDotResult = iDot.copy().set_color(PINK).move_to(out_plane.n2p(-1))
        self.play(Write(f_of_i), TransformFromCopy(iDot, iDotResult, path_arc=-PI * 0.3), run_time=3)

        # Evaluate f(-1)
        f_of_negative_1 = Tex("f({-1}) = ({-1})^2 = 1", font_size=20, tex_to_color_map={"f": PINK, "{-1}": YELLOW}).next_to(f_of_i, DOWN)
        negativeOneDot = Group(TrueDot(), GlowDot()).move_to(in_plane.n2p(-1))
        self.play(FadeIn(negativeOneDot))
        negativeOneDotResult = negativeOneDot.copy().set_color(PINK).move_to(out_plane.n2p(1))
        self.play(Write(f_of_negative_1), TransformFromCopy(negativeOneDot, negativeOneDotResult, path_arc=-PI * 0.3), run_time=3)
        self.wait(2)
        self.play(
            FadeOut(
                Group(f_of_2, twoDot, twoDotResult, f_of_i, iDot, iDotResult, f_of_negative_1, negativeOneDot, negativeOneDotResult)
            )
        )

        # Show the transformation
        square_index = 895
        for i in range(2):
            moving_plane.save_state()
            self.add(in_plane, out_plane, moving_plane, Point(), f_of_z)
            self.camera.frame.save_state()
            self.play(FadeIn(moving_plane))
            if i == 1:
                square = moving_plane[square_index]
                moving_plane.target[square_index].set_stroke(width=5, color=BLUE, opacity=1)
                self.play(
                    self.camera.frame.animate.scale(0.5, about_point=square.get_center()),
                    square.animate.set_stroke(width=5, color=BLUE, opacity=1), run_time=3)
                self.wait(2)
            self.play(self.camera.frame.animate(run_time=4).restore(), MoveToTarget(moving_plane, run_time=6))
            self.wait(2)
            if i == 0:
                self.play(FadeOut(moving_plane))
                moving_plane.restore()

        # Write "conformal map"
        conformalMapText = TexText(
            "``conformal map''", font_size=60
        ).set_stroke(
            width=13, color=BLACK, behind=True
        ).next_to(out_plane, DOWN)
        self.play(Write(conformalMapText, stroke_color=WHITE))
        self.wait(2)
        self.play(FadeOut(VGroup(moving_plane, conformalMapText)))

        squares = Square().get_grid(x_max * 5, x_max * 5, buff=0).set_width(in_plane[0].get_width() * 0.5)
        squares.set_stroke(WHITE, 1, 0.5)

        moving_plane = squares.copy()
        moving_plane.insert_n_curves(10)

        # Try f(z) = z^3
        moving_plane.align_to(in_plane, UR)
        moving_plane.generate_target()

        def func(p):
            return out_plane.n2p(in_plane.p2n(p)**3)

        moving_plane.target.apply_function(func)
        square_index = 304
        moving_plane.target[square_index].set_stroke(width=5, color=BLUE, opacity=1)
        f_of_z_2 = Tex(
            "f(z) = z^3", tex_to_color_map={"f": PINK, "z": YELLOW}
        ).set_stroke(
            width=10, color=BLACK, behind=True
        ).match_height(
            f_of_z
        ).move_to(
            f_of_z
        )
        self.play(FadeOut(f_of_z), FadeIn(f_of_z_2), FadeIn(moving_plane))
        self.play(moving_plane[square_index].animate.set_stroke(width=5, color=BLUE, opacity=1))
        target_center_in_input = moving_plane[square_index].get_center()
        self.play(MoveToTarget(moving_plane), run_time=6)
        self.add(moving_plane, Point(), f_of_z_2)

        # Try f(z) = e^z - 2iz - 3/z
        # moving_plane.align_to(in_plane[0], DL).shift(DL*0.01)
        # moving_plane.generate_target()
        # func = lambda p: out_plane.n2p(
        #     math.e**in_plane.p2n(p) - 2j*in_plane.p2n(p) - 3/(in_plane.p2n(p) if abs(in_plane.p2n(p)) > 0 else 0.001)
        # )
        # moving_plane.target.apply_function(func)
        # square_index = 70
        # moving_plane.target[square_index].set_stroke(width = 5, color = BLUE, opacity = 1)
        # f_of_z_3 = Tex(
        #     r"f(z) = e^z - 2iz - \displaystyle\frac{3}{z}", tex_to_color_map = {"f": PINK, "z": YELLOW}
        # ).set_stroke(
        #     width = 6, color = BLACK, behind = True
        # ).match_height(
        #     f_of_z
        # ).scale(1.2).move_to(
        #     f_of_z
        # ).align_to(
        #     f_of_z, UP
        # )
        # self.remove(f_of_z)
        # self.add(f_of_z_3)
        # self.wait(1)
        # self.play(FadeIn(moving_plane))
        # self.add(moving_plane, Point(), f_of_z_3)
        # self.play(moving_plane[square_index].animate.set_stroke(width = 5, color = BLUE, opacity = 1))
        # target_center_in_input = moving_plane[square_index].get_center()
        # self.play(MoveToTarget(moving_plane), run_time = 6)
        # self.wait(2)

        # Zoom in on grid to show limiting behavior
        zoomed_in_planes = []
        frame = self.camera.frame
        initial_area = frame.get_width() * frame.get_height()

        for i in range(1, 7):
            grid_res = 20
            grid_width = in_plane[0].get_width() / (2**(i + 1))

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
