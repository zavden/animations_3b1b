# ==============================================================================
# Scene:      ComingUpWrapper
# Source:     videos/_2022/puzzles/subsets.py (lines 4629-4655)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComingUpWrapper.py ComingUpWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComingUpWrapper(VideoWrapper):
    title = "Generating functions"
    wait_time = 0

    def construct(self):
        super().construct()
        self.wait(10)
        kw = self.title_config
        new_title = OldTexText("A Complex trick".replace("C", "$\\mathds{C}$"), **kw)
        parens = OldTexText("(secretly Fourier)", **kw)
        new_title.move_to(self.title_text, DOWN)
        new_title.generate_target()
        group = VGroup(new_title.target, parens)
        group.arrange(RIGHT, MED_LARGE_BUFF)
        group.move_to(self.title_text, DOWN)

        self.boundary.clear_updaters()
        self.play(
            FadeOut(self.title_text, UP),
            FadeIn(new_title, UP),
        )
        self.wait(4)
        self.play(
            Write(parens),
            MoveToTarget(new_title)
        )
        self.wait(10)
