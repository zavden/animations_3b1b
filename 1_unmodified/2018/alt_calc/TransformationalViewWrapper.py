# ==============================================================================
# Scene:      TransformationalViewWrapper
# Source:     videos/_2018/alt_calc.py (lines 1023-1026)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransformationalViewWrapper.py TransformationalViewWrapper -w -m --fps 15
# ==============================================================================

 # -*- coding: utf-8 -*-
from manim_imports_ext import *

class Wrapper(Scene):
    CONFIG = {
        "title": "",
        "title_kwargs": {},
        "screen_height": 6,
        "wait_time": 2,
    }

    def construct(self):
        rect = self.rect = ScreenRectangle(height=self.screen_height)
        title = self.title = OldTexText(self.title, **self.title_kwargs)
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait(self.wait_time)


class TransformationalViewWrapper(Wrapper):
    CONFIG = {
        "title": "Transformational view"
    }
