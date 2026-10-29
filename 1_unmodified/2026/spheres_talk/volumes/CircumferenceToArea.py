# ==============================================================================
# Scene:      CircumferenceToArea
# Source:     videos/_2026/spheres_talk/volumes.py (lines 35-74)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircumferenceToArea.py CircumferenceToArea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CircumferenceToArea(InteractiveScene):
    def construct(self):
        # Test
        t2c = {"{r}": BLUE}
        circum_formula = Tex(R"\text{Circumference} = 2 \pi {r}", t2c=t2c)

        radius = 3
        circle = Circle(radius=radius)
        circle.set_stroke(YELLOW, 5)
        radius_line = Line(ORIGIN, radius * RIGHT)
        radius_line.set_stroke(WHITE, 3)
        r_label = Tex(R"r", font_size=72)
        r_label.set_color(BLUE)
        r_label.next_to(radius_line, UP, SMALL_BUFF)
        r_group = VGroup(radius_line, r_label)
        r_group.set_z_index(1)

        self.add(circle, r_group)
        self.play(
            ShowCreation(circle),
            Rotate(r_group, TAU, about_point=ORIGIN),
            run_time=3,
        )
        self.wait()

        # Inner circles
        circles = VGroup(
            circle.copy().set_width(a * circle.get_width())
            for a in np.linspace(1, 0, 100)
        )
        circles.set_stroke(YELLOW, 3, 0.25)
        self.play(
            ReplacementTransform(
                circle.replicate(len(circles)).set_stroke(width=0, opacity=0),
                circles,
                lag_ratio=0.1
            ),
            run_time=3
        )
        self.wait()
