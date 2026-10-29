# ==============================================================================
# Scene:      LineGame
# Source:     videos/_2023/optics_puzzles/bending_waves.py (lines 521-697)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LineGame.py LineGame -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - set_stroke(background=True) -> set_stroke(behind=True) (the argument was renamed)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class LineGame(InteractiveScene):
    def construct(self):
        # Add line and medium
        interface = Line(6 * DL, 6 * UR)
        medium = Square().set_fill(BLUE, 0.2).set_stroke(width=0)
        medium.move_to(ORIGIN, LEFT)
        medium.rotate(-45 * DEGREES, about_point=ORIGIN)
        medium.scale(20, about_point=ORIGIN)
        self.add(medium, interface)

        # Prepare lines, with control
        large_spacing = 1.5
        small_spacing = 0.6 * large_spacing

        circ = Circle(radius=0.5)
        circ.set_fill(interpolate_color(BLUE_E, BLACK, 0.5), 1)
        circ.set_stroke(WHITE, 2)
        circ.next_to(ORIGIN, RIGHT, buff=1.0)
        dial = Vector(0.8 * RIGHT)
        dial.move_to(circ)

        top_lines = self.get_line_group(interface, UP, large_spacing)
        low_lines = always_redraw(lambda: self.get_line_group(
            interface, rotate_vector(dial.get_vector(), -PI / 2), small_spacing,
            line_color=GREEN,
            dot_color=YELLOW
        ))

        top_spacing_label = self.get_spacing_label(top_lines[1], R"\lambda_1")
        low_spacing_label = self.get_spacing_label(low_lines[1], R"\lambda_2")
        low_spacing_label.shift(UP)

        # Add top lines, then lower lines
        self.play(FadeIn(top_lines, lag_ratio=0.1))
        self.play(Write(top_spacing_label))
        self.wait()
        self.highlight_intersection_points(top_lines, PINK, LEFT)
        self.wait()

        # Reposition lower lines
        key_angle = -19.9 * DEGREES
        dial.rotate(key_angle)
        low_lines.update()
        low_spacing_label.rotate(key_angle, about_point=ORIGIN)
        top_lines.save_state()
        self.play(
            top_lines.animate.fade(0.8),
            FadeIn(low_lines, lag_ratio=0.1),
        )
        self.play(Write(low_spacing_label))
        self.wait()
        dial.set_stroke(opacity=0)
        self.play(
            Rotate(dial, -key_angle, run_time=2, remover=True),
            Rotate(low_spacing_label, -key_angle, run_time=2, about_point=ORIGIN),
        )
        dial.set_stroke(opacity=1)
        self.wait()
        self.highlight_intersection_points(low_lines, YELLOW, RIGHT)
        self.play(Restore(top_lines))

        # Rotate lower lines
        self.add(low_lines)
        self.play(
            FadeIn(circ),
            FadeIn(dial)
        )
        low_lines.resume_updating()
        for angle in [-15, -15, 10.1]:
            self.play(
                Rotate(dial, angle * DEGREES),
                Rotate(low_spacing_label, angle * DEGREES, about_point=ORIGIN),
                run_time=3
            )
            self.wait()
        low_lines.suspend_updating()
        self.highlight_intersection_points(low_lines, YELLOW)

        # Ask about angles
        theta1 = top_lines[1][0].get_angle() - interface.get_angle()
        theta2 = low_lines[1][0].get_angle() + TAU - (interface.get_angle() + PI)
        radius = 0.75
        arc1 = Arc(interface.get_angle(), theta1, radius=radius)
        arc2 = Arc(interface.get_angle() + PI, theta2, radius=radius)
        theta1_label = Tex(R"\theta_1", font_size=36)
        theta2_label = Tex(R"\theta_2", font_size=36)
        theta1_label.next_to(arc1.pfp(0.5), UP, SMALL_BUFF)
        theta2_label.next_to(arc2.pfp(0.75), DL, SMALL_BUFF)

        self.play(
            ShowCreation(arc1),
            Write(theta1_label),
            self.frame.animate.set_height(6.5).set_anim_args(run_time=2),
            FadeOut(circ),
            FadeOut(dial),
        )
        self.wait()
        self.play(
            ShowCreation(arc2),
            Write(theta2_label)
        )
        self.wait()

    def get_line_group(
        self,
        interface,
        line_direction=UP,
        spacing=1.0,
        n_lines=17,
        length=30,
        line_color=WHITE,
        line_stroke_width=2,
        dot_radius=0.05,
        dot_color=RED,
        dot_opacity=1,
    ):
        # Calculate dot spacing
        interface_vect = normalize(interface.get_vector())
        line_vect = normalize(line_direction)
        interface_center = interface.get_center()
        angle = angle_between_vectors(interface_vect, line_vect)
        dot_spacing = spacing / math.sin(angle)

        points = [
            interface_center + i * dot_spacing * interface_vect
            for i in range(-n_lines // 2, n_lines // 2 + 1)
        ]
        dots = VGroup(*(
            Dot(point, radius=dot_radius).set_fill(dot_color, dot_opacity)
            for point in points
        ))
        lines = VGroup(*(
            Line(
                point,
                point + length * line_vect,
                stroke_color=line_color,
                stroke_width=line_stroke_width,
            )
            for point in points
        ))
        result = VGroup(dots, lines)
        # CHANGE: set_stroke no longer accepts `background` (it is now called `behind`)
        result.set_stroke(behind=True)
        return result

    def get_spacing_label(self, lines, label_tex):
        n = len(lines)
        line1, line2 = lines[n // 2: (n // 2) + 2]
        x1 = line1.get_x()
        x2 = line2.get_x()
        dist = x2 - x1
        arrows = VGroup(
            Arrow(dist * LEFT / 4, dist * RIGHT / 2, buff=SMALL_BUFF),
            Arrow(dist * RIGHT / 4, dist * LEFT / 2, buff=SMALL_BUFF),
        )
        label = Tex(label_tex)
        label.set_max_width(0.9 * arrows.get_width())
        label.next_to(arrows, UP, MED_SMALL_BUFF)
        result = VGroup(arrows, label)
        result.move_to(VGroup(line1, line2))
        result.shift_onto_screen(buff=LARGE_BUFF)
        label.set_fill(border_width=0.5)
        return result

    def highlight_intersection_points(self, line_group, color, arrow_direction=LEFT):
        points = VGroup(*(p for p in line_group[0] if -4 < p.get_y() < 4))
        arrows = VGroup(*(
            Vector(arrow_direction).next_to(point, -arrow_direction, SMALL_BUFF)
            for point in points
        ))
        arrows.set_color(color)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.25))
        self.play(
            LaggedStartMap(Indicate, line_group[0], scale_factor=2, color=color, lag_ratio=0.2),
            LaggedStartMap(FlashAround, line_group[0], buff=0.2, color=color, lag_ratio=0.2),
            run_time=4,
        )
        self.play(FadeOut(arrows))
