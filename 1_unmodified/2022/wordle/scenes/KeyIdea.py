# ==============================================================================
# Scene:      KeyIdea
# Source:     videos/_2022/wordle/scenes.py (lines 1796-1814)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl KeyIdea.py KeyIdea -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class KeyIdea(Scene):
    def construct(self):
        title = Text("Key idea", font_size=72)
        title.to_edge(UP, LARGE_BUFF)
        title.add(Underline(title, buff=-SMALL_BUFF, stroke_width=0.5).scale(1.5))
        title.set_color(YELLOW)
        idea = OldTexText("Informative", " $\\Leftrightarrow$", " Unlikely", font_size=72)
        self.add(title)
        idea[0].save_state()
        idea[0].center()
        self.play(FadeIn(idea[0]))
        self.wait()
        self.play(
            Restore(idea[0]),
            FadeIn(idea[1], RIGHT),
            FadeIn(idea[2], 2 * RIGHT)
        )
        self.play(FlashAround(idea, run_time=2))
        self.wait()
