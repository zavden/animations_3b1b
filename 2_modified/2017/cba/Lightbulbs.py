# ==============================================================================
# Scene:      Lightbulbs
# Source:     videos/_2017/cba.py (lines 293-352)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Lightbulbs.py Lightbulbs -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo saved numbered stills with file_writer.get_image_file_path/get_image; GL has no such API: hold each state for 1 s in the video instead
# ==============================================================================

from manim_imports_ext import *

class EnumerableSaveScene(Scene):
    def setup(self):
        self.save_count = 0

    def save_enumerated_image(self):
        # CHANGE: Cairo saved numbered stills with file_writer.get_image_file_path/get_image; GL has no such API: hold each state for 1 s in the video instead
        self.wait(1)
        self.save_count += 1


class Lightbulbs(EnumerableSaveScene):
    def construct(self):
        dots = VGroup(*[Dot() for x in range(4)])
        dots.set_height(0.5)
        dots.arrange(RIGHT, buff=2)
        dots.set_fill(opacity=0)
        dots.set_stroke(width=2, color=WHITE)
        dot_radius = dots[0].get_width() / 2

        connections = VGroup()
        for d1, d2 in it.product(dots, dots):
            line = Line(
                d1.get_center(),
                d2.get_center(),
                path_arc=30 * DEGREES,
                buff=dot_radius,
                color=YELLOW,
            )
            connections.add(line)

        lower_dots = dots[:3].copy()
        lower_dots.next_to(dots, DOWN, buff=2)
        lower_lines = VGroup(*[
            Line(d.get_center(), ld.get_center(), buff=dot_radius)
            for d, ld in it.product(dots, lower_dots[1:])
        ])
        lower_lines.match_style(connections)

        top_dot = dots[0].copy()
        top_dot.next_to(dots, UP, buff=2)

        top_lines = VGroup(*[
            Line(d.get_center(), top_dot.get_center(), buff=dot_radius)
            for d in dots
        ])
        top_lines.match_style(connections)

        self.add(dots)
        self.add(top_dot)
        self.save_enumerated_image()
        dots.set_fill(YELLOW, 1)
        self.save_enumerated_image()
        self.add(connections)
        self.save_enumerated_image()
        self.add(lower_dots)
        self.add(lower_lines)
        lower_dots[1:].set_fill(YELLOW, 1)
        self.save_enumerated_image()

        self.add(top_lines)
        connections.set_stroke(width=1)
        lower_lines.set_stroke(width=1)
        top_dot.set_fill(YELLOW, 1)
        self.save_enumerated_image()

        self.remove(connections)
        self.remove(top_lines)
        self.remove(lower_lines)
        dots.set_fill(opacity=0)
        lower_dots.set_fill(opacity=0)
