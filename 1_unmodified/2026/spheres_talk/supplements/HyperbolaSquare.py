# ==============================================================================
# Scene:      HyperbolaSquare
# Source:     videos/_2026/spheres_talk/supplements.py (lines 217-337)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HyperbolaSquare.py HyperbolaSquare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class HyperbolaSquare(InteractiveScene):
    def construct(self):
        # Label distances
        square = VGroup(
            Line(UL, UR),
            Line(UR, DR),
            Line(DR, DL),
            Line(DL, UL),
        )
        square.set_height(4)
        square_shadows = VGroup(
            square.copy().scale(0.95**n).shift(0.05 * DR * n).set_stroke(opacity=0.5 / n)
            for n in range(1, 20)
        )

        center_dot = Dot()
        center_dot.move_to(square)
        side_line = Line(square.get_center(), square.get_right())
        diag_line = Line(square.get_center(), square.get_corner(UR))
        side_line.set_stroke(BLUE, 3)
        diag_line.set_stroke(YELLOW, 3)

        side_label = Tex(R"1")
        side_label.next_to(side_line, DOWN, SMALL_BUFF)
        diag_label = Tex(R"\sqrt{N}")
        diag_label.next_to(diag_line.get_center(), UL, SMALL_BUFF)
        diag_label.set_backstroke(BLACK, 5)

        self.add(square)
        self.add(square_shadows)

        self.play(
            GrowFromCenter(center_dot),
            ShowCreation(side_line),
            FadeIn(side_label, 0.5 * RIGHT)
        )
        self.wait()
        self.play(
            ShowCreation(diag_line),
            FadeIn(diag_label, 0.5 * UR),
        )
        self.wait()

        # Warp it
        warp_square = self.get_warp_square(square)
        warp_square_shadows = VGroup(self.get_warp_square(ss) for ss in square_shadows)

        side_line.target = side_line.generate_target()
        side_line.target.put_start_and_end_on(center_dot.get_center(), warp_square[1].pfp(0.5))
        diag_line.target = diag_line.generate_target()
        diag_line.target.put_start_and_end_on(center_dot.get_center(), warp_square.get_corner(UR))

        self.wait()
        self.play(
            Transform(square, warp_square),
            Transform(square_shadows, warp_square_shadows),
            MoveToTarget(side_line),
            MoveToTarget(diag_line),
            side_label.animate.next_to(side_line.target, DOWN, SMALL_BUFF),
            diag_label.animate.shift(0.4 * DOWN + 0.2 * LEFT),
            run_time=3
        )
        self.wait()

        # Corner spheres
        frame = self.frame
        lil_radius = 0.6
        big_radius = diag_line.get_length() - lil_radius
        circles = Circle(radius=lil_radius).replicate(4)
        circles.set_stroke(BLUE, 3)
        circles.set_fill(BLUE, 0.25)
        for circle, side in zip(circles, warp_square):
            circle.move_to(side.get_start())

        big_circle = Circle(radius=big_radius)
        big_circle.set_stroke(GREEN, 3).set_fill(GREEN, 0.25)

        self.play(
            LaggedStartMap(GrowFromCenter, circles),
            frame.animate.set_height(9),
        )
        self.wait()
        self.play(GrowFromCenter(big_circle))
        self.wait()

        # Show many more corners
        group = VGroup(warp_square, circles)
        n_new_groups = 12
        angles = np.linspace(0, 90 * DEG, n_new_groups + 2)[1:-1]
        alt_groups = VGroup(
            group.copy().rotate(theta, about_point=ORIGIN)
            for theta in angles
        )
        alt_groups.fade(0.75)

        corner_label = Tex(R"2^N \text{ corners}", font_size=60)
        corner_label.to_corner(UR)
        corner_label.fix_in_frame()

        self.play(
            FadeIn(corner_label),
            LaggedStart(
                (TransformFromCopy(group.copy().set_fill(opacity=0), alt_group, path_arc=angle)
                for angle, alt_group in zip(angles, alt_groups)),
                lag_ratio=0.01,
                run_time=3
            ),
            frame.animate.set_height(11),
            run_time=3
        )
        self.wait()

    def get_warp_square(self, square, scale_factor=1.7):
        hyper = FunctionGraph(lambda x: math.sqrt(1 + x**2), x_range=(-2, 2, 0.02))
        warp_square = VGroup(
            hyper.copy().put_start_and_end_on(*side.get_start_and_end())
            for side in square
        )
        warp_square.scale(scale_factor)
        warp_square.match_style(square)
        return warp_square
