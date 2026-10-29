# ==============================================================================
# Scene:      RenameTheorem
# Source:     videos/_2026/hairy_ball/supplements.py (lines 33-67)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RenameTheorem.py RenameTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RenameTheorem(InteractiveScene):
    def construct(self):
        # Test
        name1, name2 = names = VGroup(
            Text("Hairy Ball Theorem"),
            Text("Sphere Vector Field Theorem"),
        )
        names.scale(1.25)
        names.arrange(DOWN, buff=1.0, aligned_edge=LEFT)
        names.to_edge(LEFT)

        lines = VGroup()
        for text in ["Hairy", "Ball"]:
            word = name1[text][0]
            line = Line(word.get_left(), word.get_right())
            line.set_stroke(RED, 8)
            lines.add(line)
        lines[0].align_to(lines[1], UP)

        self.add(name1)
        self.wait()
        self.play(
            ShowCreation(lines[1]),
            name1["Ball"].animate.set_opacity(0.5),
            FadeTransformPieces(name1["Ball"].copy(), name2["Sphere"]),
        )
        self.play(
            ShowCreation(lines[0]),
            name1["Hairy"].animate.set_opacity(0.5),
            FadeTransformPieces(name1["Hairy"].copy(), name2["Vector Field"]),
        )
        self.play(
            TransformFromCopy(name1["Theorem"], name2["Theorem"]),
        )
        self.wait()
