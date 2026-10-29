# ==============================================================================
# Scene:      StrengthInDifferentDirectionsWithDecimal
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 555-609)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl StrengthInDifferentDirectionsWithDecimal.py StrengthInDifferentDirectionsWithDecimal -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arc(angle=0) has length 0 and arc.pfp(0.3) fails with AssertionError in this manimgl; angle=max(angulo, 1e-4) is used
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class StrengthInDifferentDirectionsWithDecimal(InteractiveScene):
    def construct(self):
        line = Line(ORIGIN, 7 * RIGHT)
        line.set_stroke(TEAL, 4)
        # CHANGE: with angle=0 the Arc has length 0 and arc.pfp(0.3) raises AssertionError (manimgl bug in curve_and_prop_of_partial_point); a minimum angle of 1e-4 is used
        arc = always_redraw(lambda: Arc(angle=max(line.get_angle(), 1e-4), radius=0.5))
        angle_label = Integer(0, unit=R"^\circ")
        angle_label.add_updater(lambda m: m.set_value(line.get_angle() / DEGREES))
        angle_label.add_updater(lambda m: m.set_height(clip(arc.get_height(), 0.01, 0.4)))
        angle_label.add_updater(lambda m: m.next_to(arc.pfp(0.3), normalize(arc.pfp(0.3)), SMALL_BUFF, aligned_edge=DOWN))

        strong_words = Text("Strongest in this direction")
        strong_words.next_to(line, UP)
        cos_temp_text = "cos(00*)=0.00"
        weak_words = Text(f"Weaker by a factor of {cos_temp_text}", font_size=36)
        cos_template = weak_words[cos_temp_text][0]
        cos_template.set_opacity(0)
        weak_words.next_to(line, UP)

        strong_words.set_backstroke(BLACK, 10)
        weak_words.set_backstroke(BLACK, 10)

        def get_cos_tex():
            cos_tex = Tex(R"\cos(10^\circ) = 0.00", font_size=36)
            cos_tex.make_number_changeable("10", edge_to_fix=RIGHT).set_value(line.get_angle() / DEGREES)
            cos_tex.make_number_changeable("0.00").set_value(math.cos(line.get_angle()))
            cos_tex.rotate(line.get_angle())
            cos_tex.move_to(weak_words[-len(cos_temp_text) + 1:])
            cos_tex.set_backstroke(BLACK, 10)
            return cos_tex

        cos_tex = always_redraw(get_cos_tex)

        # Test
        self.play(ShowCreation(line), Write(strong_words, run_time=1))
        self.wait(2)
        self.add(arc, angle_label, weak_words, cos_tex)
        self.remove(strong_words)
        rot_group = VGroup(line, weak_words)
        self.play(
            Rotate(rot_group, 30 * DEGREES, about_point=ORIGIN),
            run_time=3
        )
        self.wait(2)
        self.play(
            self.frame.animate.set_height(12),
            Rotate(rot_group, 30 * DEGREES, about_point=ORIGIN),
            run_time=3
        )
        self.wait(2)
        self.play(
            self.frame.animate.set_height(15),
            Rotate(rot_group, 30 * DEGREES, about_point=ORIGIN),
            run_time=3
        )
        self.wait(2)
