# ==============================================================================
# Scene:      EngineersSinc
# Source:     videos/_2022/borwein/supplements.py (lines 328-347)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EngineersSinc.py EngineersSinc -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EngineersSinc(InteractiveScene):
    def construct(self):
        # Blah
        sinc = OldTex(R"{\text{sin}(\pi x) \over \pi x}", tex_to_color_map={R"\pi": TEAL})
        sinc.shift(UP)
        rect = SurroundingRectangle(sinc, buff=SMALL_BUFF)
        rect.set_stroke(YELLOW, 2)
        rect.round_corners()
        rect.insert_n_curves(20)

        label = Text("sinc\n(to an engineer)")
        label.select_part("sinc").scale(1.5, about_edge=DOWN)
        label.next_to(rect, DOWN, MED_LARGE_BUFF)
        label.set_color(GREY_A)

        # self.add(sinc)
        self.play(FadeIn(label, DOWN))
        self.wait()
        self.play(ShowCreation(rect))
        self.wait()
