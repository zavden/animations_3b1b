# ==============================================================================
# Scene:      FeynmansLostLectureWrapper
# Source:     videos/_2018/dandelin.py (lines 168-178)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeynmansLostLectureWrapper.py FeynmansLostLectureWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FeynmansLostLectureWrapper(Scene):
    def construct(self):
        title = OldTexText("Feynman's Lost Lecture")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
