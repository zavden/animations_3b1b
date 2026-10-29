# ==============================================================================
# Scene:      ShowAngleRange
# Source:     videos/_2024/transformers/mlp.py (lines 2183-2199)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ShowAngleRange.py ShowAngleRange -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *


# ----- From _2024/transformers/helpers.py -----

def get_vector_pair(angle_in_degrees=90, length=1.0, colors=(BLUE, BLUE)):
    angle = angle_in_degrees * DEGREES
    v1 = Vector(length * RIGHT)
    v2 = v1.copy().rotate(angle, about_point=ORIGIN)
    v1.set_color(colors[0])
    v2.set_color(colors[1])
    arc = Arc(radius=0.2, angle=angle)
    arc.set_stroke(WHITE, 2)
    label = Tex(Rf"180^\circ", font_size=24)
    num = label.make_number_changeable("180")
    num.set_value(angle_in_degrees)
    label.next_to(arc.pfp(0.5), normalize(arc.pfp(0.5)), buff=SMALL_BUFF)

    return VGroup(v1, v2, arc, label)



# ----- From _2024/transformers/mlp.py -----

class ShowAngleRange(InteractiveScene):
    def construct(self):
        # Test
        angle_tracker = ValueTracker(10)
        vect_pair = always_redraw(lambda: get_vector_pair(angle_tracker.get_value(), length=3, colors=(RED, GREEN)))

        self.add(vect_pair)
        self.play(
            angle_tracker.animate.set_value(180),
            run_time=8,
        )
        self.wait()
        self.play(
            angle_tracker.animate.set_value(95),
            run_time=3
        )
        self.wait()
