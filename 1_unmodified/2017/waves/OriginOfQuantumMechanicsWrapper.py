# ==============================================================================
# Scene:      OriginOfQuantumMechanicsWrapper
# Source:     videos/_2017/waves.py (lines 560-563)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OriginOfQuantumMechanicsWrapper.py OriginOfQuantumMechanicsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class VideoWrapper(Scene):
    CONFIG = {
        "title" : ""
    }
    def construct(self):
        title = OldTexText(self.title)
        title.to_edge(UP)
        self.add(title)
        rect = ScreenRectangle()
        rect.set_height(6)
        rect.next_to(title, DOWN)
        self.add(rect)
        self.wait()


class OriginOfQuantumMechanicsWrapper(VideoWrapper):
    CONFIG = {
        "title" : "The origin of quantum mechanics"
    }
