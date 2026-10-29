# ==============================================================================
# Scene:      ConvexityPrelude
# Source:     videos/_2021/shadows.py (lines 4472-4589)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ConvexityPrelude.py ConvexityPrelude -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ConvexityPrelude(Scene):
    def construct(self):
        square = Square(side_length=3)
        square.rotate(-PI / 4)
        square.flip()
        square.set_stroke(BLUE, 2)

        points = [square.pfp(1 / 8), square.pfp(7 / 8)]

        beam = VGroup(
            Line(points[0] + 3 * UP, points[0], stroke_width=3),
            Line(points[0], points[1], stroke_width=2),
            Line(points[1], points[1] + 3 * DOWN, stroke_width=1),
        )

        beam.set_stroke(YELLOW)

        words = OldTexText("2 intersections\\\\", "(almost always)")
        words[1].scale(0.7, about_edge=UP).set_color(GREY_B)
        words.to_edge(LEFT)
        arrows = VGroup(*(
            Arrow(words[0].get_right(), point)
            for point in points
        ))

        dots = GlowDot()
        dots.set_points(points)
        dots.set_color(WHITE)
        dots.set_radius(0.2)
        dots.set_glow_factor(3)

        self.add(square)
        self.add(words)
        self.play(
            ShowCreation(beam),
            FadeIn(arrows, lag_ratio=0.7),
            FadeIn(dots, lag_ratio=0.7),
        )
        self.wait()

        question1 = Text("Why is this true?")
        question2 = Text("Is this true for all shapes?")
        question2.next_to(question1, DOWN, aligned_edge=LEFT)
        VGroup(question1, question2).to_corner(UR)

        self.play(Write(question1, run_time=1))
        self.wait()
        self.play(FadeIn(question2, 0.25 * DOWN))
        self.wait()

        # Convexity
        square.generate_target()
        convex_shapes = VGroup(
            square.target,
            RegularPolygon(5, color=TEAL),
            Rectangle(2, 1, color=TEAL_E),
            RegularPolygon(6, color=GREEN),
            Circle(color=GREEN_B),
        )
        convex_shapes[2].apply_matrix([[1, 0.5], [0, 1]])
        convex_shapes[3].shift(2 * RIGHT).apply_complex_function(np.exp)
        convex_shapes[3].make_jagged()
        for shape in convex_shapes:
            shape.set_height(1)
            shape.set_stroke(width=2)
        convex_shapes.arrange(DOWN)
        convex_shapes.set_height(6)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.set_y(3)
        VGroup(v_line, h_line).set_stroke(WHITE, 2)
        convex_title = Text("Convex")
        non_convex_title = Text("Non-convex")
        for title, vect in zip([convex_title, non_convex_title], [LEFT, RIGHT]):
            title.scale(1.5)
            title.next_to(h_line, UP)
            title.shift(vect * FRAME_WIDTH / 4)

        convex_shapes.next_to(h_line, DOWN)
        convex_shapes.match_x(convex_title)

        self.play(
            MoveToTarget(square),
            FadeIn(convex_shapes[1:], lag_ratio=0.5),
            FadeTransform(beam, v_line),
            ShowCreation(h_line),
            FadeIn(convex_title),
            LaggedStart(*map(FadeOut, (
                dots, arrows, words,
                question1, question2,
            ))),
        )
        self.wait()

        # Non-convex shapes
        pi = OldTex("\\pi").family_members_with_points()[0]
        pent = RegularPolygon(5)
        pent.set_points_as_corners([ORIGIN, *pent.get_vertices()[1:], ORIGIN])
        n_mob = OldTex("N").family_members_with_points()[0]
        nc_shapes = VGroup(pi, pent, n_mob)
        nc_shapes.set_fill(opacity=0)
        nc_shapes.set_stroke(width=2)
        nc_shapes.set_submobject_colors_by_gradient(RED, PINK)
        for shape in nc_shapes:
            shape.set_height(1)
        nc_shapes.arrange(DOWN)
        nc_shapes.replace(convex_shapes, dim_to_match=1)
        nc_shapes.match_x(non_convex_title)

        self.play(
            Write(non_convex_title, run_time=1),
            LaggedStartMap(FadeIn, nc_shapes),
        )
        self.wait()

        # Embed
        self.embed()
