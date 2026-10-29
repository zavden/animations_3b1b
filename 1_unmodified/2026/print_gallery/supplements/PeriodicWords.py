# ==============================================================================
# Scene:      PeriodicWords
# Source:     videos/_2026/print_gallery/supplements.py (lines 550-584)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PeriodicWords.py PeriodicWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PeriodicWords(InteractiveScene):
    def construct(self):
        # Test
        periodic = Text("Periodic")
        vertically = Text("Vertically")
        horizontally = Text("Horizontally")
        doubly = Text("Doubly")
        for word in [periodic, vertically, horizontally, doubly]:
            word.scale(1.5)
            word.set_backstroke(BLACK, 3)

        periodic.target = periodic.generate_target()

        group1 = VGroup(periodic, vertically)
        group2 = VGroup(doubly, periodic.target)
        for group in [group1, group2]:
            group.arrange(RIGHT, aligned_edge=UP, buff=0.35)
            group.to_edge(UP)
            group.set_backstroke(BLACK, 3)
        horizontally.move_to(vertically, UL)

        self.play(Write(group1, stroke_color=WHITE, run_time=2))
        self.wait()
        self.play(LaggedStart(
            FadeIn(horizontally, 0.75 * UP),
            FadeOut(vertically, 0.75 * UP),
            lag_ratio=0.2
        ))
        self.wait()
        self.play(
            MoveToTarget(periodic, path_arc=45 * DEG),
            FadeTransform(horizontally, doubly, path_arc=45 * DEG),
            run_time=2
        )
        self.wait()
