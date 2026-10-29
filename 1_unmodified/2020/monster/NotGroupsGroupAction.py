# ==============================================================================
# Scene:      NotGroupsGroupAction
# Source:     videos/_2020/monster.py (lines 1740-1761)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NotGroupsGroupAction.py NotGroupsGroupAction -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NotGroupsGroupAction(Scene):
    def construct(self):
        words = VGroup(
            OldTexText("Group"),
            OldTexText("Group", " action"),
        )
        words.scale(2)
        words.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        words.to_corner(UL)
        group, group_action = words

        cross = Cross(group)

        self.add(group)
        self.wait()
        self.play(ShowCreation(cross))
        self.play(
            TransformFromCopy(group[0], group_action[0]),
            Animation(cross.copy(), remover=True)
        )
        self.play(Write(group_action[1]))
        self.wait()
