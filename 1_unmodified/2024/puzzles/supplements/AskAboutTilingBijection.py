# ==============================================================================
# Scene:      AskAboutTilingBijection
# Source:     videos/_2024/puzzles/supplements.py (lines 849-866)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutTilingBijection.py AskAboutTilingBijection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutTilingBijection(InteractiveScene):
    def construct(self):
        # Test
        arrows = VGroup(
            Tex(R"\longleftarrow", font_size=180),
            Tex(R"\longrightarrow", font_size=180),
        )
        arrows.stretch(1.5, 0)
        arrows.arrange(DOWN)
        top_text = Text("Each stack clearly\ngives a tiling.", font_size=42)
        low_text = Text("But does such tiling\nnecessarily have a stack?", font_size=42)
        top_text.next_to(arrows, UP)
        low_text.next_to(arrows, DOWN)

        self.add(arrows[0], top_text)
        self.wait()
        self.play(Write(low_text), GrowFromCenter(arrows[1]))
        self.wait()
