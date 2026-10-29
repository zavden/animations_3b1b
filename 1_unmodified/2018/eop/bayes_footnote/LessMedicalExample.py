# ==============================================================================
# Scene:      LessMedicalExample
# Source:     videos/_2018/eop/bayes_footnote.py (lines 1158-1171)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LessMedicalExample.py LessMedicalExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LessMedicalExample(Scene):
    def construct(self):
        disease = OldTex("P(\\text{Having a disease})")
        telepathy = OldTex("P(\\text{Telepathy})")
        cross = Cross(disease)

        self.add(disease)
        self.wait()
        self.play(ShowCreation(cross))
        self.play(
            FadeIn(telepathy),
            VGroup(disease, cross).shift, 2*UP
        )
        self.wait()
