# ==============================================================================
# Scene:      IntroduceTetrahedronSupplement
# Source:     videos/_2017/putnam.py (lines 203-224)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceTetrahedronSupplement.py IntroduceTetrahedronSupplement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class IntroduceTetrahedronSupplement(Scene):
    def construct(self):
        title = OldTexText("4", "random$^*$ points on sphere")
        title.set_color(YELLOW)
        question = OldTexText("Probability that this tetrahedron \\\\ contains the sphere's center?")
        question.next_to(title, DOWN, MED_LARGE_BUFF)
        group = VGroup(title, question)
        group.set_width(FRAME_WIDTH-1)
        group.to_edge(DOWN)

        for n in range(1, 4):
            num = OldTexText(str(n))
            num.replace(title[0], dim_to_match = 1)
            num.set_color(YELLOW)
            self.add(num)
            self.wait(0.7)
            self.remove(num)
        self.add(title[0])
        self.play(FadeIn(title[1], lag_ratio = 0.5))
        self.wait(2)
        self.play(Write(question))
        self.wait(2)
