# ==============================================================================
# Scene:      JustBecauseYouCantVisualize
# Source:     videos/_2017/highD.py (lines 3419-3434)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl JustBecauseYouCantVisualize.py JustBecauseYouCantVisualize -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class JustBecauseYouCantVisualize(Scene):
    def construct(self):
        phrase = "\\raggedright "
        phrase += "Just because you can't visualize\\\\ "
        phrase += "something   doesn't mean you can't\\\\ "
        phrase += "still think about it visually."
        phrase_mob = OldTexText(*phrase.split(" "))
        phrase_mob.set_color_by_tex("visual", YELLOW)
        phrase_mob.next_to(ORIGIN, UP)

        for part in phrase_mob:
            self.play(LaggedStartMap(
                FadeIn, part,
                run_time = 0.05*len(part)
            ))
        self.wait(2)
