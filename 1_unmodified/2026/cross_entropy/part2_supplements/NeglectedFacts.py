# ==============================================================================
# Scene:      NeglectedFacts
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 374-405)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NeglectedFacts.py NeglectedFacts -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NeglectedFacts(TeacherStudentsScene):
    def construct(self):
        # Test
        morty = self.teacher
        stds = self.students

        neglected_facts = VGroup(
            Text("Batch size scheduling"),
            Text("Optimizer choice and tuning"),
            Text("Learning rate schedules"),
            Text("Gradient clipping"),
            Text("Compute-optimal scaling laws"),
            Tex(R"\vdots")
        )
        neglected_facts.arrange(DOWN, aligned_edge=LEFT)
        neglected_facts[-1].set_x(neglected_facts.get_x() - 1)
        neglected_facts.to_corner(UR)

        self.add(neglected_facts)

        self.play(
            morty.change("raise_left_hand", look_at=5 * UR),
            self.change_students("sassy", "hesitant", "guilty", look_at=5 * UR),
            LaggedStartMap(FadeIn, neglected_facts, shift=0.5 * DOWN, lag_ratio=0.7, run_time=5)
        )
        self.wait(3)
        self.play(
            morty.change("tease", stds),
            self.change_students("pondering", "sassy", "pondering"),
            LaggedStartMap(FadeOut, neglected_facts, shift=RIGHT, lag_ratio=0.1),
        )
        self.wait()
