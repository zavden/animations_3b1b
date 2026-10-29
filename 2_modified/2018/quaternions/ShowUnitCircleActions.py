# ==============================================================================
# Scene:      ShowUnitCircleActions
# Source:     videos/_2018/quaternions.py (lines 2028-2152)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowUnitCircleActions.py ShowUnitCircleActions -w -m --fps 15
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


class ShowUnitCircleActions(ShowComplexMultiplicationExamples):
    CONFIG = {
        "random_seed": 0,
        "plane_config": {
            "secondary_line_ratio": 0,
        }
    }

    def construct(self):
        self.add_planes(include_title=False)
        self.show_unit_circle_actions()

    def show_unit_circle_actions(self):
        plane = self.plane
        origin = plane.number_to_point(0)
        one_point = plane.number_to_point(1)
        one_dot = Dot(one_point)
        one_dot.set_fill(WHITE)
        one_dot.set_stroke(BLACK, 1)
        plane.add(one_dot)

        pin = PushPin()
        pin.move_to(origin, DR)
        hand = Hand()
        update_hand = UpdateFromFunc(
            hand, lambda m: m.move_to(one_dot.get_center(), LEFT)
        )

        circle = Circle(
            color=YELLOW,
            radius=get_norm(one_point - origin)
        )

        self.add(circle)
        self.add(pin, one_dot)
        self.add_foreground_mobjects(hand)

        title = OldTexText(
            "Numbers on the unit circle",
            "$\\rightarrow$", "pure rotation."
        )
        title.set_width(FRAME_WIDTH - 1)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.add_background_rectangle(buff=SMALL_BUFF)
        self.add_foreground_mobjects(title)
        self.background_plane.coordinate_labels.submobjects.pop(-1)

        n_angles = 12
        angles = list(np.linspace(-PI, PI, n_angles + 2)[1:-1])
        random.shuffle(angles)

        for angle in angles:
            plane.save_state()
            temp_plane = plane.copy()

            z = np.exp(complex(0, angle))
            if angle is angles[0]:
                z_label = DecimalNumber(
                    z, num_decimal_places=2,
                )
                z_label.set_stroke(BLACK, width=11, background=True)
                z_label_rect = BackgroundRectangle(z_label)
                z_label_rect.set_fill(opacity=0)
            z_point = plane.number_to_point(z)
            z_arrow = Arrow(2.5 * z_point, z_point, buff=SMALL_BUFF)
            z_dot = Dot(z_point)
            z_label_start_center = z_label.get_center()
            z_label.next_to(
                z_arrow.get_start(),
                np.sign(z_arrow.get_start()[1]) * UP,
            )
            z_label_end_center = z_label.get_center()
            z_group = VGroup(z_arrow, z_dot, z_label)
            z_group.set_color(GREEN)
            z_group.add_to_back(z_label_rect)
            z_arrow.set_stroke(BLACK, 1)
            z_dot.set_stroke(BLACK, 1)

            if angle is angles[0]:
                self.play(
                    FadeInFromDown(z_label_rect),
                    FadeInFromDown(z_label),
                    GrowArrow(z_arrow),
                    FadeInFromLarge(z_dot),
                )
            else:
                alpha_tracker = ValueTracker(0)
                self.play(
                    ReplacementTransform(old_z_dot, z_dot),
                    ReplacementTransform(old_z_arrow, z_arrow),
                    UpdateFromFunc(
                        z_label_rect,
                        lambda m: m.replace(z_label)
                    ),
                    ChangeDecimalToValue(
                        z_label, z,
                        position_update_func=lambda m: m.move_to(
                            interpolate(
                                z_label_start_center,
                                z_label_end_center,
                                alpha_tracker.get_value()
                            )
                        )
                    ),
                    alpha_tracker.set_value, 1,
                    # hand.move_to, one_point, LEFT
                )
            old_z_dot = z_dot
            old_z_arrow = z_arrow
            VGroup(old_z_arrow, old_z_dot)
            self.play(
                Rotate(plane, angle, run_time=2),
                update_hand,
                Animation(z_group),
            )
            self.wait()
            self.add(temp_plane, z_group)
            self.play(
                FadeOut(plane),
                FadeOut(hand),
                FadeIn(temp_plane),
            )
            plane.restore()
            self.remove(temp_plane)
            self.add(plane, *z_group)
