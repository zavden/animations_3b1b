# ==============================================================================
# Scene:      MultiplicationByI
# Source:     videos/_2025/laplace/prequel_equations.py (lines 409-542)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MultiplicationByI.py MultiplicationByI -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MultiplicationByI(InteractiveScene):
    def construct(self):
        # Example number
        plane = ComplexPlane(
            background_line_style=dict(stroke_color=BLUE, stroke_width=1),
            # faded_line_style=dict(stroke_color=BLUE, stroke_width=0.5, stroke_opacity=0.5),
        )
        plane.add_coordinate_labels(font_size=24)

        z = 3 + 2j
        tex_kw = dict(t2c={"a": YELLOW, "b": PINK})

        vect = Vector(plane.n2p(z), fill_color=WHITE, thickness=4)
        vect_label = Tex(R"a + bi", **tex_kw)
        vect_label.next_to(vect.get_end(), UR, SMALL_BUFF)
        vect_label.set_backstroke(BLACK, 5)

        lines = VGroup(
            Line(ORIGIN, plane.n2p(z.real)).set_color(YELLOW),
            Line(plane.n2p(z.real), plane.n2p(z)).set_color(PINK),
        )
        a_label, b_label = line_labels = VGroup(
            Tex(R"a", font_size=36, **tex_kw).next_to(lines[0], UP, SMALL_BUFF),
            Tex(R"bi", font_size=36, **tex_kw).next_to(lines[1], RIGHT, SMALL_BUFF),
        )
        line_labels.set_backstroke(BLACK, 5)

        self.add(plane, Point(), plane.coordinate_labels)
        self.add(vect)
        self.add(vect_label)
        for line, label in zip(lines, line_labels):
            self.play(
                ShowCreation(line),
                FadeIn(label, 0.25 * line.get_vector())
            )
        self.wait()

        # Multiply components by i
        new_lines = lines.copy()
        new_lines.rotate(90 * DEG, about_point=ORIGIN)
        new_lines[1].move_to(ORIGIN, RIGHT)

        new_a_label = Tex(R"ai", font_size=36, **tex_kw).next_to(new_lines[0], RIGHT, SMALL_BUFF)
        new_b_label = Tex(R"bi \cdot i", font_size=36, **tex_kw).next_to(new_lines[1], UP, SMALL_BUFF)
        neg_b_label = Tex(R"=-b", font_size=36, **tex_kw)
        neg_b_label.move_to(new_b_label.get_right())

        mult_i_label = Tex(R"\times i", font_size=90)
        mult_i_label.set_backstroke(BLACK, 5)
        mult_i_label.to_corner(UR, buff=MED_LARGE_BUFF).shift(0.2 * UP)

        self.play(Write(mult_i_label))
        self.wait()
        self.play(
            TransformFromCopy(lines[0], new_lines[0], path_arc=90 * DEG),
            TransformFromCopy(a_label[0], new_a_label[0], path_arc=90 * DEG),
            TransformFromCopy(mult_i_label[1], new_a_label[1]),
        )
        self.wait()
        self.play(
            TransformFromCopy(lines[1], new_lines[1], path_arc=90 * DEG),
            TransformFromCopy(b_label[0], new_b_label[:-1], path_arc=90 * DEG),
            TransformFromCopy(mult_i_label[1], new_b_label[-1]),
        )
        self.wait()
        self.play(
            FlashAround(VGroup(new_b_label, new_lines[1]), color=PINK, time_width=1.5, run_time=2),
            new_b_label.animate.next_to(neg_b_label, LEFT, SMALL_BUFF),
            FadeIn(neg_b_label, SMALL_BUFF * RIGHT),
        )
        self.wait()
        self.play(VGroup(new_lines[1], new_b_label, neg_b_label).animate.shift(new_lines[0].get_vector()))

        # New vector
        vect_copy = vect.copy()
        elbow = Elbow().rotate(vect.get_angle(), about_point=ORIGIN)
        self.play(
            Rotate(vect_copy, 90 * DEG, run_time=2, about_point=ORIGIN),
        )
        self.play(
            ShowCreation(elbow)
        )
        self.wait()

    def old_material(self):
        # Show the algebra
        algebra = VGroup(
            Tex(R"i \cdot (a + bi)", **tex_kw),
            Tex(R"ai + bi^2", **tex_kw),
            Tex(R"-b + ai", **tex_kw),
        )
        algebra.set_backstroke(BLACK, 8)
        algebra.arrange(DOWN, buff=0.35)
        algebra.to_corner(UL)

        self.play(
            TransformFromCopy(vect_label, algebra[0]["a + bi"][0]),
            FadeIn(algebra[0]),
        )
        self.play(LaggedStart(
            TransformFromCopy(algebra[0]["a"], algebra[1]["a"]),
            TransformFromCopy(algebra[0]["+ bi"], algebra[1]["+ bi"]),
            TransformFromCopy(algebra[0]["i"][0], algebra[1]["i"][0]),
            TransformFromCopy(algebra[0]["i"][0], algebra[1]["2"]),
            lag_ratio=0.25
        ))
        self.wait()
        self.play(LaggedStart(
            TransformFromCopy(algebra[1]["bi^2"], algebra[2]["-b"]),
            TransformFromCopy(algebra[1]["ai"], algebra[2]["ai"]),
            TransformFromCopy(algebra[1]["+"], algebra[2]["+"]),
            lag_ratio=0.25
        ))
        self.wait()

        # New lines
        new_lines = lines.copy()
        new_lines.rotate(90 * DEG)
        new_lines.refresh_bounding_box()
        new_lines[1].move_to(ORIGIN, RIGHT)
        new_lines[0].move_to(new_lines[1].get_left(), DOWN)

        neg_b_label = Tex(R"-b", fill_color=PINK, font_size=36).next_to(new_lines[1], UP, SMALL_BUFF)
        new_a_label = Tex(R"a", fill_color=YELLOW, font_size=36).next_to(new_lines[0], LEFT, SMALL_BUFF)

        self.play(
            TransformFromCopy(lines[1], new_lines[1]),
            FadeTransform(algebra[2]["-b"].copy(), neg_b_label),
        )
        self.play(
            TransformFromCopy(lines[0], new_lines[0]),
            FadeTransform(algebra[2]["a"].copy(), new_a_label),
        )
        self.wait()
