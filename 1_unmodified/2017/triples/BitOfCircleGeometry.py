# ==============================================================================
# Scene:      BitOfCircleGeometry
# Source:     videos/_2017/triples.py (lines 2912-2958)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BitOfCircleGeometry.py BitOfCircleGeometry -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BitOfCircleGeometry(Scene):
    def construct(self):
        circle = Circle(color = BLUE, radius = 3)
        p0, p1, p2 = [
            circle.point_from_proportion(alpha)
            for alpha in (0, 0.15, 0.55)
        ]
        O = circle.get_center()
        O_dot = Dot(O, color = WHITE)
        self.add(circle, O_dot)


        groups = VGroup()
        for point, tex, color in (O, "2", MAROON_B), (p2, "", RED):
            line1 = Line(point, p0)
            line2 = Line(point, p1)
            dot1 = Dot(p0)
            dot2 = Dot(p1)
            angle = line1.get_angle()
            arc = Arc(
                angle = line2.get_angle()-line1.get_angle(), 
                start_angle = line1.get_angle(),
                radius = 0.75,
                color = WHITE
            )
            arc.set_stroke(YELLOW, 3)
            arc.shift(point)
            label = OldTex(tex + "\\theta")
            label.next_to(
                arc.point_from_proportion(0.9), RIGHT
            )

            group = VGroup(line1, line2, dot1, dot2)
            group.set_color(color)
            group.add(arc, label)
            if len(groups) == 0:
                self.play(*list(map(ShowCreation, [dot1, dot2])))
                self.play(*list(map(ShowCreation, [line1, line2])))
                self.play(ShowCreation(arc))
                self.play(FadeIn(label))
            groups.add(group)

        self.wait(2)
        self.play(ReplacementTransform(
            groups[0].copy(), groups[1]
        ))
        self.wait(2)
