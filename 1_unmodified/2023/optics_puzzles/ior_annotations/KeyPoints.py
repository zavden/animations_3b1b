# ==============================================================================
# Scene:      KeyPoints
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 405-425)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyPoints.py KeyPoints -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KeyPoints(InteractiveScene):
    def construct(self):
        key_points = VGroup(
            Text("Key point #1: Phase kicks"),
            Text("Key point #2: Layer oscillations"),
            Text("Key point #3: Resonance"),
        )
        key_points.set_submobject_colors_by_gradient(BLUE, TEAL, YELLOW)
        key_points.scale(1.25)
        key_points.to_edge(UP, buff=0.25)
        key_points.set_backstroke(BLACK, 4)
        key_points.to_edge(UP)

        self.add(key_points[0])
        self.wait()
        for kp1, kp2 in zip(key_points, key_points[1:]):
            self.play(
                FadeOut(kp1, 0.5 * UP),
                FadeIn(kp2, 0.5 * UP),
            )
            self.wait()
