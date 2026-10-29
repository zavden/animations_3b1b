# ==============================================================================
# Scene:      PonderOverOffCenterDiagram
# Source:     videos/_2018/lost_lecture.py (lines 3543-3607)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PonderOverOffCenterDiagram.py PonderOverOffCenterDiagram -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PonderOverOffCenterDiagram(PiCreatureScene):
    def construct(self):
        randy, morty = self.pi_creatures
        velocity_diagram = self.get_velocity_diagram()
        bubble = randy.get_bubble()

        rect = SurroundingRectangle(
            velocity_diagram,
            buff=MED_LARGE_BUFF,
            color=GREY_B
        )
        rect.stretch(1.2, 1, about_edge=DOWN)
        words = OldTexText("Velocity space")
        words.next_to(rect.get_top(), DOWN)

        self.play(
            LaggedStartMap(GrowFromCenter, velocity_diagram),
            randy.change, "pondering",
            morty.change, "confused",
        )
        self.wait(2)
        self.play(ShowCreation(bubble))
        self.wait(2)
        self.play(
            FadeOut(bubble),
            randy.change, "confused",
            morty.change, "pondering",
            ShowCreation(rect)
        )
        self.play(Write(words))
        self.wait(2)

    def create_pi_creatures(self):
        randy = Randolph(height=2.5)
        randy.to_corner(DL)
        morty = Mortimer(height=2.5)
        morty.to_corner(DR)
        return randy, morty

    def get_velocity_diagram(self):
        circle = Circle(color=WHITE, radius=2)
        circle.rotate(90 * DEGREES)
        circle.to_edge(DOWN, buff=LARGE_BUFF)
        root_point = interpolate(
            circle.get_center(),
            circle.get_bottom(),
            0.5,
        )
        dot = Dot(root_point)
        vectors = VGroup()
        for a in np.arange(0, 1, 1.0 / 24):
            end_point = circle.point_from_proportion(a)
            vector = Arrow(root_point, end_point, buff=0)
            vector.set_color(interpolate_color(
                BLUE, RED,
                inverse_interpolate(
                    1, 3, vector.get_length(),
                )
            ))
            vector.add_to_back(vector.copy().set_stroke(BLACK, 5))
            vectors.add(vector)

        vectors.add_to_back(circle)
        vectors.add(dot)
        return vectors
