# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2020/monster.py (lines 191-209)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_monster(height=3):
    monster = SVGMobject("monster")
    monster.set_fill(GREY_BROWN)
    monster.set_stroke(BLACK, 0.1)
    monster.set_height(height)
    return monster


class Thumbnail(Scene):
    def construct(self):
        monster = get_monster()
        monster.set_height(7)
        monster.to_edge(LEFT)
        monster.set_gloss(0.2)

        words = VGroup(
            OldTexText("The"),
            OldTexText("Monster"),
            OldTexText("Group"),
        )
        words.scale(3.5)
        words.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        words.set_stroke(BLACK, 3, background=True)
        words.to_edge(RIGHT)

        self.add(monster)
        self.add(words)
