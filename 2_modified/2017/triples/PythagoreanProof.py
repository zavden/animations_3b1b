# ==============================================================================
# Scene:      PythagoreanProof
# Source:     videos/_2017/triples.py (lines 318-483)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PythagoreanProof.py PythagoreanProof -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - fork bug: with draw_together the render fails with "min_storage_buffer_offset_alignment" (unaligned GPU offsets); draw each mobject separately (slower)
# ==============================================================================

from manim_imports_ext import *

A_COLOR = BLUE


B_COLOR = GREEN


C_COLOR = YELLOW


SIDE_COLORS = [A_COLOR, B_COLOR, C_COLOR]


# CHANGE: fork bug: with draw_together the render fails with "min_storage_buffer_offset_alignment" (unaligned GPU offsets); draw each mobject separately (slower)
class PythagoreanProof(Scene):
    default_camera_config = {"draw_together": False}
    def construct(self):
        self.add_title()
        self.show_proof()

    def add_title(self):
        title = OldTex("a^2", "+", "b^2", "=", "c^2")
        for color, char in zip(SIDE_COLORS, "abc"):
            title.set_color_by_tex(char, color)
        title.to_edge(UP)
        self.add(title)
        self.title = title

    def show_proof(self):
        triangle = Polygon(
            ORIGIN, 5*RIGHT, 5*RIGHT+12*UP,
            stroke_color = WHITE,
            stroke_width = 2,
            fill_color = WHITE,
            fill_opacity = 0.5
        )
        triangle.set_height(3)
        triangle.center()
        side_labels = self.get_triangle_side_labels(triangle)
        triangle_copy = triangle.copy()
        squares = self.get_abc_squares(triangle)
        a_square, b_square, c_square = squares


        self.add(triangle, triangle_copy)
        self.play(Write(side_labels))
        self.wait()
        self.play(*list(map(DrawBorderThenFill, squares)))
        self.add_labels_to_squares(squares, side_labels)
        self.wait()
        self.play(
            VGroup(triangle_copy, a_square, b_square).move_to, 
                4*LEFT+2*DOWN, DOWN,
            VGroup(triangle, c_square).move_to, 
                4*RIGHT+2*DOWN, DOWN,
            run_time = 2,
            path_arc = np.pi/2,
        )
        self.wait()
        self.add_new_triangles(
            triangle, 
            self.get_added_triangles_to_c_square(triangle, c_square)
        )
        self.wait()
        self.add_new_triangles(
            triangle_copy,
            self.get_added_triangles_to_ab_squares(triangle_copy, a_square)
        )
        self.wait()

        big_squares = VGroup(*list(map(
            self.get_big_square,
            [triangle, triangle_copy]
        )))
        negative_space_words = OldTexText(
            "Same negative \\\\ space"
        )
        negative_space_words.scale(0.75)
        negative_space_words.shift(UP)
        double_arrow = DoubleArrow(LEFT, RIGHT)
        double_arrow.next_to(negative_space_words, DOWN)

        self.play(
            FadeIn(big_squares), 
            Write(negative_space_words), 
            ShowCreation(double_arrow),
            *list(map(FadeOut, squares))
        )
        self.wait(2)
        self.play(*it.chain(
            list(map(FadeIn, squares)),
            list(map(Animation, big_squares)),
        ))
        self.wait(2)

    def add_labels_to_squares(self, squares, side_labels):
        for label, square in zip(side_labels, squares):
            label.target = OldTex(label.get_tex() + "^2")
            label.target.set_color(label.get_color())
            # label.target.scale(0.7)
            label.target.move_to(square)
            square.add(label)

        self.play(LaggedStartMap(MoveToTarget, side_labels))

    def add_new_triangles(self, triangle, added_triangles):
        brace = Brace(added_triangles, DOWN)
        label = OldTex("a", "+", "b")
        label.set_color_by_tex("a", A_COLOR)
        label.set_color_by_tex("b", B_COLOR)
        label.next_to(brace, DOWN)

        self.play(ReplacementTransform(
            VGroup(triangle.copy().set_fill(opacity = 0)),
            added_triangles,
            run_time = 2,
        ))
        self.play(GrowFromCenter(brace))
        self.play(Write(label))
        triangle.added_triangles = added_triangles

    def get_big_square(self, triangle):
        square = Square(stroke_color = RED)
        square.replace(
            VGroup(triangle, triangle.added_triangles),
            stretch = True
        )
        square.scale(1.01)
        return square

    #####

    def get_triangle_side_labels(self, triangle):
        a, b, c = list(map(Tex, "abc"))
        for mob, color in zip([a, b, c], SIDE_COLORS):
            mob.set_color(color)
        a.next_to(triangle, DOWN)
        b.next_to(triangle, RIGHT)
        c.next_to(triangle.get_center(), LEFT)
        return VGroup(a, b, c)

    def get_abc_squares(self, triangle):
        a_square, b_square, c_square = squares = [
            Square(
                stroke_color = color,
                fill_color = color,
                fill_opacity = 0.5,
            )
            for color in SIDE_COLORS
        ]
        a_square.set_width(triangle.get_width())
        a_square.move_to(triangle.get_bottom(), UP)
        b_square.set_height(triangle.get_height())
        b_square.move_to(triangle.get_right(), LEFT)
        hyp_line = Line(
            triangle.get_corner(UP+RIGHT),
            triangle.get_corner(DOWN+LEFT),
        )
        c_square.set_width(hyp_line.get_length())
        c_square.move_to(hyp_line.get_center(), UP)
        c_square.rotate(
            hyp_line.get_angle(), 
            about_point = hyp_line.get_center()
        )

        return a_square, b_square, c_square

    def get_added_triangles_to_c_square(self, triangle, c_square):
        return VGroup(*[
            triangle.copy().rotate(i*np.pi/2, about_point = c_square.get_center())
            for i in range(1, 4)
        ])

    def get_added_triangles_to_ab_squares(self, triangle, a_square):
        t1 = triangle.copy()
        t1.rotate(np.pi)
        group = VGroup(triangle, t1).copy()
        group.rotate(-np.pi/2)
        group.move_to(a_square.get_right(), LEFT)
        t2, t3 = group
        return VGroup(t1, t2, t3)
