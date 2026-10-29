# ==============================================================================
# Scene:      FeynmanLecturesScreenCaptureFrame
# Source:     videos/_2018/lost_lecture.py (lines 573-583)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FeynmanLecturesScreenCaptureFrame.py FeynmanLecturesScreenCaptureFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FeynmanLecturesScreenCaptureFrame(Scene):
    def construct(self):
        url = OldTexText("http://www.feynmanlectures.caltech.edu/")
        url.to_edge(UP)

        screen_rect = ScreenRectangle(height=6)
        screen_rect.next_to(url, DOWN)

        self.add(url)
        self.play(ShowCreation(screen_rect))
        self.wait()
