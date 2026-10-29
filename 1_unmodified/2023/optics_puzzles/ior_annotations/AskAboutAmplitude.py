# ==============================================================================
# Scene:      AskAboutAmplitude
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1014-1028)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutAmplitude.py AskAboutAmplitude -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskAboutAmplitude(InteractiveScene):
    def construct(self):
        # Test
        lines = DashedLine(3 * LEFT, 3 * RIGHT).replicate(2)
        lines.arrange(DOWN, buff=0.8)
        brace = Brace(lines, LEFT)
        text = brace.get_text("What is this\nAmplitude?")
        text.set_backstroke(BLACK, 8)

        self.play(*map(ShowCreation, lines))
        self.play(
            GrowFromCenter(brace),
            Write(text),
        )
        self.wait()
