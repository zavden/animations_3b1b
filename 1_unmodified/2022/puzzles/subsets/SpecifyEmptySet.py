# ==============================================================================
# Scene:      SpecifyEmptySet
# Source:     videos/_2022/puzzles/subsets.py (lines 1501-1545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SpecifyEmptySet.py SpecifyEmptySet -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SpecifyEmptySet(TeacherStudentsScene):
    def construct(self):
        # Ask
        morty = self.teacher
        ss = self.students
        self.student_says(
            "Do we count\nthe empty set?",
            bubble_config=dict(direction=RIGHT),
            target_mode="raise_right_hand",
            added_anims=[
                morty.change("happy"),
                ss[0].change("hesitant"),
                ss[0].change("pondering"),
            ]
        )
        self.wait()

        # Facts
        kw = dict(tex_to_color_map={"\\{\\}": YELLOW})
        facts = VGroup(
            Tex("\\text{We do count } \\{\\}", **kw),
            Tex("\\text{sum}(\\{\\}) = 0", **kw),
            OldTexText("0 is a multiple of 5", **kw),
        )
        facts.next_to(morty.get_corner(UL), UP, MED_LARGE_BUFF)

        last_facts = VGroup()
        for fact in facts:
            self.play(
                FadeIn(fact, 0.5 * UP),
                morty.change("raise_right_hand", fact),
                ss[0].change("pondering", fact),
                ss[1].change("pondering", fact),
                ss[2].change("pondering", fact),
                last_facts.animate.shift(UP)
            )
            self.wait()
            last_facts.add(fact)
        self.wait()
        self.play(
            RemovePiCreatureBubble(ss[2], target_mode="happy"),
            ss[0].change("thinking"),
            ss[1].change("tease"),
        )
        self.wait(3)
