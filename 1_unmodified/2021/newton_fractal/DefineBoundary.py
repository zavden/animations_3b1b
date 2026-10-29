# ==============================================================================
# Scene:      DefineBoundary
# Source:     videos/_2021/newton_fractal.py (lines 3898-4048)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefineBoundary.py DefineBoundary -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefineBoundary(Scene):
    def construct(self):
        # Add set
        blob = VMobject()
        blob.set_fill(BLUE_E, 1)
        blob.set_stroke(width=0)
        blob.set_points_as_corners([
            (1 + 0.3 * random.random()) * p
            for p in compass_directions(12)
        ])
        blob.close_path()
        blob.set_height(3)
        blob.set_width(1.0, stretch=True)
        blob.move_to(2 * RIGHT)
        blob.apply_complex_function(np.exp)
        blob.make_smooth()
        blob.rotate(90 * DEGREES)
        blob.center()
        blob.set_height(4)
        blob.insert_n_curves(50)

        set_text = Text("Set", font_size=72)
        set_text.set_stroke(BLACK, 3, background=True)
        set_text.move_to(interpolate(blob.get_top(), blob.get_bottom(), 0.35))

        self.add(blob)
        self.add(set_text)

        # Preview boundary
        point = Dot(radius=0.05)
        point.move_to(blob.get_start())

        boundary_word = Text("Boundary")
        boundary_word.set_color(YELLOW)
        boundary_word.next_to(blob, LEFT)
        outline = blob.copy()
        outline.set_fill(opacity=0)
        outline.set_stroke(YELLOW, 2)

        self.add(point)

        kw = {
            "rate_func": bezier([0, 0, 1, 1]),
            "run_time": 5,
        }
        self.play(
            FadeIn(boundary_word),
            ShowCreation(outline, **kw),
            MoveAlongPath(point, blob, **kw)
        )
        self.play(FadeOut(outline))

        # Mention formality
        boundary_word.generate_target()
        boundary_word.target.to_corner(UL)
        formally_word = Text("More formally")
        formally_word.next_to(boundary_word.target, DOWN, aligned_edge=LEFT)

        self.play(
            MoveToTarget(boundary_word),
            FadeTransform(boundary_word.copy(), formally_word)
        )
        self.wait()

        # Draw circle
        circle = Circle()
        circle.move_to(point)
        circle.set_stroke(TEAL, 3.0)

        self.play(
            ShowCreation(circle),
            point.animate.scale(0.5),
        )
        self.wait()
        group = VGroup(blob, set_text)
        self.add(group, point, circle)
        self.play(
            ApplyMethod(
                group.scale, 2, {"about_point": point.get_center()},
                run_time=4
            ),
            ApplyMethod(
                circle.set_height, 0.5,
                run_time=2,
            ),
        )

        # Labels
        inside_words = Text("Points inside", font_size=36)
        outside_words = Text("Points outside", font_size=36)
        inside_words.next_to(circle, DOWN, buff=0.5).shift(0.5 * LEFT)
        outside_words.next_to(circle, UP, buff=0.5).shift(0.5 * RIGHT)
        inside_arrow = Arrow(
            inside_words, point,
            stroke_width=3,
            buff=0.1,
        )
        outside_arrow = Arrow(
            outside_words, point,
            stroke_width=3,
            buff=0.1,
        )

        self.play(
            FadeIn(inside_words),
            ShowCreation(inside_arrow)
        )
        self.play(
            FadeIn(outside_words),
            ShowCreation(outside_arrow)
        )
        self.wait()

        # Show interior
        point_group = VGroup(point, circle)

        self.play(
            point_group.animate.shift(circle.get_height() * DOWN / 4),
            LaggedStartMap(
                FadeOut, VGroup(inside_words, inside_arrow, outside_words, outside_arrow)
            )
        )
        self.wait()
        self.play(circle.animate.set_height(0.2))
        self.wait()

        # Show exterior
        point_group.generate_target()
        point_group.target.move_to(blob.get_start() + 0.25 * UP)
        point_group.target[1].set_height(1.0)

        self.play(MoveToTarget(point_group))
        self.wait()
        self.play(circle.animate.set_height(0.2))
        self.wait()

        # Back to boundary
        self.play(point_group.animate.move_to(blob.get_start()))
        frame = self.camera.frame
        frame.generate_target()
        frame.target.set_height(0.2)
        frame.target.move_to(point)
        point_group.generate_target()
        point_group.target.set_height(0.2 / 8)
        point_group.target[1].set_stroke(width=0.1)

        self.play(MoveToTarget(point_group))
        self.play(
            MoveToTarget(frame),
            run_time=4
        )
