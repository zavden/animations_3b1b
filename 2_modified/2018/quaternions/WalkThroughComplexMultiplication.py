# ==============================================================================
# Scene:      WalkThroughComplexMultiplication
# Source:     videos/_2018/quaternions.py (lines 1809-2025)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WalkThroughComplexMultiplication.py WalkThroughComplexMultiplication -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - iterate over a copy: Cairo looped over split() (a new list) while GL iterates the live submobjects list, so adding/removing inside the loop skips or revisits items (the BackgroundRectangle loop never ends)
# ==============================================================================

from manim_imports_ext import *

class PushPin(SVGMobject):
    CONFIG = {
        "file_name": "push_pin",
        "height": 0.5,
        "sheen": 0.7,
        "fill_color": GREY,
    }

    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.rotate(20 * DEGREES)

    def pin_to(self, point):
        self.move_to(point, DR)


class Hand(SVGMobject):
    CONFIG = {
        "file_name": "pinch_hand",
        "height": 0.5,
        "sheen": 0.2,
        "fill_color": ORANGE,
    }

    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        # self.rotate(30 * DEGREES)
        self.add(VectorizedPoint().next_to(self, UP, buff=0.17))


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


class WalkThroughComplexMultiplication(ShowComplexMultiplicationExamples):
    CONFIG = {
        "z": complex(2, 3),
        "w": complex(1, -1),
        "z_color": YELLOW,
        "w_color": PINK,
        "product_color": RED,
    }

    def construct(self):
        self.add_planes(include_title=False)
        self.introduce_z_and_w()
        self.show_action_on_all_complex_numbers()

    def introduce_z_and_w(self):
        # Tolerating code repetition here in case I want
        # to specialize behavior for z or w...
        plane = self.plane
        origin = plane.number_to_point(0)

        z_point = plane.number_to_point(self.z)
        z_dot = Dot(z_point)
        z_line = Line(origin, z_point)
        z_label = VGroup(
            OldTex("z="),
            DecimalNumber(self.z, num_decimal_places=0)
        )
        z_label.arrange(
            RIGHT, buff=SMALL_BUFF,
        )
        z_label.next_to(z_dot, UP, buff=SMALL_BUFF)
        z_label.set_color(self.z_color)
        z_label.add_background_rectangle()
        VGroup(z_line, z_dot).set_color(self.z_color)

        w_point = plane.number_to_point(self.w)
        w_dot = Dot(w_point)
        w_line = Line(origin, w_point)
        w_label = VGroup(
            OldTex("w="),
            DecimalNumber(self.w, num_decimal_places=0)
        )
        w_label.arrange(RIGHT, buff=SMALL_BUFF)
        w_label.next_to(w_dot, DOWN, buff=SMALL_BUFF)
        w_label.set_color(self.w_color)
        w_label.add_background_rectangle()
        VGroup(w_line, w_dot).set_color(self.w_color)

        VGroup(
            z_label[1], w_label[1]
        ).shift(0.25 * SMALL_BUFF * DOWN)

        product = OldTex("z", "\\cdot", "w")
        z_sym, w_sym = product[0], product[2]
        z_sym.set_color(self.z_color)
        w_sym.set_color(self.w_color)
        product.scale(2)
        product.to_corner(UL)
        product.add_background_rectangle()

        self.add(
            z_line, z_label,
            w_line, w_label,
        )
        self.play(LaggedStartMap(
            FadeInFromLarge, VGroup(z_dot, w_dot),
            lambda m: (m, 5),
            lag_ratio=0.8,
            run_time=1.5
        ))
        self.play(
            ReplacementTransform(z_label[1][0].copy(), z_sym)
        )
        self.add(product[:-1])
        self.play(
            ReplacementTransform(w_label[1][0].copy(), w_sym),
            FadeIn(product[2], LEFT),
            FadeIn(product[0]),
        )
        self.wait()

        self.set_variables_as_attrs(
            product,
            z_point, w_point,
            z_dot, w_dot,
            z_line, w_line,
        )

    def show_action_on_all_complex_numbers(self):
        plane = self.plane
        plane.save_state()
        origin = plane.number_to_point(0)
        z = self.z
        angle = np.log(z).imag
        product_tex = self.product[1:]
        z_sym, cdot, w_sym = product_tex

        product = self.z * self.w
        product_point = plane.number_to_point(product)
        product_dot = Dot(product_point)
        product_line = Line(origin, product_point)
        for mob in product_line, product_dot:
            mob.set_color(self.product_color)

        rect = SurroundingRectangle(VGroup(z_sym, cdot))
        rect.set_fill(BLACK, opacity=1)
        func_words = OldTexText("Function on the plane")
        func_words.next_to(
            rect, DOWN,
            buff=MED_SMALL_BUFF,
            aligned_edge=LEFT,
        )
        func_words.set_color(self.z_color)

        sparkly_plane = VGroup()
        for line in plane.family_members_with_points():
            if self.camera.is_in_frame(line):
                for piece in line.get_pieces(10):
                    p1, p2 = piece.get_pieces(2)
                    p1.rotate(PI)
                    pair = VGroup(p1, p2)
                    pair.scale(0.3)
                    sparkly_plane.add(pair)
        sparkly_plane.sort(
            lambda p: 0.1 * get_norm(p) + random.random()
        )
        sparkly_plane.set_color_by_gradient(YELLOW, RED, PINK, BLUE)
        sparkly_plane.set_stroke(width=4)

        pin = PushPin()
        pin.move_to(origin, DR)

        one_dot = Dot(plane.number_to_point(1))
        one_dot.set_fill(WHITE)
        one_dot.set_stroke(BLACK, 1)
        hand = Hand()
        hand.move_to(plane.number_to_point(1), LEFT)

        zero_eq = OldTex("z \\cdot 0 = 0")
        one_eq = OldTex("z \\cdot 1 = z")
        equations = VGroup(zero_eq, one_eq)
        equations.arrange(DOWN)
        equations.scale(1.5)
        for eq in equations:
            eq.add_background_rectangle()
        equations.next_to(func_words, DOWN)
        equations.to_edge(LEFT)

        product_label = VGroup(
            OldTex("z \\cdot w ="),
            DecimalNumber(product, num_decimal_places=0)
        )
        product_label.arrange(RIGHT)
        product_label[0].shift(0.025 * DOWN)
        product_label.next_to(product_dot, UP, SMALL_BUFF)
        product_label.add_background_rectangle()

        big_rect = Rectangle(
            height=4,
            width=6,
            fill_color=BLACK,
            fill_opacity=0.9,
            stroke_width=0,
        )
        big_rect.to_corner(UL, buff=0)

        self.add(big_rect, product_tex, rect, z_sym, cdot)
        self.play(
            FadeIn(big_rect),
            ShowCreation(rect),
            Write(func_words),
            run_time=1
        )
        self.play(
            ReplacementTransform(
                self.w_line.copy(), product_line,
            ),
            ReplacementTransform(
                self.w_dot.copy(), product_dot,
            ),
            path_arc=angle,
            run_time=3
        )
        self.wait()
        self.play(FadeOut(VGroup(product_line, product_dot)))
        self.play(LaggedStartMap(
            ShowCreationThenDestruction, sparkly_plane,
            lag_ratio=0.5,
            run_time=2
        ))
        self.play(
            plane.apply_complex_function, lambda w: z * w,
            Transform(self.w_line, product_line),
            Transform(self.w_dot, product_dot),
            path_arc=angle,
            run_time=9,
            rate_func=lambda t: there_and_back_with_pause(t, 2 / 9)
        )
        self.wait()
        self.play(FadeIn(pin, UL))
        self.play(Write(zero_eq))
        self.play(
            FadeInFromLarge(one_dot),
            FadeIn(hand, UR)
        )
        self.play(Write(one_eq))
        self.wait()
        self.play(
            plane.apply_complex_function, lambda w: z * w,
            ReplacementTransform(self.w_line.copy(), product_line),
            ReplacementTransform(self.w_dot.copy(), product_dot),
            one_dot.move_to, self.z_point,
            hand.move_to, self.z_point, LEFT,
            path_arc=angle,
            run_time=4,
        )
        self.play(Write(product_label))
