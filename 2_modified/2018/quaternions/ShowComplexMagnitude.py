# ==============================================================================
# Scene:      ShowComplexMagnitude
# Source:     videos/_2018/quaternions.py (lines 4437-4497)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowComplexMagnitude.py ShowComplexMagnitude -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
# ==============================================================================

from manim_imports_ext import *

class ShowComplexMultiplicationExamples(Scene):
    CONFIG = {
        "plane_config": {
            "x_radius": 9,
            "y_radius": 9,
            "stroke_width": 3,
        },
        "background_plane_config": {
            "color": GREY_B,
            "secondary_color": GREY_D,
            "stroke_width": 0.5,
            "stroke_opacity": 0.5,
            "secondary_line_ratio": 0,
        }
    }

    def construct(self):
        self.add_planes()
        z_tuples = [
            (complex(2, 1), "2 + i", UP),
            (complex(5, 2), "5 + 2i", LEFT),
            (
                complex(-np.sqrt(2) / 2, np.sqrt(2) / 2),
                "-\\frac{\\sqrt{2}}{2} + \\frac{\\sqrt{2}}{2} i",
                LEFT,
            ),
            (complex(-4, 1.5), "-4 + 1.5i", RIGHT),
            (complex(3, 0), "3 + 0i", UP),
            (complex(4, -3), "4 + -3i", UP),
        ]

        for z, z_tex, label_vect in z_tuples:
            self.show_multiplication(z, z_tex, label_vect)

    def add_planes(self, include_title=True):
        plane = ComplexPlane(**self.plane_config)
        self.plane = plane
        background_plane = ComplexPlane(**self.background_plane_config)
        background_plane.add_coordinates()
        self.background_plane = background_plane

        self.add(background_plane)
        self.add(plane)

        if include_title:
            title = OldTexText("Complex plane")
            title.scale(1.5)
            title.to_corner(UL, buff=MED_LARGE_BUFF)
            title.shift(SMALL_BUFF * UR)
            self.title = title
            self.add_foreground_mobjects(title)

    def show_multiplication(self, z, z_tex, label_vect):
        z_color = WHITE
        plane = self.plane
        new_plane = plane.deepcopy()
        real_tex, imag_tex = z_tex.split("+")
        label = OldTex(
            "\\text{Multiply by}\\\\",
            real_tex, "+", imag_tex,
            alignment="",
        )
        label[1].set_color(GREEN)
        label[3].set_color(RED)
        label.scale(1.2)

        h_line = Line(
            plane.number_to_point(0),
            plane.number_to_point(z.real),
            color=GREEN,
            stroke_width=5,
        )
        v_line = Line(
            plane.number_to_point(z.real),
            plane.number_to_point(z),
            color=RED,
            stroke_width=5,
        )
        lines = VGroup(h_line, v_line)

        z_point = plane.number_to_point(z)
        z_dot = Dot(z_point)
        z_dot.set_color(z_color)
        label[1:].next_to(z_dot, label_vect)
        label[0].next_to(label[1:], UP)
        # CHANGE: iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
        for mob in list(label):
            label.add_to_back(BackgroundRectangle(mob))

        one_dot = Dot(plane.number_to_point(1))
        one_dot.set_color(YELLOW)
        for dot in z_dot, one_dot:
            dot.save_state()
            dot.scale(5)
            dot.set_fill(opacity=0)
            dot.set_stroke(width=1, opacity=0.5)
        to_fade_out = VGroup(
            plane, label, lines, z_dot, one_dot
        )

        self.play(
            ShowCreation(lines),
            FadeInFromDown(label),
            Restore(z_dot),
        )
        self.play(Restore(one_dot))
        angle = np.log(z).imag
        self.play(
            one_dot.move_to, z_dot,
            plane.apply_complex_function, lambda w: z * w,
            path_arc=angle,
            run_time=3
        )
        self.wait()
        self.play(
            FadeOut(to_fade_out),
            FadeIn(new_plane),
        )
        self.plane = new_plane


class ShowComplexMagnitude(ShowComplexMultiplicationExamples):
    def construct(self):
        self.add_planes()
        plane = self.plane
        tex_to_color_map = {
            "a": YELLOW,
            "b": GREEN,
        }

        z = complex(3, 2)
        z_point = plane.number_to_point(z)
        z_dot = Dot(z_point)
        z_dot.set_color(PINK)
        z_line = Line(plane.number_to_point(0), z_point)
        z_line.set_stroke(WHITE, 2)
        z_label = OldTex(
            "z", "=", "a", "+", "b", "i",
            tex_to_color_map=tex_to_color_map
        )
        z_label.add_background_rectangle()
        z_label.next_to(z_dot, UR, buff=SMALL_BUFF)
        z_norm_label = OldTex("||z||")
        z_norm_label.add_background_rectangle()
        z_norm_label.next_to(ORIGIN, UP, SMALL_BUFF)
        z_norm_label.rotate(z_line.get_angle(), about_point=ORIGIN)
        z_norm_label.shift(z_line.get_center())

        h_line = Line(
            plane.number_to_point(0),
            plane.number_to_point(z.real),
            stroke_color=YELLOW,
            stroke_width=5,
        )
        v_line = Line(
            plane.number_to_point(z.real),
            plane.number_to_point(z),
            stroke_color=GREEN,
            stroke_width=5,
        )

        z_norm_equation = OldTex(
            "||z||", "=", "\\sqrt", "{a^2", "+", "b^2", "}",
            tex_to_color_map=tex_to_color_map
        )
        z_norm_equation.set_background_stroke(width=0)
        z_norm_equation.add_background_rectangle()
        z_norm_equation.next_to(z_label, UP)

        self.add(z_line, h_line, v_line, z_dot, z_label)
        self.play(ShowCreation(z_line))
        self.play(FadeInFromDown(z_norm_label))
        self.wait()
        self.play(
            FadeIn(z_norm_equation[0]),
            FadeIn(z_norm_equation[2:]),
            TransformFromCopy(
                z_norm_label[1:],
                VGroup(z_norm_equation[1]),
            ),
        )
        self.wait()
