# ==============================================================================
# Scene:      NaiveLinearScaling
# Source:     videos/_2026/print_gallery/misc_scenes.py (lines 288-577)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NaiveLinearScaling.py NaiveLinearScaling -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NaiveLinearScaling(InteractiveScene):
    def construct(self):
        # Add the canvas
        canvas = Square(
            side_length=6,
            fill_opacity=0,
            stroke_width=5,
            stroke_color=WHITE
        )
        self.add(canvas)
        corners = [DR, DL, UL, UR]

        # Draw a little square in the bottom left
        square1b = Square(
            side_length=0.25,
            fill_opacity=0.7,
            fill_color=BLUE,
            stroke_width=0
        ).align_to(canvas, DR)
        square1b.shift(-corners[0] * square1b.get_width() * 1.5)
        self.play(DrawBorderThenFill(square1b))
        self.wait(2)

        # Scale a copy of the square up around the 4 corners
        square2a = square1b.copy().set_color(GREEN)
        self.play(FadeIn(square2a))
        lines_per_side = 4
        corner = 1
        connectingLines1 = always_redraw(
            lambda corner=corner: VGroup(*[
                Line(
                    square1b.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square1b.get_width() * i / (lines_per_side - 1),
                    square2a.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square2a.get_width() * i / (lines_per_side - 1), stroke_width=2
                ).set_color(YELLOW)
                for i in range(lines_per_side)
            ])
        )
        self.add(connectingLines1)
        self.bring_to_back(connectingLines1)
        self.bring_to_back(canvas)
        self.play(
            square2a.animate.scale(4).align_to(canvas, corners[1])
        )
        square2b = square1b.copy().align_to(square2a, corners[1]).shift(-corners[1] * square1b.get_width() * 1.5)

        square3a = square2b.copy().set_color(GREEN)
        self.play(FadeIn(square2b), FadeIn(square3a))
        corner = 2
        connectingLines2 = always_redraw(
            lambda corner=corner: VGroup(*[
                Line(
                    square2b.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square2b.get_width() * i / (lines_per_side - 1),
                    square3a.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square3a.get_width() * i / (lines_per_side - 1), stroke_width=2
                ).set_color(YELLOW)
                for i in range(lines_per_side)
            ])
        )
        self.add(connectingLines2)
        self.bring_to_back(connectingLines2)
        self.bring_to_back(canvas)
        self.play(
            square3a.animate.scale(4).align_to(canvas, UL)
        )
        square3b = square1b.copy().align_to(square3a, UL).shift(-corners[2] * square1b.get_width() * 1.5)

        square4a = square3b.copy().set_color(GREEN)
        self.play(FadeIn(square3b), FadeIn(square4a))
        corner = 3
        connectingLines3 = always_redraw(
            lambda corner=corner: VGroup(*[
                Line(
                    square3b.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square3b.get_width() * i / (lines_per_side - 1),
                    square4a.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square4a.get_width() * i / (lines_per_side - 1), stroke_width=2
                ).set_color(YELLOW)
                for i in range(lines_per_side)
            ])
        )
        self.add(connectingLines3)
        self.bring_to_back(connectingLines3)
        self.bring_to_back(canvas)
        self.play(
            square4a.animate.scale(4).align_to(canvas, UR)
        )
        square4b = square1b.copy().align_to(square4a, UR).shift(-corners[3] * square1b.get_width() * 1.5)

        square1a = square4b.copy().set_color(GREEN)
        self.play(FadeIn(square4b), FadeIn(square1a))
        corner = 0
        connectingLines4 = always_redraw(
            lambda corner=corner: VGroup(*[
                Line(
                    square4b.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square4b.get_width() * i / (lines_per_side - 1),
                    square1a.get_corner(corners[corner]) + (corners[(corner + 1) % 4] - corners[corner]) * 0.5 * square1a.get_width() * i / (lines_per_side - 1), stroke_width=2
                ).set_color(YELLOW)
                for i in range(lines_per_side)
            ])
        )
        self.add(connectingLines4)
        self.bring_to_back(connectingLines4)
        self.bring_to_back(canvas)
        self.play(
            square1a.animate.scale(4).align_to(canvas, DR)
        )

        # Zoom in on one of the corners
        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.reorient(0, 0, 0, (np.float32(-2.06), np.float32(-2.52), np.float32(0.0)), 1.20),
            run_time=2.5
        )

        # Show the pressure from the right and the bottom
        moving_square_from_right = square2b.copy().scale(
            0.7
        ).set_stroke(
            color=RED, width=5
        ).set_fill(
            opacity=0
        ).align_to(
            self.camera.frame.get_right(), LEFT
        ).shift(RIGHT * 0.2)
        self.add(moving_square_from_right)
        moving_square_from_right.generate_target()
        trapezoid1 = Polygon(
            [1.9, 1, 0],
            [0, 1.15, 0],
            [0, -1.15, 0],
            [1.9, -1, 0],
            fill_opacity=0,
            stroke_width=5,
            stroke_color=RED,
        )
        trapezoid1.match_height(moving_square_from_right).scale(1.2).scale(1 / 0.7).move_to(square2b)
        moving_square_from_right.target.become(trapezoid1)
        self.bring_to_front(square2b)
        # effectExaggerated = TexText(r"$^*$Effect exaggerated for demonstration", font_size = 9).set_color(WHITE).align_to(self.camera.frame.get_corner(UR), UR).shift(DL*0.1 + DOWN*0.06)

        moving_square_from_bottom = square2b.copy().scale(
            0.7
        ).set_stroke(
            color=ORANGE, width=5
        ).set_fill(
            opacity=0
        ).align_to(
            self.camera.frame.get_bottom(), UP
        ).shift(DOWN * 0.2)
        self.add(moving_square_from_bottom)
        moving_square_from_bottom.generate_target()

        v1 = trapezoid1.get_vertices()
        v2 = [rotate_vector(v, -PI * 0.5) for v in v1]
        v2_cycled = v2[1:] + [v2[0]]

        trapezoid2 = Polygon(*v2_cycled)
        trapezoid2.set_color(ORANGE).set_stroke(width=5).move_to(square2b)

        self.add(VGroup(moving_square_from_bottom, moving_square_from_right), Point(), square2b)
        moving_square_from_bottom.target.become(trapezoid2)
        self.play(
            MoveToTarget(moving_square_from_bottom),
            MoveToTarget(moving_square_from_right),
            square2b.animate.set_opacity(0.6), run_time=5)
        self.wait(2)
        self.add(VGroup(moving_square_from_bottom, moving_square_from_right), Point(), square2b)
        self.play(FadeOut(moving_square_from_bottom), FadeOut(moving_square_from_right), square2b.animate.set_opacity(1))

        # Wiggle the square to try to fit the two different shapes
        square2b.save_state()
        connectingLines1.clear_updaters()
        connectingLines2.clear_updaters()
        connectingLines3.clear_updaters()
        connectingLines4.clear_updaters()
        # self.play(self.camera.frame.animate.scale(0.8, about_point = square2b.get_center()).shift(LEFT*0.25), run_time = 2)
        shift_amt = 0.01
        for i in range(3):
            self.add(connectingLines2, Point(), square2b)
            self.play(
                AnimationGroup(
                    connectingLines1[0].animate.put_start_and_end_on(
                        connectingLines1[0].get_start() + LEFT * 3.3, connectingLines1[0].get_end()
                    ),
                    connectingLines1[1].animate.put_start_and_end_on(
                        connectingLines1[1].get_start() + LEFT * 3.3, connectingLines1[1].get_end()),
                    connectingLines1[2].animate.put_start_and_end_on(
                        connectingLines1[2].get_start() + LEFT * 3.3, connectingLines1[2].get_end()),
                    connectingLines1[3].animate.put_start_and_end_on(
                        connectingLines1[3].get_start() + LEFT * 3.3, connectingLines1[3].get_end()),
                    square2b.animate.shift(0)
                ) if i == 0 else
                AnimationGroup(
                    connectingLines1[0].animate.put_start_and_end_on(
                        connectingLines1[0].get_start() + RIGHT * 3.3, connectingLines1[0].get_end()
                    ),
                    connectingLines1[1].animate.put_start_and_end_on(
                        connectingLines1[1].get_start() + RIGHT * 3.3, connectingLines1[1].get_end()
                    ),
                    connectingLines1[2].animate.put_start_and_end_on(
                        connectingLines1[2].get_start() + RIGHT * 3.3, connectingLines1[2].get_end()
                    ),
                    connectingLines1[3].animate.put_start_and_end_on(
                        connectingLines1[3].get_start() + RIGHT * 3.3, connectingLines1[3].get_end()
                    ),
                    connectingLines2[0].animate.put_start_and_end_on(
                        connectingLines2[0].get_start() + LEFT * 2 * shift_amt, connectingLines2[0].get_end()
                    ),
                    connectingLines2[1].animate.put_start_and_end_on(
                        connectingLines2[1].get_start() + LEFT * shift_amt, connectingLines2[1].get_end()
                    ),
                    connectingLines2[2].animate.put_start_and_end_on(
                        connectingLines2[2].get_start() + RIGHT * shift_amt, connectingLines2[2].get_end()
                    ),
                    connectingLines2[3].animate.put_start_and_end_on(
                        connectingLines2[3].get_start() + RIGHT * 2 * shift_amt, connectingLines2[3].get_end()
                    ),
                    square2b.animate.shift(0)
                ) if i % 2 == 1 else
                AnimationGroup(
                    connectingLines2[0].animate.put_start_and_end_on(
                        connectingLines2[0].get_start() + RIGHT * 2 * shift_amt, connectingLines2[0].get_end()
                    ),
                    connectingLines2[1].animate.put_start_and_end_on(
                        connectingLines2[1].get_start() + RIGHT * shift_amt, connectingLines2[1].get_end()
                    ),
                    connectingLines2[2].animate.put_start_and_end_on(
                        connectingLines2[2].get_start() + LEFT * shift_amt, connectingLines2[2].get_end()
                    ),
                    connectingLines2[3].animate.put_start_and_end_on(
                        connectingLines2[3].get_start() + LEFT * 2 * shift_amt, connectingLines2[3].get_end()
                    ),
                    square2b.animate.shift(0)
                ),
                square2b.animate.match_points(
                    trapezoid1.copy() if i % 2 == 0 else trapezoid2.copy()
                ) if i < 2 else square2b.animate.restore(),
                run_time=1.5
            )
            self.wait(1.5)

        # Turn the lines into curves
        self.bring_to_front(VGroup(square1b, square2b, square3b, square4b).set_opacity(1))
        self.play(self.camera.frame.animate.restore(), run_time=2)
        offset = 3
        self.play(
            *[
                line.animate.become(
                    CubicBezier(
                        line.get_start(),
                        line.get_start() + LEFT * offset,
                        line.get_end() + RIGHT * offset,
                        line.get_end()
                    ).set_color(YELLOW).set_stroke(width=2)
                )
                for line in connectingLines1
            ],
            *[
                line.animate.become(
                    CubicBezier(
                        line.get_start(),
                        line.get_start() + UP * offset,
                        line.get_end() + DOWN * offset,
                        line.get_end()
                    ).set_color(YELLOW).set_stroke(width=2)
                )
                for line in connectingLines2
            ],
            *[
                line.animate.become(
                    CubicBezier(
                        line.get_start(),
                        line.get_start() + RIGHT * offset,
                        line.get_end() + LEFT * offset,
                        line.get_end()
                    ).set_color(YELLOW).set_stroke(width=2)
                )
                for line in connectingLines3
            ],
            *[
                line.animate.become(
                    CubicBezier(
                        line.get_start(),
                        line.get_start() + DOWN * offset,
                        line.get_end() + UP * offset,
                        line.get_end()
                    ).set_color(YELLOW).set_stroke(width=2)
                )
                for line in connectingLines4
            ],
            run_time=1
        )
        self.wait(2)
