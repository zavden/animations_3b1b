# ==============================================================================
# Scene:      BringTogether
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 110-125)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BringTogether.py BringTogether -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BringTogether(Scene):
    def construct(self):
        arrows = VGroup(Vector(2 * RIGHT), Vector(2 * LEFT))
        arrows.arrange(RIGHT, buff=2)
        words = OldTexText("Bring together")[0]
        words.next_to(arrows, DOWN)
        words.save_state()
        words.space_out_submobjects(1.2)

        self.play(
            VFadeIn(words),
            Restore(words),
            arrows.arrange, RIGHT, {"buff": SMALL_BUFF},
            VFadeIn(arrows),
        )
        self.play(FadeOut(words), FadeOut(arrows))
