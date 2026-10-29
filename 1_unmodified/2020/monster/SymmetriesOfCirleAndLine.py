# ==============================================================================
# Scene:      SymmetriesOfCirleAndLine
# Source:     videos/_2020/monster.py (lines 3368-3407)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SymmetriesOfCirleAndLine.py SymmetriesOfCirleAndLine -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SymmetriesOfCirleAndLine(Scene):
    def construct(self):
        line = NumberLine((0, 100, 1))
        line.move_to(2 * UP)

        circle = Circle(radius=1)
        circle_ticks = VGroup(*[
            Line(0.95 * vect, 1.05 * vect)
            for vect in compass_directions(12)
        ])
        circle.add(circle_ticks)
        circle.set_stroke(BLUE, 3)
        circle.scale(1.5)
        circle.next_to(line, DOWN, buff=2)
        circle.shift(RIGHT)

        R_label = OldTex("\\mathds{R}")
        RmodZ = OldTex("\\mathds{R} / \\mathds{Z}")
        R_label.set_height(0.9)
        R_label.next_to(line, UP, MED_LARGE_BUFF)
        RmodZ.set_height(0.9)
        RmodZ.next_to(circle, LEFT, LARGE_BUFF)
        R_label.match_x(RmodZ)

        self.add(line)
        self.add(circle)
        self.add(R_label)
        self.add(RmodZ)

        # Rotations and shifts
        for n in range(10):
            x = interpolate(-20, 20, random.random())
            self.play(
                line.shift, x * RIGHT,
                Rotate(circle, -x / PI),
                run_time=2,
            )
            self.wait()

        self.embed()
