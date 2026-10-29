# ==============================================================================
# Scene:      ShellTimesThickness
# Source:     videos/_2026/spheres_talk/supplements.py (lines 627-654)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShellTimesThickness.py ShellTimesThickness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShellTimesThickness(InteractiveScene):
    def construct(self):
        # Test
        equation = Tex(R"V(\partial B^n) \times {1 \over n} = V(B^n)", font_size=72)
        shell_rect = SurroundingRectangle(equation[R"V(\partial B^n)"]).set_stroke(TEAL, 2)
        thickness_rect = SurroundingRectangle(equation[R"{1 \over n}"]).set_stroke(YELLOW, 2)
        volume_rect = SurroundingRectangle(equation[R"V(B^n)"]).set_stroke(BLUE, 2)
        rects = VGroup(shell_rect, thickness_rect, volume_rect)
        for rect in rects:
            rect.set_height(rects.get_height(), stretch=True)
            rect.align_to(rects, UP)

        labels = VGroup()
        for rect, text in zip(rects, ["Shell", "Thickness", "Total\nVolume"]):
            label = Text(text, font_size=48)
            label.match_color(rect)
            label.next_to(rect, DOWN)
            labels.add(label)
        # for label in labels:
        #     label.align_to(labels, DOWN)

        radius_label = Text("(When radius=1)", font_size=36)
        radius_label.set_color(GREY_C)
        radius_label.next_to(labels, DOWN, MED_LARGE_BUFF).match_x(equation)

        self.add(equation, radius_label)
        self.add(rects)
        self.add(labels)
