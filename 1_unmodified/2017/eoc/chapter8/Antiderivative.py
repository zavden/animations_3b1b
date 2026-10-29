# ==============================================================================
# Scene:      Antiderivative
# Source:     videos/_2017/eoc/chapter8.py (lines 429-497)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/eoc/chapter2.py
#
# Run from this folder:
#     manimgl Antiderivative.py Antiderivative -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2017/eoc/chapter2.py -----

DISTANCE_COLOR = BLUE


VELOCITY_COLOR = GREEN



# ----- From _2017/eoc/chapter8.py -----

class Antiderivative(PiCreatureScene):
    def construct(self):
        functions = self.get_functions("t^2", "2t")
        alt_functions = self.get_functions("???", "t(8-t)")
        top_arc, bottom_arc = arcs = self.get_arcs(functions)
        derivative, antiderivative = self.get_arc_labels(arcs)
        group = VGroup(functions, arcs, derivative, antiderivative)

        self.add(functions, top_arc, derivative)
        self.wait()
        self.play(
            ShowCreation(bottom_arc),
            Write(antiderivative),
            self.pi_creature.change_mode, "raise_right_hand"
        )
        self.wait(2)
        for pair in reversed(list(zip(functions, alt_functions))):
            self.play(
                Transform(*pair),
                self.pi_creature.change_mode, "pondering"
            )
        self.wait(2)

        self.pi_creature_says(
            "But first!", 
            target_mode = "surprised",
            look_at = 50*OUT,
            added_anims = [group.to_edge, LEFT],
            run_time = 1,
        )
        self.wait()

    def get_functions(self, left_tex, right_tex):
        left = OldTex(left_tex)
        left.shift(2*LEFT)
        left.set_color(DISTANCE_COLOR)
        right = OldTex(right_tex)
        right.shift(2*RIGHT)
        right.set_color(VELOCITY_COLOR)
        result = VGroup(left, right)
        result.shift(UP)
        return result

    def get_arcs(self, functions):
        f1, f2 = functions
        top_line = Line(f1.get_corner(UP+RIGHT), f2.get_corner(UP+LEFT))
        bottom_line = Line(f1.get_corner(DOWN+RIGHT), f2.get_corner(DOWN+LEFT))
        top_arc = Arc(start_angle = 5*np.pi/6, angle = -2*np.pi/3)
        bottom_arc = top_arc.copy()
        bottom_arc.rotate(np.pi)
        arcs = VGroup(top_arc, bottom_arc)
        arcs.set_width(top_line.get_width())
        for arc in arcs:
            arc.add_tip()
        top_arc.next_to(top_line, UP)
        bottom_arc.next_to(bottom_line, DOWN)
        bottom_arc.set_color(MAROON_B)

        return arcs

    def get_arc_labels(self, arcs):
        top_arc, bottom_arc = arcs
        derivative = OldTexText("Derivative")
        derivative.next_to(top_arc, UP)
        antiderivative = OldTexText("``Antiderivative''")
        antiderivative.next_to(bottom_arc, DOWN)
        antiderivative.set_color(bottom_arc.get_color())

        return VGroup(derivative, antiderivative)
