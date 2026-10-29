# ==============================================================================
# Scene:      Test
# Source:     videos/_2017/dominos/domino_play.py (lines 807-872)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Test.py Test -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Test(Scene):
    def construct(self):
        shift_val = 1.5

        domino1 = Rectangle(
            width = 0.5, height = 3,
            stroke_width = 0,
            fill_color = GREEN,
            fill_opacity = 1
        )
        domino1.shift(LEFT)
        domino2 = domino1.copy()
        domino2.set_fill(BLUE_E)
        domino2.shift(shift_val*RIGHT)
        spacing = shift_val - domino2.get_width()
        dominos = VGroup(domino1, domino2)
        for domino in dominos:
            line = DashedLine(domino.get_left(), domino.get_right())
            dot = Dot(domino.get_center())
            domino.add(line, dot)

        arc1 = Arc(
            radius = domino1.get_height(),
            start_angle = np.pi/2,
            angle = -np.arcsin(spacing / domino1.get_height())
        )
        arc1.shift(domino1.get_corner(DOWN+RIGHT))
        arc2 = Arc(
            radius = domino1.get_height()/2,
            start_angle = np.pi/2,
            angle = -np.arcsin(2*spacing/domino1.get_height())
        )
        arc2.shift(domino1.get_right())
        arc2.set_color(BLUE)
        arcs = VGroup(arc1, arc2)
        for arc, vect in zip(arcs, [DOWN+RIGHT, RIGHT]):
            arc_copy = arc.copy()
            point = domino1.get_bounding_box_point(vect)
            arc_copy.add_line_to([point])
            arc_copy.set_stroke(width = 0)
            arc_copy.set_fill(
                arc.get_stroke_color(),
                0.2,
            )
            self.add(arc_copy)

        domino1_ghost = domino1.copy()
        domino1_ghost.fade(0.8)
        self.add(domino1_ghost, dominos, arcs)

        self.play(Rotate(
            domino1,
            angle = arc1.angle,
            about_point = domino1.get_corner(DOWN+RIGHT),
            rate_func = there_and_back,
            run_time = 3,
        ))
        self.play(Rotate(
            domino1,
            angle = arc2.angle,
            about_point = domino1.get_right(),
            rate_func = there_and_back,
            run_time = 3,
        ))

        print(arc1.angle, arc2.angle)
